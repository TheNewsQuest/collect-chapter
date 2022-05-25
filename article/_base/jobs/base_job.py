from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set

from dagster import JobDefinition, OpDefinition
from strenum import StrEnum

from common.config.providers import Providers


class BaseJob(ABC):
  """Base job

  Attributes:
      provider (Providers): Provider's name
      resource_defs (Dict[str, Any] | None): Resource Definitions of Dagster
  """

  @abstractmethod
  def __init__(self,
               provider: Providers,
               resource_defs: Optional[Dict[str, Any]] = None) -> None:
    """Initialize parameters for base Scrape Articles job

    Args:
        provider (str): Provider
        required_resource_keys (Set[str]): Required Resource Keys of Dagster resource
    """
    self._provider = provider
    self._resource_defs = resource_defs

  @property
  def provider(self) -> str:
    return self._provider

  @property
  def resource_defs(self) -> Set[str]:
    return self._resource_defs

  @resource_defs.setter
  def resource_defs(self, resource_defs: Dict[str, Any]) -> None:
    self._resource_defs = resource_defs

  @abstractmethod
  def build(self, **kwargs) -> OpDefinition:
    pass


class BaseCategorizedJob(BaseJob):
  """Base Categorized job

  Attributes:
      category (StrEnum): Category
      provider (Providers): Provider's name
      resource_defs (Dict[str, Any] | None): Resource Definitions of Dagster
  """

  @abstractmethod
  def __init__(self,
               category: StrEnum,
               provider: Providers,
               resource_defs: Optional[Dict[str, Any]] = None) -> None:
    self._category = category
    super().__init__(provider, resource_defs)

  @property
  def category(self) -> str:
    return self._category


class BaseCategorizedJobFactory(ABC):
  """Base factory class for creating job correlated with category
  """

  @abstractmethod
  def create_job(self, category: StrEnum, **kwargs) -> JobDefinition:
    pass
