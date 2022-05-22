from dagster import resource
from vnexpress.common.enums.env import EnvVariables


@resource
def s3_resource_prefix() -> str:
  """S3 Resource prefix of a bucket

  Returns:
      str: Prefix
  """
  return f"{EnvVariables.S3_BUCKET_URI}/{EnvVariables.VNEXPRESS_REPO_NAME}"
