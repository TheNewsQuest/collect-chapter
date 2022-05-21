from dagster import JobDefinition, job
from vnexpress.enums.categories import VNExpressCategories
from vnexpress.ops.save_articles import save_articles_s3_op_factory
from vnexpress.ops.scrape_articles import scrape_articles_op_factory


def scrape_category_articles_job_factory(category: VNExpressCategories,
                                         **kwargs) -> JobDefinition:
  """Job factory for creating job that scrapes different categories.

  Args:
      category (VNExpressCategories): VNExpress Categories

  Returns:
      JobDefinition: Scrape job by category
  """

  @job(name=f"scrape_{category}_articles_job", **kwargs)
  def _job():
    scrape_articles_op = scrape_articles_op_factory(category)
    articles = scrape_articles_op()
    save_articles_s3_op_factory(category)(articles)

  return _job
