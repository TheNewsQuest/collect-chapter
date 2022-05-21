# pylint: disable=wrong-import-position
from dotenv import load_dotenv

# Load dotenv file configs
load_dotenv()

from dagster import RepositoryDefinition, repository

from vnexpress.common.enums.categories import VNExpressCategories
from vnexpress.jobs.scrape import scrape_category_articles_job_factory


@repository
def vnexpress_repository() -> RepositoryDefinition:
  """Repository of VNExpress scraping jobs, schedules

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules, sensors.
  """
  scrape_news = scrape_category_articles_job_factory(VNExpressCategories.NEWS)
  scrape_business = scrape_category_articles_job_factory(
      VNExpressCategories.BUSINESS)
  scrape_life = scrape_category_articles_job_factory(VNExpressCategories.LIFE)
  return [scrape_news, scrape_business, scrape_life]
