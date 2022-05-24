# pylint: disable=wrong-import-position
from dotenv import load_dotenv

load_dotenv()

from dagster import RepositoryDefinition, repository

from article.vnexpress.jobs.scrape_articles import \
    VNExpressScrapeArticlesJobFactory
from article.vnexpress.schedules.scrape_articles_schedule import \
    scrape_articles_schedule_factory
from common.config import VNExpressCategories


@repository
def article_repository() -> RepositoryDefinition:
  """Repository of VNExpress scraping jobs, schedules

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules, sensors.
  """
  vnexpress_scrape_articles_job_factory = VNExpressScrapeArticlesJobFactory()
  # Jobs
  jobs = [
      vnexpress_scrape_articles_job_factory.create_job(category)
      for category in VNExpressCategories
  ]
  # Schedules
  schedules = [
      scrape_articles_schedule_factory(category)
      for category in VNExpressCategories
  ]
  return [*jobs, *schedules]
