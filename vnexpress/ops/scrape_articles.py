from dataclasses import dataclass
from time import sleep

import requests
from bs4 import BeautifulSoup
from dagster import OpDefinition, get_dagster_logger, op
from vnexpress.constants.category_url import VNEXPRESS_CATEGORY_URL
from vnexpress.constants.selectors import (DIV_SELECTOR, HREF_SELECTOR,
                                           ITEM_LIST_FOLDER_SELECTOR,
                                           LEAD_POST_DETAIL_ROW_SELECTOR,
                                           NORMAL_PARAGRAPH_SELECTOR,
                                           PARAGRAPH_SELECTOR, SPAN_SELECTOR)
from vnexpress.enums.categories import VNExpressCategories
from vnexpress.utils import is_restricted_content

SCRAPE_SLEEP_TIME = 1.25


@dataclass
class ArticleDetail:
  """Data class for article's detail
  """
  title: str
  content: str
  link: str
  author: str
  posted_at: str


def scrape_links(page_url: str) -> list[str]:
  """Scrape list of VNExpress links from a page.

  Args:
      page_url (int): Page's url to scrape links

  Returns:
      list[str]: List of links
  """
  json_data = requests.get(page_url).json()
  if json_data["end"] == 1:  # Handle ending
    return []
  soup = BeautifulSoup(json_data["html"], "html.parser")
  folder_items = soup.find_all(DIV_SELECTOR, class_=ITEM_LIST_FOLDER_SELECTOR)
  links = []
  for item in folder_items:
    thumb_div = item.div.div  # Extract thumbnail div
    if is_restricted_content(thumb_div):
      continue
    links.append(thumb_div.a[HREF_SELECTOR])
  # Display links
  for link in links:
    print(link, end='\n' * 2)
  return links


def scrape_article(link: str) -> ArticleDetail:
  """Scrape article's detail from VNExpress

  Args:
      link (str): Link to article

  Returns:
      ArticleDetail: article's detail
  """
  resp = requests.get(link)
  get_dagster_logger().info(f"Scraping an article at: {link}")
  html = resp.text
  soup = BeautifulSoup(html, "html.parser")
  content_paragraphs = []
  lead_post_detail = soup.find(SPAN_SELECTOR,
                               class_=LEAD_POST_DETAIL_ROW_SELECTOR).text
  content_paragraphs.append(lead_post_detail)
  paragraphs = soup.find_all(PARAGRAPH_SELECTOR,
                             class_=NORMAL_PARAGRAPH_SELECTOR)
  for paragraph in paragraphs:
    content_paragraphs.append(paragraph.text)
  content = '\n'.join(content_paragraphs)
  return ArticleDetail(title='',
                       content=content,
                       author='',
                       link='',
                       posted_at='')


def scrape_articles_by_category_op_factory(category: VNExpressCategories,
                                           **kwargs) -> OpDefinition:

  @op(name=f"scrape_articles_by_{category}", **kwargs)
  def _op() -> list[ArticleDetail]:
    start_page = 1
    result = []
    while True:
      scrape_url = f"{VNEXPRESS_CATEGORY_URL[category]}/page/{start_page}"
      links = scrape_links(scrape_url)
      if len(links) == 0:
        break
      for link in links:
        result.append(scrape_article(link))
      sleep(SCRAPE_SLEEP_TIME)  # Delay crawler to avoid rate limit
      start_page += 1
      if start_page > 10:  # Early-stop for testing
        print("EARLY BREAK!")
        break
    return result

  return _op
