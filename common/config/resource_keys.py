from strenum import StrEnum  # pylint: disable=invalid-name


class ResourceKeys(StrEnum):
  """List of Resource Keys of Dagster
  """
  ARTICLE_CURSORS = "article_cursors"
  S3_RESOURCE_PREFIX = "s3_resource_prefix"