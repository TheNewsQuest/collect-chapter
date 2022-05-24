from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set

from dagster import OpDefinition
from dataclasses_json import DataClassJsonMixin
from strenum import StrEnum


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


class BaseScrapeArticlesOp(ABC):
  """Base Scrape Articles Operation

  Args:
      ABC (_type_): _description_
  """

  @abstractmethod
  def __init__(self, category: StrEnum, provider: str,
               required_resource_keys: Set[str]) -> None:
    """Initialize parameters for base Scrape Articles job

    Args:
        category (StrEnum): Category
        provider (str): Provider
        required_resource_keys (Set[str]): Required Resource Keys of Dagster resource
    """
    self._category = category
    self._provider = provider
    self._required_resource_keys = required_resource_keys

  @property
  def category(self) -> str:
    return self._category

  @property
  def provider(self) -> str:
    return self._provider

  @property
  def required_resource_keys(self) -> Set[str]:
    return self._required_resource_keys

  @abstractmethod
  def _scrape_links(self, page_url: str) -> list[str]:
    pass

  @abstractmethod
  def _scrape_article(self, article_url: str) -> ArticleDetail:
    pass

  @abstractmethod
  def build(self, **kwargs) -> OpDefinition:
    pass


class BaseScrapeArticlesOpFactory(ABC):
  """Base class for creating scraping articles operation factory

  Args:
      ABC: Abstract Base Class
  """

  @abstractmethod
  def create_op(self, category: StrEnum, **kwargs) -> OpDefinition:
    pass
