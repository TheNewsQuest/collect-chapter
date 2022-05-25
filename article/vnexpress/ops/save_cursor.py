from dataclasses import replace

from dagster import OpDefinition, op

from article._base.ops.scrape_articles import ArticleDetail
from article.vnexpress.resources.cursors import VNExpressArticleCursors
from common.config.categories import VNExpressCategories
from common.config.env import EnvVariables
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key
from common.utils.s3 import read_dataclass_json_file_s3, write_json_file_s3


def save_article_cursor_op_factory(category: VNExpressCategories,
                                   **kwargs) -> OpDefinition:
  """Save article cursor by category

  Args:
      category (VNExpressCategories): VNExpress category

  Returns:
     : _description_
  """
  s3_resource_key = build_resource_key(EnvVariables.VNEXPRESS_PROVIDER_NAME,
                                       ResourceKeys.S3_RESOURCE_PREFIX)

  @op(name=f"save_{category}_article_cursor",
      required_resource_keys={s3_resource_key},
      **kwargs)
  def _op(context, articles: list[ArticleDetail]):
    if len(articles) == 0:
      return  # Skip updating
    latest_cursor: str = articles[0].posted_at
    s3_resource = getattr(context.resources, s3_resource_key)
    uri = f"{s3_resource}/{EnvVariables.ARTICLE_CURSORS_FILENAME}"
    article_cursors_data: VNExpressArticleCursors = read_dataclass_json_file_s3(
        dataclass=VNExpressArticleCursors, uri=uri, many=False)
    # Update/Replace cursor
    params = {f"{category}_cursor": latest_cursor}
    article_cursors_data = replace(article_cursors_data, **params)
    write_json_file_s3(article_cursors_data.to_dict(), uri)

  return _op
