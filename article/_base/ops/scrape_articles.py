from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Set

from dataclasses_json import DataClassJsonMixin
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOp
from common.config.providers import Providers


@dataclass
class ArticleDetail(DataClassJsonMixin):  # pylint: disable=too-many-instance-attributes
  """Data class for article's detail
  """
  title: str
  thumbnail_url: str
  content: str
  link: str
  author: str
  posted_at: str
  category: str
  subcategory: str


class BaseScrapeArticlesOp(BaseCategorizedOp):
  """Base Categorized Scrape Articles operation

  Attributes:
      category (StrEnum): Category
      provider (Providers): Provider's name
      required_resource_keys (Set[str] | None): Required Resource Keys of Dagster
      scrape_threshold (int): Threshold (Max Page) for scraping activity
      scrape_sleep_time (float): Delay between scrape activities
  """

  def __init__(
      self,
      category: StrEnum,
      provider: Providers,
      scrape_threshold: int,
      scrape_sleep_time: float,
      required_resource_keys: Optional[Set[str]] = None,
  ) -> None:
    super().__init__(category, provider, required_resource_keys)
    self._scrape_threshold = scrape_threshold
    self._scrape_sleep_time = scrape_sleep_time

  @property
  def scrape_threshold(self) -> int:
    return self._scrape_threshold

  @property
  def scrape_sleep_time(self) -> int:
    return self._scrape_sleep_time

  @abstractmethod
  def _scrape_links(self, page_url: str) -> list[str]:
    pass

  @abstractmethod
  def _scrape_article(self, article_url: str) -> ArticleDetail:
    pass
