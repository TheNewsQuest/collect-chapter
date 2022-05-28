from typing import Any, Dict, Optional

from dagster import JobDefinition, job
from strenum import StrEnum

from article._base.jobs.base_job import BaseCategorizedJob
from article._base.ops.base_op import BaseCategorizedOpFactory
from article._base.resources.alchemy import get_alchemy_client
from article._base.resources.duty_mongo import get_duty_mongo_client
from article._base.resources.s3 import build_s3_resource
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.id import build_id
from common.utils.resource import build_resource_key


class BaseSaveQuestsJob(BaseCategorizedJob):
  """Base Save Quests job with specify category
  """

  def __init__(self,
               category: StrEnum,
               provider: Providers,
               save_quests_op_factory: BaseCategorizedOpFactory,
               resource_defs: Optional[Dict[str, Any]] = None) -> None:
    super().__init__(
        category,
        provider,
    )
    # NOTE: Specifying resource_defs will override the default init ones
    self._resource_defs = resource_defs if resource_defs is not None else {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI):
            build_s3_resource(self.provider),
        str(ResourceKeys.ALCHEMY_CLIENT):
            get_alchemy_client,
        str(ResourceKeys.DUTY_MONGO_CLIENT):
            get_duty_mongo_client,
    }
    self._save_quests_op_factory = save_quests_op_factory

  @property
  def save_quests_op_factory(self) -> BaseCategorizedOpFactory:
    return self._save_quests_op_factory

  def build(self, **kwargs) -> JobDefinition:

    save_quests_op = self.save_quests_op_factory.create_op(self.category)

    @job(name=build_id(provider=self.provider,
                       identifier=f"save_{self.category}_quests_db_job"),
         resource_defs=self.resource_defs,
         **kwargs)
    def _job():
      save_quests_op()

    return _job
