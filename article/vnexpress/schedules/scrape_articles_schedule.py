from dagster import DefaultScheduleStatus, ScheduleDefinition
from strenum import StrEnum

from article._base.schedules.base_schedule import \
    BaseCategorizedScheduleFactory
from article._base.schedules.scrape_articles_schedule import \
    BaseScrapeArticlesSchedule
from article.vnexpress.jobs.scrape_articles import \
    VNExpressScrapeArticlesJobFactory
from common.config import VNExpressCategories
from common.config.env import EnvVariables
from common.config.providers import Providers
from common.errors.key import CategoryKeyError


class VNExpressScrapeArticlesSchedule(BaseScrapeArticlesSchedule):
  """VNExpress Scrape Articles Schedule
  """

  def __init__(
      self,
      category: StrEnum,
      cron_schedule: str,
  ) -> None:
    self._default_status = DefaultScheduleStatus.STOPPED
    super().__init__(
        category=category,
        provider=Providers.VNEXPRESS,
        cron_schedule=cron_schedule,
        default_status=DefaultScheduleStatus.STOPPED,
        scrape_articles_job_factory=VNExpressScrapeArticlesJobFactory(),
        # NOTE: Convert env to str for execution_timezone!
        execution_timezone=str(EnvVariables.SCHEDULE_TIMEZONE))


class VNExpressScrapeArticlesScheduleFactory(BaseCategorizedScheduleFactory):
  """Schedule Factory for creating Scrape Articles schedule for specified category
  """

  def create_schedule(self, category: VNExpressCategories, cron_schedule: str,
                      **kwargs) -> ScheduleDefinition:
    """Creating Save Articles operation based on specified category of VNExpress

    Args:
        category (VNExpressCategories): Enum of VNExpress Categories

    Returns:
        ScheduleDefinition: Dagster's Schedule Definition
    """
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError:
      raise CategoryKeyError(VNExpressCategories) from KeyError
    scrape_articles_schedule = VNExpressScrapeArticlesSchedule(
        category, cron_schedule).build(**kwargs)
    return scrape_articles_schedule
