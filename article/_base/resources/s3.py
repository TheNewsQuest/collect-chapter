from dagster import ResourceDefinition, resource

from common.config import EnvVariables


def build_s3_resource(provider: str, **kwargs) -> ResourceDefinition:
  """Build a S3 Resource prefix based on specified provider

  Args:
      provider (str): Provider

  Returns:
      ResourceDefinition: Dagster's Resource definition
  """

  @resource(**kwargs)
  def _resource() -> str:
    """[Provider]'s S3 Resource prefix of a bucket

    Returns:
        str: S3 Bucket prefix
    """
    return f"{EnvVariables.S3_BUCKET_URI}/{provider}"

  return _resource
