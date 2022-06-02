# pylint: disable=wrong-import-position
from dotenv import load_dotenv

load_dotenv(override=False)

from dagster import RepositoryDefinition, SensorDefinition, repository
from strenum import StrEnum

from article._base.jobs.base_job import BaseCategorizedJobFactory
from article._base.sensors.base_sensor import BaseCategorizedSensorFactory
from article.history.jobs.insert_history import InsertHistoryJob
from article.vnexpress.jobs.save_quests import VNExpressSaveQuestsJobFactory
from article.vnexpress.jobs.scrape_articles import \
    VNExpressScrapeArticlesJobFactory
from article.vnexpress.schedules.scrape_articles_schedule import \
    VNExpressScrapeArticlesScheduleFactory
from article.vnexpress.sensors.save_quests_sensor import \
    VNExpressSaveQuestsSensorFactory
from common.config import VNExpressCategories

NEWS_CRON_SCHEDULE = "0 13 * * *"  # Run at 1 P.M Every day
BUSINESS_CRON_SCHEDULE = "0 16 * * *"  # Run at 4 P.M Every day
LIFE_CRON_SCHEDULE = "0 20 * * *"  # Run at 8 P.M Every day
WORLD_CRON_SCHEDULE = "0 23 * * *"  # Run at 11 P.M Every day


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
  # History Job
  insert_history_job = InsertHistoryJob().build()
  # Job definitions
  jobs = [
      *(init_categorized_jobs(VNExpressScrapeArticlesJobFactory(),
                              VNExpressCategories)),
      *(init_categorized_jobs(VNExpressSaveQuestsJobFactory(),
                              VNExpressCategories)), insert_history_job
  ]
  # Schedule definitions
  vnexpress_scrape_articles_schedule_factory = VNExpressScrapeArticlesScheduleFactory(
  )
  schedules = [
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.NEWS, NEWS_CRON_SCHEDULE),
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.BUSINESS, BUSINESS_CRON_SCHEDULE),
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.LIFE, LIFE_CRON_SCHEDULE),
      vnexpress_scrape_articles_schedule_factory.create_schedule(
          VNExpressCategories.WORLD, WORLD_CRON_SCHEDULE),
  ]
  # Sensor definitions
  sensors = [
      *(init_categorized_sensors(VNExpressSaveQuestsSensorFactory(),
                                 VNExpressCategories))
  ]
  return [*jobs, *schedules, *sensors]
