from dagster import JobDefinition, job
from vnexpress.common.enums.categories import VNExpressCategories
from vnexpress.ops.save_articles import save_articles_s3_op_factory
from vnexpress.ops.scrape_articles import scrape_articles_op_factory
from vnexpress.resources.s3 import s3_resource_prefix

SCRAPE_RESOURCE_DEFS = {"s3_resource_prefix": s3_resource_prefix}


def scrape_category_articles_job_factory(category: VNExpressCategories,
                                         **kwargs) -> JobDefinition:
  """Job factory for creating job that scrapes different categories.

  Args:
      category (VNExpressCategories): VNExpress Categories

  Returns:
      JobDefinition: Scrape job by category
  """

  @job(name=f"scrape_{category}_articles_job",
       resource_defs=SCRAPE_RESOURCE_DEFS,
       **kwargs)
  def _job():
    scrape_articles_op = scrape_articles_op_factory(category)
    articles = scrape_articles_op()
    save_articles_s3_op = save_articles_s3_op_factory(category)
    save_articles_s3_op(articles=articles)  # pylint: disable=no-value-for-parameter

  return _job
