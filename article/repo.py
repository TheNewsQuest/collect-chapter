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
      vnexpress_scrape_articles_job_factory.create_job(
          VNExpressCategories.NEWS),
      vnexpress_scrape_articles_job_factory.create_job(
          VNExpressCategories.BUSINESS),
      vnexpress_scrape_articles_job_factory.create_job(VNExpressCategories.LIFE)
  ]
  # Schedules
  schedules = [
      scrape_articles_schedule_factory(VNExpressCategories.NEWS),
      scrape_articles_schedule_factory(VNExpressCategories.BUSINESS),
      scrape_articles_schedule_factory(VNExpressCategories.LIFE),
  ]
  return [*jobs, *schedules]
