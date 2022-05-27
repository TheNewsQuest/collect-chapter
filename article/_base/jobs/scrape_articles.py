from __future__ import annotations

from typing import Any, Dict, Optional

from dagster import OpDefinition, job
from strenum import StrEnum

from article._base.jobs.base_job import BaseCategorizedJob
from article._base.ops.base_op import BaseCategorizedOpFactory
from article._base.ops.scrape_articles import ArticleDetail
from common.config.providers import Providers
from common.utils.id import build_id


class BaseScrapeArticlesJob(BaseCategorizedJob):
  """Base Scrape Articles job

  Attributes:
      category (StrEnum): Category
      provider (str): Provider name
      resource_defs (Dict[str, Any]): Resource Definitions of Dagster
      scrape_articles_op_factory (BaseCategorizedOpFactory)
      save_articles_op_factory (BaseCategorizedOpFactory)
      save_cursor_op_factory (BaseCategorizedOpFactory)
  """

  def __init__(self,
               category: StrEnum,
               provider: Providers,
               scrape_articles_op_factory: BaseCategorizedOpFactory,
               save_articles_op_factory: BaseCategorizedOpFactory,
               save_cursor_op_factory: BaseCategorizedOpFactory,
               resource_defs: Optional[Dict[str, Any]] = None) -> None:
    super().__init__(category, provider, resource_defs)
    self._scrape_articles_op_factory = scrape_articles_op_factory
    self._save_articles_op_factory = save_articles_op_factory
    self._save_cursor_op_factory = save_cursor_op_factory

  @property
  def scrape_articles_op_factory(self) -> BaseCategorizedOpFactory:
    return self._scrape_articles_op_factory

  @property
  def save_articles_op_factory(self) -> BaseCategorizedOpFactory:
    return self._save_articles_op_factory

  @property
  def save_cursor_op_factory(self) -> BaseCategorizedOpFactory:
    return self._save_cursor_op_factory

  def build(self, **kwargs) -> OpDefinition:
    """Create category-based job for scraping (Protected method)

    Returns:
        JobDefinition: Scraping job on a specific category
    """
    scrape_articles_op = self.scrape_articles_op_factory.create_op(
        self.category)
    save_articles_op = self.save_articles_op_factory.create_op(self.category)
    save_cursor_op = self.save_cursor_op_factory.create_op(self.category)

    @job(name=build_id(provider=self.provider,
                       identifier=f"scrape_{self.category}_articles_job"),
         resource_defs=self.resource_defs,
         **kwargs)
    def _job():
      # pylint: disable=no-value-for-parameter
      articles: list[ArticleDetail] = scrape_articles_op()
      save_articles_op(articles=articles)
      save_cursor_op(articles=articles)

    return _job
