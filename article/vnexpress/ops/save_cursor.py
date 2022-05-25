from dataclasses import replace

from dagster import In, OpDefinition, op
from strenum import StrEnum

from article._base.ops import ArticleDetail, BaseSaveCursorOp
from article._base.ops.base_op import BaseCategorizedOpFactory
from article.vnexpress.resources.cursors import VNExpressArticleCursors
from common.config import EnvVariables, ResourceKeys, VNExpressCategories
from common.errors.key import CategoryKeyError
from common.utils.resource import build_resource_key
from common.utils.s3 import read_dataclass_json_file_s3, write_json_file_s3


class VNExpressSaveCursorOp(BaseSaveCursorOp):
  """VNExpress Save Cursor Operation

  Args:
      BaseSaveCursorOp: Base Save Cursor Operation
  """

  def __init__(self, category: StrEnum) -> None:
    super().__init__(category=category,
                     provider=EnvVariables.VNEXPRESS_PROVIDER_NAME)
    self._required_resource_keys = {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_PREFIX)
    }

  def build(self, **kwargs) -> OpDefinition:
    """Save article cursor by category

    Args:
        category (VNExpressCategories): VNExpress category

    Returns:
      OpDefinition: Dagster's Op Definition
    """

    @op(name=f"save_{self.category}_article_cursor",
        required_resource_keys=self.required_resource_keys,
        ins={"articles": In(dagster_type=list[ArticleDetail])},
        **kwargs)
    def _op(context, articles: list[ArticleDetail]):
      """Save article cursor of a specific category

      Args:
          context: Dagster's Context
          articles (list[ArticleDetail]): List of scraped article's detail
      """
      if len(articles) == 0:
        return  # Skip updating
      latest_cursor: str = articles[0].posted_at
      uri = self._build_file_uri(context)
      article_cursors_data: VNExpressArticleCursors = read_dataclass_json_file_s3(
          dataclass=VNExpressArticleCursors, uri=uri, many=False)
      # Update/Replace cursor
      params = {f"{self.category}_cursor": latest_cursor}
      article_cursors_data = replace(article_cursors_data, **params)
      write_json_file_s3(article_cursors_data.to_dict(), uri)

    return _op


class VNExpressSaveCursorOpFactory(BaseCategorizedOpFactory):
  """Op Factory for creating Save Cursor Op of specified category

  Args:
      BaseCategorizedOpFactory: Base Categorized Op Factory
  """

  def create_op(self, category: VNExpressCategories, **kwargs) -> OpDefinition:
    """Creating Save Cursor operation based on specified category

    Args:
        category (VNExpressCategories): Enum of VNExpress category

    Returns:
        OpDefinition: Dagster's Op Definition
    """
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError as key_err:
      raise CategoryKeyError(list(VNExpressCategories)) from key_err
    save_cursor_op = VNExpressSaveCursorOp(category).build(**kwargs)
    return save_cursor_op
