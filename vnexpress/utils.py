from bs4 import ResultSet

from vnexpress.constants.selectors import (CLASS_SELECTOR, HREF_SELECTOR,
                                           ICON_INFOGRAPHIC_SELECTOR,
                                           ICON_INTERACTIVE_SELECTOR,
                                           ICON_PHOTO_SELECTOR,
                                           ICON_VIDEO_SELECTOR,
                                           VNEXPRESS_COVID19_LINK)


def is_icon(div: ResultSet, icon: str) -> bool:
  """Check the div's icon for article's content

  Args:
      div (ResultSet): HTML element (div)

  Returns:
      bool: True if it's photo slideshow  || False if not
  """
  return div.span is not None and div.span.i[CLASS_SELECTOR][1] == icon


def is_covid_content(div: ResultSet) -> bool:
  """Check if the article is linked to the COVID-19 Report of VN-Express.

  Args:
      div (ResultSet): Div Block containing href

  Returns:
      bool: True if it's photo slideshow || False if not
  """
  return div.a[HREF_SELECTOR] == VNEXPRESS_COVID19_LINK


def is_restricted_content(div: ResultSet) -> bool:
  """Check if the content is restricted to scraping.

  Args:
      div (ResultSet): Thumbnail Div

  Returns:
      bool: True if restricted content || False if not
  """
  if is_covid_content(div):
    return True
  if is_icon(div, ICON_PHOTO_SELECTOR):
    return True
  if is_icon(div, ICON_VIDEO_SELECTOR):
    return True
  if is_icon(div, ICON_INFOGRAPHIC_SELECTOR):
    return True
  if is_icon(div, ICON_INTERACTIVE_SELECTOR):
    return True
  return False
