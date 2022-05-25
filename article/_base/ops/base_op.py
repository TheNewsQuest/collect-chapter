from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Set

from dagster import OpDefinition
from strenum import StrEnum

from common.config.providers import Providers


class BaseOp(ABC):
  """Base Operation

  Args:
      ABC : Abstract Base Classes
  """

  @abstractmethod
  def __init__(self,
               provider: Providers,
               required_resource_keys: Optional[Set[str]] = None) -> None:
    """Initialize parameters for base Scrape Articles job

    Args:
        category (StrEnum): Category
        provider (str): Provider
        required_resource_keys (Set[str]): Required Resource Keys of Dagster resource
    """
    self._provider = provider
    self._required_resource_keys = required_resource_keys

  @property
  def provider(self) -> str:
    return self._provider

  @property
  def required_resource_keys(self) -> Set[str]:
    return self._required_resource_keys

  @required_resource_keys.setter
  def required_resource_keys(self, required_resource_keys: Set[str]) -> None:
    self._required_resource_keys = required_resource_keys

  @abstractmethod
  def build(self, **kwargs) -> OpDefinition:
    pass


class BaseCategorizedOp(BaseOp):
  """Base Categorized operation

  Attributes:
      category (StrEnum): Category
      provider (Providers): Provider's name
      required_resource_keys (Set[str] | None): Required Resource Keys of Dagster
  """

  @abstractmethod
  def __init__(self,
               category: StrEnum,
               provider: Providers,
               required_resource_keys: Optional[Set[str]] = None) -> None:
    self._category = category
    super().__init__(provider, required_resource_keys)

  @property
  def category(self) -> str:
    return self._category


class BaseCategorizedOpFactory(ABC):
  """Base factory class for creating operation correlated with category

  Args:
      ABC: Abstract Base Classes
  """

  @abstractmethod
  def create_op(self, category: StrEnum, **kwargs) -> OpDefinition:
    pass
