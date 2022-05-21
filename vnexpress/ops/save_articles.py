from datetime import datetime

import pytz
from dagster import OpDefinition, get_dagster_logger, op
from vnexpress.dataclasses.article_detail import ArticleDetail
from vnexpress.enums.date_format import DateFormats
from vnexpress.enums.env import EnvVariables
from vnexpress.utils.s3 import write_file_s3


def save_articles_s3_op_factory(category: str, **kwargs) -> OpDefinition:
  """Factory to create save articles operation for specified category to S3

  Args:
      category (str): VNExpress Category

  Returns:
      OpDefinition: Save to S3 Operation
  """

  @op(name=f"save_{category}_articles_s3_op", **kwargs)
  def _op(articles: list[ArticleDetail]) -> None:
    today = datetime.now(tz=pytz.utc)
    today_datestr = today.strftime(DateFormats.YYYYMMDD)
    json_file_uri = f"{EnvVariables.S3_BUCKET_URI}/{category}/{today_datestr}.json"
    json_articles_str = ArticleDetail.schema().dumps(articles, many=True)
    get_dagster_logger().debug(json_articles_str)
    write_file_s3(json_articles_str, json_file_uri)
    get_dagster_logger().info(f"Save {json_file_uri} successfully.")

  return _op
