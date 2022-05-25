from abc import ABC, abstractmethod
from typing import Optional

from dagster import DefaultScheduleStatus, JobDefinition, ScheduleDefinition
from strenum import StrEnum

from common.config.providers import Providers


class BaseSchedule(ABC):
  """Base Schedule of Dagster

  """

  @abstractmethod
  def __init__(self,
               provider: Providers,
               cron_schedule: str,
               job: JobDefinition,
               default_status: DefaultScheduleStatus,
               execution_timezone: Optional[str] = None) -> None:
    self._provider = provider
    self._cron_schedule = cron_schedule
    self._job = job
    self._default_status = default_status
    self._execution_timezone = execution_timezone

  @property
  def provider(self) -> str:
    return self._provider

  @property
  def cron_schedule(self) -> str:
    return self._cron_schedule

  @property
  def job(self) -> JobDefinition:
    return self._job

  @property
  def default_status(self) -> DefaultScheduleStatus:
    return self._default_status

  @property
  def execution_timezone(self) -> Optional[str]:
    return self._execution_timezone

  @abstractmethod
  def build(self, **kwargs) -> ScheduleDefinition:
    pass


class BaseCategorizedSchedule(BaseSchedule):
  """Base Categorized Schedule
  """

  def __init__(self,
               category: StrEnum,
               provider: Providers,
               cron_schedule: str,
               job: JobDefinition,
               default_status: DefaultScheduleStatus,
               execution_timezone: Optional[str] = None) -> None:
    self._category = category
    super().__init__(provider, cron_schedule, job, default_status,
                     execution_timezone)

  @property
  def category(self) -> str:
    return self._category


class BaseCategorizedScheduleFactory(ABC):
  """Base factory class for creating schedule correlated with category
  """

  @abstractmethod
  def create_schedule(self, category: StrEnum, cron_schedule: str,
                      **kwargs) -> ScheduleDefinition:
    pass
