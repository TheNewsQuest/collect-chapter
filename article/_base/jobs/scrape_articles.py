from abc import ABC, abstractmethod
from typing import Any, Dict

from dagster import JobDefinition, OpDefinition
from strenum import StrEnum


class BaseScrapeArticlesJob(ABC):
  """Base Scrape Articles job
  Args:
      ABC: Abstract Base Classes
  """

  def __init__(self, category: str, provider: str,
               resource_defs: Dict[str, Any]) -> None:
    """Initialize parameters for scraping articles job

    Args:
        category (str): Category
        provider (str): Provider's name
        resource_defs (Dict[str, Any]): Resource Definitions
    """
    self._category = category
    self._provider = provider
    self._resource_defs = resource_defs

  @property
  def category(self) -> str:
    return self._category

  @property
  def provider(self) -> str:
    return self._provider

  @property
  def resource_defs(self) -> Dict[str, Any]:
    return self._resource_defs

  @abstractmethod
  def build(self, **kwargs) -> OpDefinition:
    pass


class BaseScrapeArticlesJobFactory(ABC):
  """Base class for creating scraping articles job factory

  Args:
      ABC: Abstract Base Classes
  """

  @abstractmethod
  def create_job(self, category: StrEnum, **kwargs) -> JobDefinition:
    pass
