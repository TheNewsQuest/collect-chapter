from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Set

from dataclasses_json import DataClassJsonMixin
from strenum import StrEnum

from article._base.ops.base_op import BaseOp


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


class BaseScrapeArticlesOp(BaseOp):
  """Base  Operation

  Args:
      ABC (_type_): _description_
  """

  @abstractmethod
  def __init__(self,
               category: StrEnum,
               provider: str,
               required_resource_keys: Set[str] | None = None) -> None:
    """Initialize parameters for base Scrape Articles job

    Args:
        category (StrEnum): Category
        provider (str): Provider
        required_resource_keys (Set[str]): Required Resource Keys of Dagster resource
    """
    super().__init__(provider=provider,
                     required_resource_keys=required_resource_keys)
    self._category = category

  @property
  def category(self) -> StrEnum:
    return self._category

  @abstractmethod
  def _scrape_links(self, page_url: str) -> list[str]:
    pass

  @abstractmethod
  def _scrape_article(self, article_url: str) -> ArticleDetail:
    pass
