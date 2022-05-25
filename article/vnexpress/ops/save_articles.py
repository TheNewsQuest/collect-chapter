from __future__ import annotations

from dagster import In, OpDefinition, get_dagster_logger, op
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOpFactory
from article._base.ops.save_articles import BaseSaveArticlesOp
from article._base.ops.scrape_articles import ArticleDetail
from common.config import EnvVariables
from common.config.categories import VNExpressCategories
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils import build_resource_key
from common.utils.provider import build_id
from common.utils.s3 import write_json_file_s3


class VNExpressSaveArticlesOp(BaseSaveArticlesOp):
  """VNExpress Save Articles Operation

  Args:
      BaseSaveArticlesOp: Base Save Article Operation class
  """

  def __init__(
      self,
      category: StrEnum,
  ) -> None:
    super().__init__(category=category, provider=Providers.VNEXPRESS)
    self.required_resource_keys = {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_PREFIX)
    }

  def build(self, **kwargs) -> OpDefinition:
    """Build Save Articles operation for specified category

    Args:
        category (str): VNExpress Category

    Returns:
        OpDefinition: Save to S3 Operation
    """

    @op(name=build_id(provider=self.provider,
                      identifier=f"save_{self.category}_articles_s3_op"),
        required_resource_keys=self.required_resource_keys,
        ins={"articles": In(dagster_type=list[ArticleDetail])},
        **kwargs)
    def _op(context, articles: list[ArticleDetail]):
      """Save list of articles to S3 bucket operation

      Args:
          context: Dagster context object
          articles (list[ArticleDetail]): List of article details
      """
      file_uri = self._build_file_uri(context)
      article_details = ArticleDetail.schema().dump(articles, many=True)
      write_json_file_s3(article_details, file_uri)
      get_dagster_logger().info(f"Save {file_uri} successfully.")

    return _op


class VNExpressSaveArticlesOpFactory(BaseCategorizedOpFactory):
  """Op Factory for creating Save Articles Op for specified category

  Args:
      BaseCategorizedOpFactory: Base Categorized Op Factory
  """

  def create_op(self, category: VNExpressCategories, **kwargs) -> OpDefinition:
    """Creating Save Articles operation based on specified category of VNExpress

    Args:
        category (StrEnum): Enum of Category

    Returns:
        OpDefinition: Dagster's Op Definition
    """
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError:
      get_dagster_logger().error(
          "Specified category does not exist in operation factory.")
      return None
    save_articles_op = VNExpressSaveArticlesOp(category).build(**kwargs)
    return save_articles_op
