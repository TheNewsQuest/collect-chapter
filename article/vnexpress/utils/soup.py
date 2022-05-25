## Helper functions ##

import re
from datetime import datetime

import pytz
from bs4 import BeautifulSoup

from common.config import DateFormats
from common.config.env import EnvVariables
from common.config.selectors import HTMLSelectors, VNExpressSelectors


def extract_author(soup: BeautifulSoup) -> str:
  """Extract author from VNExpress article.

  Args:
      soup (BeautifulSoup): BeautifulSoup elements

  Returns:
      str: Author's name
  """
  author_div = soup.find(HTMLSelectors.DIV, class_=VNExpressSelectors.AUTHOR)
  if author_div.a is None:
    return "Unknown"
  return author_div.a.text


def extract_title(soup: BeautifulSoup) -> str:
  """Extract title from VNExpress article.

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML elements

  Returns:
      str: Title
  """
  return soup.find(HTMLSelectors.H1,
                   class_=VNExpressSelectors.TITLE_POST).text  # Extract title


def extract_lead_post_detail_row(soup: BeautifulSoup) -> str:
  """Extract lead post detail from VNExpress Article.

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: Lead post detail row
  """
  return soup.find(HTMLSelectors.SPAN,
                   class_=VNExpressSelectors.LEAD_POST_DETAIL_ROW).text


def extract_posted_at_datestr(soup: BeautifulSoup) -> str:
  """Extract article's posted date.

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: Date String for posted time
  """
  author_div = soup.find(HTMLSelectors.DIV, class_=VNExpressSelectors.AUTHOR)
  author_div_txt = author_div.text.replace("&nbsp", "")
  match_datestr = re.search(
      r"([a-zA-Z]+ [0-9]+, [0-9]+ \| [0-9]+:[0-9]+ [a-z]+)", author_div_txt)
  if match_datestr is None:
    return None
  post_datestr = author_div_txt[match_datestr.start():match_datestr.end()]
  local_time = pytz.timezone(EnvVariables.VNEXPRESS_TIMEZONE)
  local_datetime = local_time.localize(
      datetime.strptime(post_datestr, DateFormats.VNEXPRESS_DATE_POSTED))
  utc_datetime = local_datetime.astimezone(pytz.utc)
  return utc_datetime.strftime(DateFormats.YYYYMMDDHHMMSS)


def extract_thumbnail_url(soup: BeautifulSoup) -> str:
  """Extract Thumbnail's URL from VNExpress article

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: Thumbnail's URL
  """
  thumb_detail_div = soup.find(HTMLSelectors.DIV, class_="thumb_detail_top")
  # Handle missing thumbnail detail
  if thumb_detail_div is None:
    return ""
  return thumb_detail_div.img["src"]


def extract_category(soup: BeautifulSoup) -> str:
  """Extract category from VNExpress article

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: category (lowercase)
  """
  active_div = soup.find(HTMLSelectors.DIV,
                         class_=VNExpressSelectors.ITEM_MENU_LEFT_ACTIVE)
  category = active_div.a.text.lower()
  return category


def extract_subcategory(soup: BeautifulSoup) -> str:
  """Extract subcategory from VNExpress article

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: subcategory (lowercase)
  """
  detail_div = soup.find(HTMLSelectors.DIV,
                         class_=VNExpressSelectors.FOLDER_NAME_DETAIL)
  subcategory = detail_div.a.text.lower().replace('\n', '').replace('\t', '')
  return subcategory
