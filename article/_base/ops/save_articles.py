from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Optional, Set

import pytz
from strenum import StrEnum

from article._base.ops import BaseOp
from common.config import DateFormats
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key


class BaseSaveArticlesOp(BaseOp):
  """Base Save Articles operation class

  Args:
      BaseOp: Base Operation
  """

  @abstractmethod
  def __init__(self,
               category: StrEnum,
               provider: str,
               required_resource_keys: Optional[Set[str]] = None) -> None:
    """Initialize parameters for base Save Articles job

    Args:
        category (StrEnum): Category
        provider (str): Provider
        required_resource_keys (Set[str]): Required Resource Keys of Dagster resource
    """
    super().__init__(provider=provider,
                     required_resource_keys=required_resource_keys)
    self._category = category

  @property
  def category(self) -> str:
    return self._category

  def _build_file_uri(self, context) -> str:
    """Build File URI from Dagster resource context

    Args:
        context: Dagster context

    Returns:
        str: File's URI
    """
    today_datestr = datetime.now(tz=pytz.utc).strftime(DateFormats.YYYYMMDD)
    file_uri = f"{getattr(context.resources, build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_PREFIX))}/{self.category}/{today_datestr}.json"
    return file_uri
