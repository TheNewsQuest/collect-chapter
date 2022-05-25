from typing import Optional

from dagster import (DefaultScheduleStatus, RunRequest, ScheduleDefinition,
                     get_dagster_logger, schedule)
from strenum import StrEnum

from article._base.jobs.base_job import BaseCategorizedJobFactory
from article._base.schedules.base_schedule import BaseCategorizedSchedule
from common.config.date_formats import DateFormats
from common.config.providers import Providers
from common.utils.date import format_datetime_str
from common.utils.id import build_id


class BaseScrapeArticlesSchedule(BaseCategorizedSchedule):
  """Base Scrape Articles Schedule

  """

  def __init__(self,
               category: StrEnum,
               provider: Providers,
               cron_schedule: str,
               default_status: DefaultScheduleStatus,
               scrape_articles_job_factory: BaseCategorizedJobFactory,
               execution_timezone: Optional[str] = None) -> None:
    self._category = category
    self._scrape_articles_job_factory = scrape_articles_job_factory
    self._job = self.scrape_articles_job_factory.create_job(self.category)
    super().__init__(category=self.category,
                     provider=provider,
                     cron_schedule=cron_schedule,
                     job=self.job,
                     default_status=default_status,
                     execution_timezone=execution_timezone)

  @property
  def scrape_articles_job_factory(self) -> BaseCategorizedJobFactory:
    return self._scrape_articles_job_factory

  def build(self, **kwargs) -> ScheduleDefinition:
    """Build a Schedule for Scraping Articles

    Returns:
        ScheduleDefinition: Dagster's Schedule Definition
    """

    @schedule(name=build_id(self.provider,
                            f"scrape_{self.category}_articles_schedule"),
              cron_schedule=self.cron_schedule,
              job=self.job,
              execution_timezone=self.execution_timezone,
              default_status=self.default_status,
              **kwargs)
    def _schedule(context) -> RunRequest:
      scheduled_date = format_datetime_str(context.scheduled_execution_time,
                                           DateFormats.YYYYMMDD)
      get_dagster_logger().info(
          f"Trigger schedule of scraping {self.category} articles on VNExpress at {scheduled_date}."
      )
      return RunRequest(run_key=None, tags={"date": scheduled_date})

    return _schedule
