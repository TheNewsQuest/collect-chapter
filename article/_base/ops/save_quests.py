from abc import abstractmethod
from typing import Optional, Set

from dagster import OpDefinition, OpExecutionContext, get_dagster_logger, op
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOp
from article._base.ops.save_articles import ArticleDetail
from article._base.resources.alchemy import AlchemyClient, GeneratedQuest
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.id import build_id
from common.utils.s3 import read_dataclass_json_file_s3


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
        required_resource_keys=(required_resource_keys
                                if required_resource_keys is not None else {
                                    str(ResourceKeys.ALCHEMY_CLIENT),
                                    str(ResourceKeys.DUTY_MONGO_CLIENT),
                                }))
    self._config_schema = {"file_uri": str}

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
          file_uri: Detected new file's URI on S3 after scraping event
      """
      file_uri = context.op_config["file_uri"]
      alchemy: AlchemyClient = context.resources.alchemy_client
      article_details: list[ArticleDetail] = []
      article_details = read_dataclass_json_file_s3(ArticleDetail,
                                                    file_uri,
                                                    many=True)
      if not article_details:
        return
      get_dagster_logger().info(article_details)
      for article_detail in article_details:
        quests: list[GeneratedQuest] = alchemy.generate_quests(
            article_detail.content)
        get_dagster_logger().info(quests)
        # TODO: Perform randomly insert logic

    return _op
