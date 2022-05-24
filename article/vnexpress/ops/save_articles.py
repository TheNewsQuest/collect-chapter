from datetime import datetime

import pytz
from dagster import OpDefinition, get_dagster_logger, op

from article._base.ops.scrape_articles import ArticleDetail
from common.config.date_formats import DateFormats
from common.config.resource_keys import ResourceKeys
from common.utils.s3 import write_json_file_s3

# TODO: Change Save Articles function factory to OOP Factory!!!


def save_articles_s3_op_factory(category: str, **kwargs) -> OpDefinition:
  """Factory to create save articles operation for specified category to S3

  Args:
      category (str): VNExpress Category

  Returns:
      OpDefinition: Save to S3 Operation
  """

  @op(name=f"save_{category}_articles_s3_op",
      required_resource_keys={str(ResourceKeys.S3_RESOURCE_PREFIX)},
      **kwargs)
  def _op(context, articles: list[ArticleDetail]) -> None:
    """Save list of articles to S3 bucket operation

    Args:
        context: Dagster context object
        articles (list[ArticleDetail]): List of article details
    """
    today_datestr = datetime.now(tz=pytz.utc).strftime(DateFormats.YYYYMMDD)
    json_file_uri = f"{context.resources.s3_resource_prefix}/{category}/{today_datestr}.json"
    article_obj_list = ArticleDetail.schema().dump(articles, many=True)
    write_json_file_s3(article_obj_list, json_file_uri)
    get_dagster_logger().info(f"Save {json_file_uri} successfully.")

  return _op
