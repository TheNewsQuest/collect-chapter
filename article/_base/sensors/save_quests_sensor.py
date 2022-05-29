from dagster import (DefaultSensorStatus, OpDefinition, RunRequest,
                     SensorDefinition, SensorEvaluationContext, SkipReason,
                     get_dagster_logger, sensor)
from dagster_aws.s3.sensor import get_s3_keys
from strenum import StrEnum

from article._base.jobs.base_job import BaseCategorizedJobFactory
from article._base.ops.base_op import BaseCategorizedOpFactory
from article._base.sensors.base_sensor import BaseCategorizedSensor
from common.config.env import EnvVariables
from common.config.providers import Providers
from common.utils.id import build_id


class BaseSaveQuestsSensor(BaseCategorizedSensor):
  """Base Save Quests sensor
  """

  def __init__(
      self,
      category: StrEnum,
      provider: Providers,
      save_quests_job_factory: BaseCategorizedJobFactory,
      save_quests_op_factory: BaseCategorizedOpFactory,
      default_status: DefaultSensorStatus,
      minimum_interval_seconds: int,
  ) -> None:
    self._save_quests_op_factory = save_quests_op_factory
    self._save_quests_job_factory = save_quests_job_factory
    self._save_quests_op = save_quests_op_factory.create_op(category)
    self._job = self._save_quests_job_factory.create_job(category)
    super().__init__(category, provider, self._job, default_status,
                     minimum_interval_seconds)

  @property
  def save_quests_op_factory(self) -> BaseCategorizedOpFactory:
    return self._save_quests_op_factory

  @property
  def save_quests_op(self) -> OpDefinition:
    return self._save_quests_op

  @property
  def save_quests_job_factory(self) -> BaseCategorizedJobFactory:
    return self._save_quests_job_factory

  def build(self, **kwargs) -> SensorDefinition:

    @sensor(name=build_id(self.provider,
                          f"save_{self.category}_quests_db_sensor"),
            job=self.job,
            default_status=self.default_status,
            minimum_interval_seconds=self.minimum_interval_seconds,
            **kwargs)
    def _sensor(context: SensorEvaluationContext):
      bucket_name = EnvVariables.S3_BUCKET_NAME
      prefix = f"{self.provider}/{self.category}"
      new_s3_keys = get_s3_keys(bucket=bucket_name,
                                prefix=prefix,
                                since_key=context.last_run_key)
      # Handle skip
      if not new_s3_keys:
        yield SkipReason(
            f"There are no new files created in bucket {bucket_name} at prefix {prefix}"
        )
      for s3_key in new_s3_keys:
        get_dagster_logger().info(f"New s3_key: {s3_key}")
        get_dagster_logger().info(self.job)
        s3_filename = s3_key.split('/')[-1]
        yield RunRequest(run_key=s3_key,
                         run_config={
                             "ops": {
                                 self.save_quests_op.name: {
                                     "config": {
                                         "filename": s3_filename
                                     }
                                 }
                             }
                         })

    return _sensor
