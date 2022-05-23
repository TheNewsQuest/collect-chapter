from dataclasses import replace

from dagster import OpDefinition, op

from common.dataclasses.article_cursors import ArticleCursors
from common.dataclasses.article_detail import ArticleDetail
from common.enums.categories import VNExpressCategories
from common.enums.env import EnvVariables
from common.enums.resource_keys import ResourceKeys
from common.utils.s3 import read_dataclass_json_file_s3, write_json_file_s3


def save_article_cursor_op_factory(category: VNExpressCategories,
                                   **kwargs) -> OpDefinition:
  """Save article cursor by category

  Args:
      category (VNExpressCategories): VNExpress category

  Returns:
     : _description_
  """

  @op(name=f"save_{category}_article_cursor",
      required_resource_keys={str(ResourceKeys.S3_RESOURCE_PREFIX)},
      **kwargs)
  def _op(context, articles: list[ArticleDetail]):
    if len(articles) == 0:
      return  # Skip updating
    latest_cursor: str = articles[0].posted_at
    uri = f"{context.resources.s3_resource_prefix}/{EnvVariables.ARTICLE_CURSORS_FILENAME}"
    article_cursors_data: ArticleCursors = read_dataclass_json_file_s3(
        dataclass=ArticleCursors, uri=uri, many=False)
    params = {f"{category}_cursor": latest_cursor}
    # Update/Replace cursor
    article_cursors_data = replace(article_cursors_data, **params)
    write_json_file_s3(article_cursors_data.to_dict(), uri)

  return _op
