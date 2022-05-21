from dagster import repository
from dotenv import load_dotenv

from vnexpress.enums.categories import VNExpressCategories
from vnexpress.jobs.scrape import scrape_category_articles_job_factory

load_dotenv()


@repository
def vnexpress_repository():
  """Repository of VNExpress scraping jobs, schedules

  Returns:
      RepositoryDefinition: Repository containing all jobs, schedules
  """
  scrape_news = scrape_category_articles_job_factory(VNExpressCategories.NEWS)
  scrape_business = scrape_category_articles_job_factory(
      VNExpressCategories.BUSINESS)
  scrape_life = scrape_category_articles_job_factory(VNExpressCategories.LIFE)
  return [scrape_news, scrape_business, scrape_life]
