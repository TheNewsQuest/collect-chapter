# pylint: disable=wrong-import-position
from dotenv import load_dotenv

load_dotenv()

from dagster import RepositoryDefinition, repository

from article.jobs.scrape import scrape_articles_job_factory
from article.schedules.scrape_articles_schedule import \
    scrape_articles_schedule_factory
from common.enums import VNExpressCategories


@repository
def article_repository() -> RepositoryDefinition:
  """Repository of VNExpress scraping jobs, schedules

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules, sensors.
  """
  # Jobs
  jobs = [
      scrape_articles_job_factory(VNExpressCategories.NEWS),
      scrape_articles_job_factory(VNExpressCategories.BUSINESS),
      scrape_articles_job_factory(VNExpressCategories.LIFE)
  ]
  # Schedules
  schedules = [
      scrape_articles_schedule_factory(VNExpressCategories.NEWS),
      scrape_articles_schedule_factory(VNExpressCategories.BUSINESS),
      scrape_articles_schedule_factory(VNExpressCategories.LIFE),
  ]
  return [*jobs, *schedules]
