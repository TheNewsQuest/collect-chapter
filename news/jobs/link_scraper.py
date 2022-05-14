from dagster import job
from news.ops.scrape_link import scrape_link


@job
def scrape_link_job():
  """Scrape Link from VNExpress job
  """
  scrape_link()  # pylint: disable=no-value-for-parameter
