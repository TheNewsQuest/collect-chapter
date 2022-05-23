from dagster import JobDefinition, job

from article.ops.save_article_cursor import save_article_cursor_op_factory
from article.ops.save_articles import save_articles_s3_op_factory
from article.ops.scrape_articles import scrape_articles_op_factory
from article.resources.article_cursors import get_article_cursors
from article.resources.s3_prefix import s3_resource_prefix
from common.enums.categories import VNExpressCategories
from common.enums.resource_keys import ResourceKeys

SCRAPE_RESOURCE_DEFS = {
    str(ResourceKeys.S3_RESOURCE_PREFIX): s3_resource_prefix,
    str(ResourceKeys.ARTICLE_CURSORS): get_article_cursors
}


def scrape_articles_job_factory(category: VNExpressCategories,
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
    articles = scrape_articles_op()  # pylint: disable=no-value-for-parameter
    save_articles_s3_op = save_articles_s3_op_factory(category)
    save_articles_s3_op(articles=articles)  # pylint: disable=no-value-for-parameter
    save_article_cursor_op = save_article_cursor_op_factory(category)
    save_article_cursor_op(articles=articles)  # pylint: disable=no-value-for-parameter

  return _job
