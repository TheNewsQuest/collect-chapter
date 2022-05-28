from dagster import get_dagster_logger, resource
from dataclasses_json import DataClassJsonMixin

from common.config.env import EnvVariables
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key
from common.utils.s3 import read_dataclass_json_file_s3, write_json_file_s3


def build_article_cursors_resource(provider: str,
                                   dataclass_: DataClassJsonMixin, **kwargs):

  s3_resource_key = build_resource_key(provider, ResourceKeys.S3_RESOURCE_URI)

  @resource(required_resource_keys={s3_resource_key}, **kwargs)
  def _resource(context) -> DataClassJsonMixin:
    """Get Article Cursors of all categories

    Args:
        context: Dagster Context object

    Raises:
        err: OSError

    Returns:
        ArticleCursors: Article cursors data
    """
    cursors = dataclass_()
    s3_resource = getattr(context.resources, s3_resource_key)
    uri = f"{s3_resource}/{EnvVariables.ARTICLE_CURSORS_FILENAME}"
    try:
      cursors = read_dataclass_json_file_s3(dataclass_, uri, False)
    except OSError as err:
      # pylint: disable=line-too-long
      if str(err).startswith(
          f"""unable to access bucket: '{EnvVariables.S3_BUCKET_NAME}' key: '{provider}/{EnvVariables.ARTICLE_CURSORS_FILENAME}'"""
      ):
        get_dagster_logger().info(
            f"Initializing {uri} as file did not exist in prior.")
        write_json_file_s3(cursors.to_dict(), uri)
      else:
        raise err
    return cursors

  return _resource
