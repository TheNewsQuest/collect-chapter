from dagster import job
from vnexpress.constants.prefix import VNEXPRESS_PREFIX
from vnexpress.enums.categories import VNExpressCategories
from vnexpress.ops.scrape_articles import \
    scrape_articles_by_category_op_factory


@job(name=f"scrape_news_{VNEXPRESS_PREFIX}")
def scrape_news():
  """Job for scraping news articles
  """
  scrape_articles_by_category_op_factory(VNExpressCategories.NEWS)()


@job(name=f"scrape_business_{VNEXPRESS_PREFIX}")
def scrape_business():
  """Job for scraping business articles
  """
  scrape_articles_by_category_op_factory(VNExpressCategories.BUSINESS)()


@job(name=f"scrape_life_{VNEXPRESS_PREFIX}")
def scrape_life():
  """Job for scraping life articles
  """
  scrape_articles_by_category_op_factory(VNExpressCategories.LIFE)()
