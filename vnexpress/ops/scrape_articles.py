from time import sleep

import requests
from bs4 import BeautifulSoup
from dagster import OpDefinition, get_dagster_logger, op
from vnexpress.common.constants.selectors import (DIV_SELECTOR, HREF_SELECTOR,
                                                  ITEM_LIST_FOLDER_SELECTOR,
                                                  NORMAL_PARAGRAPH_SELECTOR,
                                                  PARAGRAPH_SELECTOR)
from vnexpress.common.constants.url import VNEXPRESS_CATEGORY_URL
from vnexpress.common.dataclasses.article_detail import ArticleDetail
from vnexpress.common.enums.categories import VNExpressCategories
from vnexpress.common.enums.env import EnvVariables
from vnexpress.common.utils.content import is_restricted_content
from vnexpress.common.utils.soup import (extract_author, extract_category,
                                         extract_lead_post_detail_row,
                                         extract_posted_at_datestr,
                                         extract_subcategory,
                                         extract_thumbnail_url, extract_title)


def _scrape_links(page_url: str) -> list[str]:
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


def _scrape_article(link: str) -> ArticleDetail:
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
  title = extract_title(soup)
  author = extract_author(soup)
  posted_at = extract_posted_at_datestr(soup)
  thumbnail_url = extract_thumbnail_url(soup)
  lead_post_detail = extract_lead_post_detail_row(soup)
  category = extract_category(soup)
  subcategory = extract_subcategory(soup)
  paragraphs = [lead_post_detail]  # Init paragraphs content
  p_tags = soup.find_all(PARAGRAPH_SELECTOR, class_=NORMAL_PARAGRAPH_SELECTOR)
  for p_tag in p_tags:
    paragraphs.append(p_tag.text)
  content = '\n'.join(paragraphs)
  return ArticleDetail(title=title,
                       thumbnail_url=thumbnail_url,
                       content=content,
                       author=author,
                       link=link,
                       posted_at=posted_at,
                       category=category,
                       subcategory=subcategory)


def scrape_articles_op_factory(category: VNExpressCategories,
                               **kwargs) -> OpDefinition:
  """Factory for creating article scraping job based on specified category.

  Args:
      category (VNExpressCategories): VNExpress Category

  Returns:
      OpDefinition: Operation for scraping article based on specified category.
  """

  @op(name=f"scrape_{category}_articles_op",
      required_resource_keys={"latest_articles_dt"},
      **kwargs)
  def _op(context) -> list[ArticleDetail]:
    """Scrape list of articles based on category operation

    Returns:
        list[ArticleDetail]: List of article details
    """
    # Retrieve latest article's datetimes by category
    latest_dts = getattr(context.resources.latest_articles_dt, f"{category}_dt")
    get_dagster_logger().info(f"latest_dts of {category}: {latest_dts}")
    # Extract config from env vars
    scrape_threshold = int(EnvVariables.PAGE_SCRAPING_THRESHOLD)
    scrape_sleep_time = float(EnvVariables.SCRAPE_SLEEP_TIME)
    # Scrape articles per page
    articles = []
    for page in range(1, scrape_threshold + 1):
      scrape_url = f"{VNEXPRESS_CATEGORY_URL[category]}/page/{page}"
      links = _scrape_links(scrape_url)
      if len(links) == 0:
        break
      for link in links:
        article = _scrape_article(link)
        articles.append(article)
        # Delay crawler to avoid rate limit
        sleep(scrape_sleep_time)
    get_dagster_logger().info(
        f"Total {category} articles collected: {len(articles)}")
    return articles

  return _op
