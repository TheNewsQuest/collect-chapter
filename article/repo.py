# pylint: disable=wrong-import-position
from dotenv import load_dotenv

load_dotenv()

from dagster import RepositoryDefinition, repository

from article.vnexpress.jobs.scrape_articles import \
    VNExpressScrapeArticlesJobFactory
from article.vnexpress.schedules.scrape_articles_schedule import \
    VNExpressScrapeArticlesScheduleFactory
from common.config import VNExpressCategories

SAMPLE_CRON_SCHEDULE = "*/5 * * * *"  # Cron every 5 minutes


@repository
def article_repository() -> RepositoryDefinition:
  """Repository of VNExpress scraping jobs, schedules, sensors.

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules, sensors.
  """
  vnexpress_scrape_articles_job_factory = VNExpressScrapeArticlesJobFactory()
  # Job definitions
  jobs = [
      vnexpress_scrape_articles_job_factory.create_job(category)
      for category in VNExpressCategories
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
  return [*jobs, *schedules]
