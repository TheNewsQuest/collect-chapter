from __future__ import annotations

from dagster import get_dagster_logger, resource
from vnexpress.common.dataclasses.latest_articles_dt import \
    LatestArticlesDatetime
from vnexpress.common.enums.env import EnvVariables
from vnexpress.common.utils.s3 import (read_dataclass_json_file_s3,
                                       write_json_file_s3)


@resource(required_resource_keys={"s3_resource_prefix"})
def get_latest_articles_dt(context) -> LatestArticlesDatetime:
  """Get latest articles' datetimes

  Args:
      context: Dagster context

  Returns:
      LatestArticlesDatetime: _description_
  """
  article_dts = LatestArticlesDatetime()
  uri = f"{context.resources.s3_resource_prefix}/{EnvVariables.LATEST_ARTICLES_DT_FILENAME}"
  try:
    article_dts = read_dataclass_json_file_s3(dataclass=LatestArticlesDatetime,
                                              uri=uri,
                                              many=False)
  except OSError as err:
    if str(err).startswith(
        f"""unable to access bucket: '{EnvVariables.S3_BUCKET_NAME}' key: '{EnvVariables.VNEXPRESS_REPO_NAME}/{EnvVariables.LATEST_ARTICLES_DT_FILENAME}'"""
    ):
      write_json_file_s3(article_dts.to_dict(), uri)
      get_dagster_logger().info(
          f"Initializing {uri} as file did not exist in prior...")
    else:
      raise err
  return article_dts
