from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional

from dagster import DefaultSensorStatus, JobDefinition, SensorDefinition
from strenum import StrEnum

from common.config.providers import Providers


class BaseSensor(ABC):
  """Base Dagster Sensor abstract class
  """

  def __init__(self,
               provider: Providers,
               job: JobDefinition,
               default_status: DefaultSensorStatus,
               minimum_interval_seconds: int,
               run_config: Optional[Mapping[str, Any]] = None) -> None:
    self._provider = provider
    self._job = job
    self._default_status = default_status
    self._minimum_interval_seconds = minimum_interval_seconds
    self._run_config = run_config

  @property
  def provider(self) -> Providers:
    return self._provider

  @property
  def job(self) -> JobDefinition:
    return self._job

  @property
  def default_status(self) -> DefaultSensorStatus:
    return self._default_status

  @property
  def minimum_interval_seconds(self) -> int:
    return self._minimum_interval_seconds

  @property
  def run_config(self) -> Optional[Mapping[str, Any]]:
    return self._run_config

  @abstractmethod
  def build(self, **kwargs) -> SensorDefinition:
    pass


class BaseCategorizedSensor(BaseSensor):
  """Base Categorized Sensor
  """

  def __init__(self,
               category: StrEnum,
               provider: Providers,
               job: JobDefinition,
               default_status: DefaultSensorStatus,
               minimum_interval_seconds: int,
               run_config: Optional[Mapping[str, Any]] = None) -> None:
    self._category = category
    super().__init__(provider, job, default_status, minimum_interval_seconds,
                     run_config)

  @property
  def category(self) -> StrEnum:
    return self._category


class BaseCategorizedSensorFactory(ABC):
  """Base factory class for creating sensor correlated with category
  """

  @abstractmethod
  def create_sensor(self, category: StrEnum, **kwargs) -> SensorDefinition:
    pass
