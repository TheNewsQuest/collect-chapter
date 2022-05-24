from dagster import JobDefinition, OpDefinition, get_dagster_logger, job
from strenum import StrEnum

from article._base.jobs import BaseScrapeArticlesJobFactory
from article._base.jobs.scrape_articles import BaseScrapeArticlesJob
from article.vnexpress.ops.save_article_cursor import \
    save_article_cursor_op_factory
from article.vnexpress.ops.save_articles import save_articles_s3_op_factory
from article.vnexpress.ops.scrape_articles import \
    VNExpressScrapeArticlesOpFactory
from article.vnexpress.resources.article_cursors import get_article_cursors
from article.vnexpress.resources.s3_prefix import s3_resource_prefix
from common.config import EnvVariables, ResourceKeys
from common.config.categories import VNExpressCategories
from common.utils.provider import build_provider_id


class VNExpressScrapeArticlesJob(BaseScrapeArticlesJob):
  """VNExpress Scrape Articles job

  Args:
      BaseScrapeArticlesJob: _description_
  """

  def __init__(self, category: str) -> None:
    super().__init__(
        category=category,
        provider=EnvVariables.VNEXPRESS_PROVIDER_NAME,
        resource_defs={
            str(ResourceKeys.S3_RESOURCE_PREFIX): s3_resource_prefix,
            str(ResourceKeys.ARTICLE_CURSORS): get_article_cursors
        })

  def build(self, **kwargs) -> OpDefinition:
    """Create category-based job for scraping (Protected method)

    Returns:
        JobDefinition: Scraping job on a specific category
    """
    # Init factories
    scrape_articles_op_factory = VNExpressScrapeArticlesOpFactory()

    @job(name=build_provider_id(
        provider=self.provider,
        identifier=f"scrape_{self.category}_articles_job"),
         resource_defs=self.resource_defs,
         **kwargs)
    def _job():
      scrape_articles_op = scrape_articles_op_factory.create_op(self.category)
      articles = scrape_articles_op()  # pylint: disable=no-value-for-parameter
      save_articles_s3_op = save_articles_s3_op_factory(self.category)
      save_articles_s3_op(articles=articles)  # pylint: disable=no-value-for-parameter
      save_article_cursor_op = save_article_cursor_op_factory(self.category)
      save_article_cursor_op(articles=articles)  # pylint: disable=no-value-for-parameter

    return _job


class VNExpressScrapeArticlesJobFactory(BaseScrapeArticlesJobFactory):
  """Scrape Articles Job Factory for VNExpress provider
  """

  def create_job(self, category: StrEnum, **kwargs) -> JobDefinition:
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError:
      get_dagster_logger().error(
          "Specified category does not exist in job factory.")
      return None
    scrape_job = VNExpressScrapeArticlesJob(category).build(**kwargs)
    return scrape_job
