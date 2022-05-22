from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class LatestArticlesDatetime(DataClassJsonMixin):
  """Latest articles' datetime by category data
  """
  news_dt: str = None
  business_dt: str = None
  life_dt: str = None
