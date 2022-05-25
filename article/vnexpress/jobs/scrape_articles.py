from dagster import JobDefinition

from article._base.jobs.base_job import BaseCategorizedJobFactory
from article._base.jobs.scrape_articles import BaseScrapeArticlesJob
from article.vnexpress.ops.save_articles import VNExpressSaveArticlesOpFactory
from article.vnexpress.ops.save_cursor import VNExpressSaveCursorOpFactory
from article.vnexpress.ops.scrape_articles import \
    VNExpressScrapeArticlesOpFactory
from article.vnexpress.resources.cursors import (
    vnexpress_article_cursors_key, vnexpress_article_cursors_resource)
from article.vnexpress.resources.s3 import (vnexpress_s3_resource,
                                            vnexpress_s3_resource_key)
from common.config.categories import VNExpressCategories
from common.config.providers import Providers
from common.errors.key import CategoryKeyError


class VNExpressScrapeArticlesJob(BaseScrapeArticlesJob):
  """VNExpress Scrape Articles job

  Args:
      BaseScrapeArticlesJob: _description_
  """

  def __init__(self, category: str) -> None:
    super().__init__(
        category=category,
        provider=Providers.VNEXPRESS,
        scrape_articles_op_factory=VNExpressScrapeArticlesOpFactory(),
        save_articles_op_factory=VNExpressSaveArticlesOpFactory(),
        save_cursor_op_factory=VNExpressSaveCursorOpFactory())
    self.resource_defs = {
        vnexpress_s3_resource_key: vnexpress_s3_resource,
        vnexpress_article_cursors_key: vnexpress_article_cursors_resource
    }


class VNExpressScrapeArticlesJobFactory(BaseCategorizedJobFactory):
  """Scrape Articles Job Factory for VNExpress provider
  """

  def create_job(self, category: VNExpressCategories,
                 **kwargs) -> JobDefinition:
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError as key_err:
      raise CategoryKeyError(VNExpressCategories) from key_err
    scrape_job = VNExpressScrapeArticlesJob(category).build(**kwargs)
    return scrape_job
