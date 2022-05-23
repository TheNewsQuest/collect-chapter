from __future__ import annotations

from dagster import get_dagster_logger, resource

from common.dataclasses.article_cursors import ArticleCursors
from common.enums.env import EnvVariables
from common.enums.resource_keys import ResourceKeys
from common.utils.s3 import read_dataclass_json_file_s3, write_json_file_s3


@resource(required_resource_keys={str(ResourceKeys.S3_RESOURCE_PREFIX)})
def get_article_cursors(context) -> ArticleCursors:
  """Get Article Cursors of all categories

  Args:
      context (_type_): Dagster Context object

  Raises:
      err: OSError

  Returns:
      ArticleCursors: Article cursors data
  """
  cursors = ArticleCursors()
  uri = f"{context.resources.s3_resource_prefix}/{EnvVariables.ARTICLE_CURSORS_FILENAME}"
  try:
    cursors = read_dataclass_json_file_s3(dataclass=ArticleCursors,
                                          uri=uri,
                                          many=False)
  except OSError as err:
    # pylint: disable=line-too-long
    if str(err).startswith(
        f"""unable to access bucket: '{EnvVariables.S3_BUCKET_NAME}' key: '{EnvVariables.VNEXPRESS_REPO_NAME}/{EnvVariables.ARTICLE_CURSORS_FILENAME}'"""
    ):
      get_dagster_logger().info(
          f"Initializing {uri} as file did not exist in prior...")
      write_json_file_s3(cursors.to_dict(), uri)
    else:
      raise err
  return cursors
