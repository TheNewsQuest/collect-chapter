from dataclasses import dataclass
from typing import Optional

from dagster import OpDefinition, OpExecutionContext, get_dagster_logger, op
from dataclasses_json import DataClassJsonMixin
from pymongo import InsertOne
from pymongo.database import Database
from pymongo.errors import BulkWriteError

from article._base.ops.base_op import BaseOp
from article._base.ops.save_quests import ArticleSchema
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.date import format_datetime, get_today_utc
from common.utils.resource import build_resource_key
from common.utils.s3 import read_dataclass_multiple_json_lines_s3


@dataclass
class HistoryArticleDetail(DataClassJsonMixin):
  """History Article Detail Data Class
  """
  # pylint: disable=invalid-name
  title: str
  content: str
  postedAt: str
  domain: str
  link: str
  thumbnailURL: str
  category: Optional[str] = None
  author: Optional[str] = None


class InsertHistoryOps(BaseOp):
  """Insert History Articles to Ops

  Args:
      BaseOp (_type_): _description_
  """

  def __init__(self) -> None:
    super().__init__(
        provider=Providers.HISTORY,
        required_resource_keys={
            build_resource_key(Providers.HISTORY, ResourceKeys.S3_RESOURCE_URI),
            str(ResourceKeys.DUTY_MONGO_CLIENT)
        },
    )
    self._config_schema = {"news_file": str}

  def _chunk_insert_db(self, db_client: Database,
                       chunks: list[list[InsertOne]]):
    """Insert individual chunk from list of chunks to Duty DB

    Args:
        db_client (Database): DB Client
        chunks (list[list[InsertOne]]): List of Chunks
    """
    get_dagster_logger().info("Inserting documents by chunks to Duty DB...")
    for chunk in chunks:
      error_count = 0
      try:
        db_client.articles.bulk_write(chunk, ordered=False)
      except BulkWriteError as bwe:
        error_count = len(bwe.details["writeErrors"])
        get_dagster_logger().error(bwe.details)
      get_dagster_logger().info(
          f"Successfully inserted {len(chunk)-error_count} documents of a chunk to 'articles' collection."
      )

  def build(self, **kwargs) -> OpDefinition:

    @op(name=f"{self.provider}_insert_history_ops",
        required_resource_keys=self.required_resource_keys,
        config_schema=self.config_schema,
        **kwargs)
    def _op(context: OpExecutionContext):
      filename = context.op_config["news_file"]
      s3_resource = getattr(
          context.resources,
          build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI))
      duty_db: Database = getattr(context.resources,
                                  ResourceKeys.DUTY_MONGO_CLIENT)
      uri = f"{s3_resource}/{filename}"
      get_dagster_logger().info(f"Reading history articles at file {uri}...")
      history_articles: list[
          HistoryArticleDetail] = read_dataclass_multiple_json_lines_s3(
              HistoryArticleDetail, uri)
      insert_request_chunks: list[list[InsertOne]] = []
      cur_chunk: list[InsertOne] = []
      skip_count = 0
      for history_article in history_articles:
        if not history_article.postedAt:
          skip_count += 1
          continue
        # Chunk by 1000
        if len(cur_chunk) == 1000:
          insert_request_chunks.append(cur_chunk[:])
          cur_chunk.clear()  # Reset
        article_schema = ArticleSchema(
            author=None,
            title=history_article.title,
            content=history_article.content,
            thumbnailURL=history_article.thumbnailURL,
            link=history_article.link,
            category="unknown",
            subcategory=None,
            provider=history_article.domain
            if history_article.domain is not None else "unknown",
            providerAvatarURL=None,
            quests=[],
            postedAt=format_datetime(history_article.postedAt),
            createdAt=get_today_utc(),
        )
        cur_chunk.append(InsertOne(article_schema.to_dict()))
      # Add remaining
      if len(cur_chunk) > 0:
        insert_request_chunks.append(cur_chunk[:])
      get_dagster_logger().info(
          f"Total chunks: {len(insert_request_chunks)} in {len(history_articles)-skip_count} valid elements"
      )
      self._chunk_insert_db(duty_db, insert_request_chunks)

    return _op
