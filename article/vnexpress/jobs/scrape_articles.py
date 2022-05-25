from dagster import JobDefinition, OpDefinition, job

from article._base.jobs import BaseScrapeArticlesJobFactory
from article._base.jobs.scrape_articles import BaseScrapeArticlesJob
from article._base.ops.scrape_articles import ArticleDetail
from article._base.resources.s3 import build_s3_resource
from article.vnexpress.ops.save_articles import VNExpressSaveArticlesOpFactory
from article.vnexpress.ops.save_cursor import VNExpressSaveCursorOpFactory
from article.vnexpress.ops.scrape_articles import \
    VNExpressScrapeArticlesOpFactory
from article.vnexpress.resources.cursors import get_vnexpress_article_cursors
from common.config import EnvVariables, ResourceKeys
from common.config.categories import VNExpressCategories
from common.errors.key import CategoryKeyError
from common.utils.provider import build_id
from common.utils.resource import build_resource_key


class VNExpressScrapeArticlesJob(BaseScrapeArticlesJob):
  """VNExpress Scrape Articles job

  Args:
      BaseScrapeArticlesJob: _description_
  """

  def __init__(self, category: str) -> None:
    super().__init__(
        category=category,
        provider=EnvVariables.VNEXPRESS_PROVIDER_NAME,
    )
    self.resource_defs = {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_PREFIX):
            build_s3_resource(EnvVariables.VNEXPRESS_PROVIDER_NAME),
        build_resource_key(self.provider, ResourceKeys.ARTICLE_CURSORS):
            get_vnexpress_article_cursors
    }

  def build(self, **kwargs) -> OpDefinition:
    """Create category-based job for scraping (Protected method)

    Returns:
        JobDefinition: Scraping job on a specific category
    """
    # Init factories
    scrape_articles_op_factory = VNExpressScrapeArticlesOpFactory()
    save_articles_op_factory = VNExpressSaveArticlesOpFactory()
    save_cursor_op_factory = VNExpressSaveCursorOpFactory()

    @job(name=build_id(provider=self.provider,
                       identifier=f"scrape_{self.category}_articles_job"),
         resource_defs=self.resource_defs,
         **kwargs)
    def _job():
      scrape_articles_op = scrape_articles_op_factory.create_op(self.category)
      articles: list[ArticleDetail] = scrape_articles_op()  # pylint: disable=no-value-for-parameter
      save_articles_op = save_articles_op_factory.create_op(self.category)
      save_articles_op(articles=articles)  # pylint: disable=no-value-for-parameter
      save_cursor_op = save_cursor_op_factory.create_op(self.category)
      save_cursor_op(articles=articles)  # pylint: disable=no-value-for-parameter

    return _job


class VNExpressScrapeArticlesJobFactory(BaseScrapeArticlesJobFactory):
  """Scrape Articles Job Factory for VNExpress provider
  """

  def create_job(self, category: VNExpressCategories,
                 **kwargs) -> JobDefinition:
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError as key_err:
      raise CategoryKeyError(list(VNExpressCategories)) from key_err
    scrape_job = VNExpressScrapeArticlesJob(category).build(**kwargs)
    return scrape_job
