from dagster import JobDefinition

from article._base.jobs.base_job import BaseCategorizedJobFactory
from article._base.jobs.save_quests import BaseSaveQuestsJob
from article.vnexpress.ops.save_quests import VNExpressSaveQuestsOpFactory
from common.config.categories import VNExpressCategories
from common.config.providers import Providers
from common.errors.key import CategoryKeyError


class VNExpressSaveQuestsJob(BaseSaveQuestsJob):
  """VNExpress Save Quests Job with specified category
  """

  def __init__(
      self,
      category: VNExpressCategories,
  ) -> None:
    super().__init__(
        category=category,
        provider=Providers.VNEXPRESS,
        save_quests_op_factory=VNExpressSaveQuestsOpFactory(),
    )


class VNExpressSaveQuestsJobFactory(BaseCategorizedJobFactory):
  """VNExpress Save Quests Job Factory for category-specified one
  """

  def create_job(self, category: VNExpressCategories,
                 **kwargs) -> JobDefinition:
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError as key_err:
      raise CategoryKeyError(VNExpressCategories) from key_err
    save_quests_job = VNExpressSaveQuestsJob(category).build(**kwargs)
    return save_quests_job
