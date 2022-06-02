from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Optional, Set

import pytz
from dagster import In, OpDefinition, get_dagster_logger, op
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOp
from article._base.ops.scrape_articles import ArticleDetail
from common.config import DateFormats
from common.config.resource_keys import ResourceKeys
from common.utils.date import format_datetime_str
from common.utils.id import build_id
from common.utils.resource import build_resource_key
from common.utils.s3 import write_json_file_s3


class BaseSaveArticlesOp(BaseCategorizedOp):
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
    super().__init__(category=category,
                     provider=provider,
                     required_resource_keys=required_resource_keys)

  def _build_save_file_uri(self, context) -> str:
    """Build Save File URI from Dagster resource context

    Args:
        context: Dagster context

    Returns:
        str: File's URI
    """
    today_datestr = format_datetime_str(datetime.now(tz=pytz.utc),
                                        DateFormats.YYYYMMDDHHMMSS)
    s3_resource = getattr(
        context.resources,
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI))
    file_uri = f"{s3_resource}/{self.category}/{today_datestr}.json"
    return file_uri

  def build(self, **kwargs) -> OpDefinition:
    """Build Save Articles operation for specified category

    Returns:
        OpDefinition: Save to S3 Operation
    """

    @op(name=build_id(provider=self.provider,
                      identifier=f"save_{self.category}_articles_s3_op"),
        required_resource_keys=self.required_resource_keys,
        ins={"articles": In(dagster_type=list[ArticleDetail])},
        **kwargs)
    def _op(context, articles: list[ArticleDetail]):
      """Save list of articles to S3 bucket operation

      Args:
          context: Dagster context object
          articles (list[ArticleDetail]): List of article details
      """
      file_uri = self._build_save_file_uri(context)
      article_details = ArticleDetail.schema().dump(articles, many=True)
      write_json_file_s3(article_details, file_uri)
      get_dagster_logger().info(f"Save {file_uri} successfully.")

    return _op
