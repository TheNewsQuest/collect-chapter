from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class ArticleCursors(DataClassJsonMixin):
  """Latest articles' cursor by category data
  """
  news_cursor: str = None
  business_cursor: str = None
  life_cursor: str = None
