from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from random import randint
from typing import Optional, Set

import pymongo
from dagster import OpDefinition, OpExecutionContext, get_dagster_logger, op
from dataclasses_json import DataClassJsonMixin
from pymongo import InsertOne
from pymongo.database import Database
from pymongo.errors import BulkWriteError
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOp
from article._base.ops.save_articles import ArticleDetail
from article._base.resources.alchemy import AlchemyClient, GeneratedQuest
from common.config.avatar import ProviderAvatars
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.date import format_datetime, get_today_utc
from common.utils.id import build_id
from common.utils.resource import build_resource_key
from common.utils.s3 import read_dataclass_json_file_s3


@dataclass
class QuestSchema(DataClassJsonMixin):
  """Quest schema dataclass for persisting in MongoDB collection
  """
  # pylint: disable=invalid-name
  description: str
  choices: list[str]
  answer: int
  createdAt: datetime


@dataclass
class ArticleSchema(DataClassJsonMixin):
  """Article schema dataclass for persisting in MongoDB collection
  """
  # pylint: disable=invalid-name
  title: str
  thumbnailURL: str
  content: str
  link: str
  author: str
  category: str
  subcategory: Optional[str]
  provider: str
  providerAvatarURL: str
  quests: list[QuestSchema]
  postedAt: datetime
  createdAt: datetime
  deletedAt: Optional[datetime] = None


def standardize_quest(quest: GeneratedQuest) -> QuestSchema:
  """Standardize Quest into Mongo's schema

  Args:
      quest (GeneratedQuest): quest

  Returns:
      QuestSchema: Quest schema for MongoDB's collection
  """
  choices = list(quest.distractors)
  rand_ans_idx = randint(0, len(choices))
  choices.insert(rand_ans_idx, quest.answerText)
  return QuestSchema(description=quest.questionText,
                     answer=rand_ans_idx,
                     choices=choices,
                     createdAt=get_today_utc())


class BaseSaveQuestsOp(BaseCategorizedOp):
  """Base Save Quests operation specified with category

    Description:
      Save Quest Operation receives the input of a latest scraped data from S3, then call
      the Alchemy API to generate quests and persist generated data to Duty's DB
  """

  @abstractmethod
  def __init__(self,
               category: StrEnum,
               provider: Providers,
               required_resource_keys: Optional[Set[str]] = None) -> None:
    super().__init__(
        category=category,
        provider=provider,
    )
    # NOTE: Specifying required resource keys will override the default init ones!
    self._required_resource_keys = required_resource_keys if required_resource_keys is not None else {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI),
        str(ResourceKeys.ALCHEMY_CLIENT),
        str(ResourceKeys.DUTY_MONGO_CLIENT),
    }
    self._config_schema = {"filename": str}

  def build(self, **kwargs) -> OpDefinition:
    """Build a base Save Quest operation

    Returns:
        OpDefinition: _description_
    """

    @op(name=build_id(
        provider=self.provider,
        identifier=f"save_{self.category}_quests_db_op",
    ),
        required_resource_keys=self.required_resource_keys,
        config_schema=self.config_schema,
        **kwargs)
    def _op(context: OpExecutionContext):
      """Save Quests operation
        Args (context):
          filename: Detected new file's URI on S3 after scraping event
      """
      filename = context.op_config["filename"]
      s3_resource = getattr(
          context.resources,
          build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI))
      uri = f"{s3_resource}/{self.category}/{filename}"
      alchemy: AlchemyClient = getattr(context.resources,
                                       ResourceKeys.ALCHEMY_CLIENT)
      duty_db: Database = getattr(context.resources,
                                  ResourceKeys.DUTY_MONGO_CLIENT)
      articles: list[ArticleDetail] = read_dataclass_json_file_s3(ArticleDetail,
                                                                  uri,
                                                                  many=True)
      article_count = len(articles)
      if article_count == 0:
        get_dagster_logger().warn(
            "Operation stopped early due to empty article detail results.")
        return
      # Init compound indexes for articles collection
      duty_db.articles.create_index([("postedAt", pymongo.ASCENDING),
                                     ("_id", pymongo.ASCENDING)])
      duty_db.articles.create_index([("category", pymongo.ASCENDING),
                                     ("postedAt", pymongo.ASCENDING),
                                     ("_id", pymongo.ASCENDING)])
      # Insert quests
      get_dagster_logger().info(
          f"Total {article_count} {self.category} articles are going to be processed..."
      )
      insert_requests: list[InsertOne] = []
      for idx, article in enumerate(articles):
        quests: list[GeneratedQuest] = alchemy.generate_quests(article.content)
        get_dagster_logger().info(
            f"Generated {len(quests)} quests for article at: {article.link} ({idx+1})"
        )
        quest_schemas: list[QuestSchema] = [
            standardize_quest(quest) for quest in quests
        ]
        article_schema = ArticleSchema(
            title=article.title,
            thumbnailURL=article.thumbnail_url,
            content=article.content,
            link=article.link,
            author=article.author,
            category=article.category,
            subcategory=article.subcategory,
            provider=self.provider,
            providerAvatarURL=getattr(ProviderAvatars, self.provider.upper()),
            quests=quest_schemas,
            postedAt=format_datetime(article.posted_at),
            createdAt=get_today_utc(),
        )
        insert_requests.append(InsertOne(article_schema.to_dict()))
      error_count = 0
      try:
        duty_db.articles.bulk_write(insert_requests, ordered=False)
      except BulkWriteError as bwe:
        error_count = len(bwe.details.writeErrors)
        get_dagster_logger().error(bwe.details)
      get_dagster_logger().info(
          f"Successfully inserted {article_count-error_count} documents to 'articles' collection."
      )

    return _op
