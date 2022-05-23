from bs4 import ResultSet

from common.constants import VNEXPRESS_COVID19_URL
from common.enums.selectors import HTMLSelectors, VNExpressSelectors


def is_icon(div: ResultSet, icon: str) -> bool:
  """Check the div's icon for article's content

  Args:
      div (ResultSet): HTML element (div)

  Returns:
      bool: True if it's photo slideshow  || False if not
  """
  return div.span is not None and div.span.i[HTMLSelectors.CLASS][1] == icon


def is_covid_content(div: ResultSet) -> bool:
  """Check if the article is linked to the COVID-19 Report of VN-Express.

  Args:
      div (ResultSet): Div Block containing href

  Returns:
      bool: True if it's photo slideshow || False if not
  """
  return div.a[HTMLSelectors.HREF] == VNEXPRESS_COVID19_URL


def is_restricted_content(div: ResultSet) -> bool:
  """Check if the content is restricted to scraping.

  Args:
      div (ResultSet): Thumbnail Div

  Returns:
      bool: True if restricted content || False if not
  """
  if is_covid_content(div):
    return True
  if is_icon(div, VNExpressSelectors.ICON_PHOTO):
    return True
  if is_icon(div, VNExpressSelectors.ICON_VIDEO):
    return True
  if is_icon(div, VNExpressSelectors.ICON_INFOGRAPHIC):
    return True
  if is_icon(div, VNExpressSelectors.ICON_INTERACTIVE):
    return True
  return False
