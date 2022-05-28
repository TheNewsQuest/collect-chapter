from dagster import OpDefinition
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOpFactory
from article._base.ops.save_quests import BaseSaveQuestsOp
from common.config.categories import VNExpressCategories
from common.config.providers import Providers
from common.errors.key import CategoryKeyError


class VNExpressSaveQuestsOp(BaseSaveQuestsOp):
  """Save Quests operation for VNExpress
  """

  def __init__(
      self,
      category: StrEnum,
  ) -> None:
    super().__init__(category=category, provider=Providers.VNEXPRESS)


class VNExpressSaveQuestsOpFactory(BaseCategorizedOpFactory):
  """VNExpress Save Quests categorized Op Factory
  """

  def create_op(self, category: VNExpressCategories, **kwargs) -> OpDefinition:
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError as key_err:
      raise CategoryKeyError(VNExpressCategories) from key_err
    save_quests_op = VNExpressSaveQuestsOp(category).build(**kwargs)
    return save_quests_op
