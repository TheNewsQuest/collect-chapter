from strenum import StrEnum  # pylint: disable=invalid-name


class ResourceKeys(StrEnum):
  """List of Resource Keys of Dagster
  """
  ARTICLE_CURSORS = "article_cursors"
  S3_RESOURCE_URI = "s3_resource_uri"
  ALCHEMY_CLIENT = "alchemy_client"
  DUTY_MONGO_CLIENT = "duty_mongo_client"
