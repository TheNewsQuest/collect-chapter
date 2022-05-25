from dataclasses import dataclass
from typing import Optional

from dagster import get_dagster_logger, resource
from dataclasses_json import DataClassJsonMixin

from common.config.env import EnvVariables
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key
from common.utils.s3 import read_dataclass_json_file_s3, write_json_file_s3


@dataclass
class VNExpressArticleCursors(DataClassJsonMixin):
  """Latest VNExpress articles' cursor by category data
  """
  news_cursor: Optional[str] = None
  business_cursor: Optional[str] = None
  life_cursor: Optional[str] = None
  world_cursor: Optional[str] = None


@resource(
    required_resource_keys={
        build_resource_key(EnvVariables.VNEXPRESS_PROVIDER_NAME,
                           ResourceKeys.S3_RESOURCE_PREFIX)
    })
def get_vnexpress_article_cursors(context) -> VNExpressArticleCursors:
  """Get Article Cursors of all categories in VNExpress

  Args:
      context: Dagster Context object

  Raises:
      err: OSError

  Returns:
      ArticleCursors: Article cursors data
  """
  cursors = VNExpressArticleCursors()
  s3_resource_prefix = getattr(
      context.resources,
      build_resource_key(EnvVariables.VNEXPRESS_PROVIDER_NAME,
                         ResourceKeys.S3_RESOURCE_PREFIX))
  uri = f"{s3_resource_prefix}/{EnvVariables.ARTICLE_CURSORS_FILENAME}"
  try:
    cursors = read_dataclass_json_file_s3(dataclass=VNExpressArticleCursors,
                                          uri=uri,
                                          many=False)
  except OSError as err:
    # pylint: disable=line-too-long
    if str(err).startswith(
        f"""unable to access bucket: '{EnvVariables.S3_BUCKET_NAME}' key: '{EnvVariables.VNEXPRESS_PROVIDER_NAME}/{EnvVariables.ARTICLE_CURSORS_FILENAME}'"""
    ):
      get_dagster_logger().info(
          f"Initializing {uri} as file did not exist in prior.")
      write_json_file_s3(cursors.to_dict(), uri)
    else:
      raise err
  return cursors
