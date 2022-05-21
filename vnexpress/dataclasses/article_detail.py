from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


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
