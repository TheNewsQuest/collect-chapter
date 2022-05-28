from dagster import DefaultSensorStatus, SensorDefinition
from strenum import StrEnum

from article._base.sensors.base_sensor import BaseCategorizedSensorFactory
from article._base.sensors.save_quests_sensor import BaseSaveQuestsSensor
from article.vnexpress.jobs.save_quests import VNExpressSaveQuestsJobFactory
from article.vnexpress.ops.save_quests import VNExpressSaveQuestsOpFactory
from common.config.categories import VNExpressCategories
from common.config.env import EnvVariables
from common.config.providers import Providers
from common.errors.key import CategoryKeyError


class VNExpressSaveQuestsSensor(BaseSaveQuestsSensor):
  """VNExpress Save Quests sensor with specified category
  """

  def __init__(
      self,
      category: StrEnum,
  ) -> None:
    super().__init__(
        category=category,
        provider=Providers.VNEXPRESS,
        save_quests_job_factory=VNExpressSaveQuestsJobFactory(),
        save_quests_op_factory=VNExpressSaveQuestsOpFactory(),
        default_status=DefaultSensorStatus.STOPPED
        if EnvVariables.APP_ENV == "local" else DefaultSensorStatus.RUNNING,
        minimum_interval_seconds=60)


class VNExpressSaveQuestsSensorFactory(BaseCategorizedSensorFactory):
  """VNExpress Save Quests Sensor Factory on a specific category
  """

  def create_sensor(self, category: VNExpressCategories,
                    **kwargs) -> SensorDefinition:
    """Create a Save Quests sensor based on specified category

    Args:
        category (VNExpressCategories): VNExpress Category

    Raises:
        CategoryKeyError: Invalid category

    Returns:
        SensorDefinition: Dagster Sensor
    """
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError as key_err:
      raise CategoryKeyError(VNExpressCategories) from key_err
    save_quests_sensor = VNExpressSaveQuestsSensor(category).build(**kwargs)
    return save_quests_sensor
