import re
from datetime import datetime

import pytz
from bs4 import BeautifulSoup
from vnexpress.constants.selectors import (AUTHOR_SELECTOR, DIV_SELECTOR,
                                           H1_SELECTOR,
                                           LEAD_POST_DETAIL_ROW_SELECTOR,
                                           SPAN_SELECTOR, TITLE_POST_SELECTOR)
from vnexpress.constants.time import (VNEXPRESS_DATE_POSTED_FORMAT,
                                      VNEXPRESS_TIMEZONE,
                                      YYYYMMDDHHMMSS_DATE_FORMAT)


def extract_author(soup: BeautifulSoup) -> str:
  """Extract author from VNExpress article.

  Args:
      soup (BeautifulSoup): BeautifulSoup elements

  Returns:
      str: Author's name
  """
  author_div = soup.find(DIV_SELECTOR, class_=AUTHOR_SELECTOR)
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
  return soup.find(H1_SELECTOR,
                   class_=TITLE_POST_SELECTOR).text  # Extract title


def extract_lead_post_detail_row(soup: BeautifulSoup) -> str:
  """Extract lead post detail from VNExpress Article.

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: Lead post detail row
  """
  return soup.find(
      SPAN_SELECTOR,
      class_=LEAD_POST_DETAIL_ROW_SELECTOR).text  # Find post leading row


def extract_posted_at_datestr(soup: BeautifulSoup) -> str:
  """Extract article's posted date.

  Args:
      soup (BeautifulSoup): BeautifulSoup HTML Elements

  Returns:
      str: Date String for posted time
  """
  author_div = soup.find(DIV_SELECTOR, class_=AUTHOR_SELECTOR)
  author_div_txt = author_div.text.replace("&nbsp", "")
  match_datestr = re.search(
      r"([a-zA-Z]+ [0-9]+, [0-9]+ \| [0-9]+:[0-9]+ [a-z]+)", author_div_txt)
  if match_datestr is None:
    return None
  post_datestr = author_div_txt[match_datestr.start():match_datestr.end()]
  local_time = pytz.timezone(VNEXPRESS_TIMEZONE)
  local_datetime = local_time.localize(
      datetime.strptime(post_datestr, VNEXPRESS_DATE_POSTED_FORMAT))
  utc_datetime = local_datetime.astimezone(pytz.utc)
  return utc_datetime.strftime(YYYYMMDDHHMMSS_DATE_FORMAT)


def extract_thumbnail_url(soup: BeautifulSoup) -> str:
  thumb_detail_div = soup.find(DIV_SELECTOR, class_="thumb_detail_top")
  # Handle missing thumbnail detail
  if thumb_detail_div is None:
    return ""
  return thumb_detail_div.img["src"]
