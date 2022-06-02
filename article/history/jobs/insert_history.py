from dagster import JobDefinition, job

from article._base.jobs.base_job import BaseJob
from article._base.resources.duty_mongo import get_duty_mongo_client
from article._base.resources.s3 import build_s3_resource
from article.history.ops.insert_history import InsertHistoryOps
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.id import build_id
from common.utils.resource import build_resource_key


class InsertHistoryJob(BaseJob):
  """Insert History Job
  """

  def __init__(self) -> None:
    super().__init__(provider=Providers.HISTORY)
    self._resource_defs = {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI):
            build_s3_resource(self.provider),
        str(ResourceKeys.DUTY_MONGO_CLIENT):
            get_duty_mongo_client
    }
    self._insert_history_op = InsertHistoryOps().build()

  def build(self, **kwargs) -> JobDefinition:

    @job(name=build_id(self.provider, "insert_history_job"),
         resource_defs=self.resource_defs,
         **kwargs)
    def _job():
      self._insert_history_op()  # pylint: disable=no-value-for-parameter

    return _job
