from dataclasses import dataclass
from typing import Optional

from dagster import get_dagster_logger, resource
from dataclasses_json import DataClassJsonMixin

from article._base.resources.cursors import build_article_cursors_resource
from common.config.env import EnvVariables
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key


@dataclass
class VNExpressArticleCursors(DataClassJsonMixin):
  """Latest VNExpress articles' cursor by category data
  """
  news_cursor: Optional[str] = None
  business_cursor: Optional[str] = None
  life_cursor: Optional[str] = None
  world_cursor: Optional[str] = None


vnexpress_article_cursors_key = build_resource_key(Providers.VNEXPRESS,
                                                   ResourceKeys.ARTICLE_CURSORS)
vnexpress_article_cursors_resource = build_article_cursors_resource(
    Providers.VNEXPRESS, VNExpressArticleCursors)
