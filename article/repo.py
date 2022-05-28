# pylint: disable=wrong-import-position
import os

from dotenv import load_dotenv

load_dotenv(override=False)

from dagster import RepositoryDefinition, SensorDefinition, repository
from strenum import StrEnum

from article._base.jobs.base_job import BaseCategorizedJobFactory
from article._base.sensors.base_sensor import BaseCategorizedSensorFactory
from article.vnexpress.jobs.save_quests import VNExpressSaveQuestsJobFactory
from article.vnexpress.jobs.scrape_articles import \
    VNExpressScrapeArticlesJobFactory
from article.vnexpress.schedules.scrape_articles_schedule import \
    VNExpressScrapeArticlesScheduleFactory
from article.vnexpress.sensors.save_quests_sensor import \
    VNExpressSaveQuestsSensorFactory
from common.config import VNExpressCategories

SAMPLE_CRON_SCHEDULE = "*/5 * * * *"  # Cron every 5 minutes


def init_categorized_jobs(factory: BaseCategorizedJobFactory,
                          categories: StrEnum) -> list[SensorDefinition]:
  jobs = [factory.create_job(category) for category in categories]
  return jobs


def init_categorized_sensors(factory: BaseCategorizedSensorFactory,
                             categories: StrEnum) -> list[SensorDefinition]:
  sensors = [factory.create_sensor(category) for category in categories]
  return sensors


@repository
def article_repository() -> RepositoryDefinition:
  """Repository of VNExpress scraping jobs, schedules, sensors.

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules, sensors.
  """
  # Job definitions
  jobs = [
      *(init_categorized_jobs(VNExpressScrapeArticlesJobFactory(),
                              VNExpressCategories)),
      *(init_categorized_jobs(VNExpressSaveQuestsJobFactory(),
                              VNExpressCategories)),
  ]
  # Schedule definitions
  vnexpress_scrape_articles_schedule_factory = VNExpressScrapeArticlesScheduleFactory(
  )
  schedules = [
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.NEWS, SAMPLE_CRON_SCHEDULE),
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.BUSINESS, SAMPLE_CRON_SCHEDULE),
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.LIFE, SAMPLE_CRON_SCHEDULE),
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.WORLD, SAMPLE_CRON_SCHEDULE),
  ]
  # Sensor definitions
  sensors = [
      *(init_categorized_sensors(VNExpressSaveQuestsSensorFactory(),
                                 VNExpressCategories))
  ]
  return [*jobs, *schedules, *sensors]
