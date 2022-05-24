from datetime import datetime
from time import sleep, strptime

import requests
from bs4 import BeautifulSoup
from dagster import OpDefinition, get_dagster_logger, op

from article._base.ops import (ArticleDetail, BaseScrapeArticlesOp,
                               BaseScrapeArticlesOpFactory)
from common.configs import (VNEXPRESS_CATEGORY_URL, HTMLSelectors,
                            VNExpressSelectors)
from common.configs.categories import VNExpressCategories
from common.configs.date_formats import DateFormats
from common.configs.env import EnvVariables
from common.configs.resource_keys import ResourceKeys
from common.utils.content import is_restricted_content
from common.utils.provider import build_provider_id
from common.utils.soup import (extract_author, extract_category,
                               extract_lead_post_detail_row,
                               extract_posted_at_datestr, extract_subcategory,
                               extract_thumbnail_url, extract_title)


class VNExpressScrapeArticlesOp(BaseScrapeArticlesOp):
  """VNExpress Scrape Articles by category Op
  """

  def __init__(self, category: str) -> None:
    super().__init__(category, EnvVariables.VNEXPRESS_PROVIDER_NAME,
                     {str(ResourceKeys.ARTICLE_CURSORS)})

  def _scrape_links(self, page_url: str) -> list[str]:
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
    folder_items = soup.find_all(HTMLSelectors.DIV,
                                 class_=VNExpressSelectors.ITEM_LIST_FOLDER)
    links = []
    for item in folder_items:
      thumb_div = item.div.div  # Extract thumbnail div
      if is_restricted_content(thumb_div):
        continue
      links.append(thumb_div.a[HTMLSelectors.HREF])
    # Display links
    for link in links:
      print(link, end='\n' * 2)
    return links

  def _scrape_article(self, article_url: str) -> list[str]:
    """Scrape article's detail from VNExpress

    Args:
        link (str): Link to article

    Returns:
        ArticleDetail: article's detail
    """
    resp = requests.get(article_url)
    get_dagster_logger().info(f"Scraping an article at: {article_url}")
    soup = BeautifulSoup(resp.text, "html.parser")
    title = extract_title(soup)
    author = extract_author(soup)
    posted_at = extract_posted_at_datestr(soup)
    thumbnail_url = extract_thumbnail_url(soup)
    lead_post_detail = extract_lead_post_detail_row(soup)
    category = extract_category(soup)
    subcategory = extract_subcategory(soup)
    paragraphs = [lead_post_detail]  # Init paragraphs content
    p_tags = soup.find_all(HTMLSelectors.PARAGRAPH,
                           class_=VNExpressSelectors.NORMAL_PARAGRAPH)
    for p_tag in p_tags:
      paragraphs.append(p_tag.text)
    content = '\n'.join(paragraphs)
    return ArticleDetail(title=title,
                         thumbnail_url=thumbnail_url,
                         content=content,
                         author=author,
                         link=article_url,
                         posted_at=posted_at,
                         category=category,
                         subcategory=subcategory)

  def build(self, **kwargs) -> OpDefinition:
    # Build op process
    @op(name=build_provider_id(
        provider=self.provider,
        identifier=f"scrape_{self.category}_articles_op"),
        required_resource_keys=self.required_resource_keys,
        **kwargs)
    def _op(context) -> list[ArticleDetail]:
      """Scrape list of articles based on category operation

      Returns:
          list[ArticleDetail]: List of article details
      """
      # Extract config from env vars
      scrape_threshold = int(EnvVariables.PAGE_SCRAPING_THRESHOLD)
      scrape_sleep_time = float(EnvVariables.SCRAPE_SLEEP_TIME)
      # Get article's cursor by category
      article_cursor: str = getattr(context.resources.article_cursors,
                                    f"{self.category}_cursor")
      cursor_dt: datetime = None if article_cursor is None else strptime(
          article_cursor, DateFormats.YYYYMMDDHHMMSS)
      get_dagster_logger().info(
          f"Latest Datetime of {self.category}'s cursor: {cursor_dt}")
      # Scrape articles per page
      articles = []
      for page in range(1, scrape_threshold + 1):
        scrape_url = f"{VNEXPRESS_CATEGORY_URL[self.category]}/page/{page}"
        links = self._scrape_links(scrape_url)
        if len(links) == 0:
          break
        for link in links:
          article = self._scrape_article(link)
          posted_at_dt = strptime(article.posted_at, DateFormats.YYYYMMDDHHMMSS)
          if (cursor_dt is not None) and (posted_at_dt == cursor_dt):
            return articles  # Early-stop scraping
          articles.append(article)
          sleep(scrape_sleep_time)  # Delay scraper
      get_dagster_logger().info(
          f"Total {self.category} articles collected: {len(articles)}")
      return articles

    return _op


class VNExpressScrapeArticlesOpFactory(BaseScrapeArticlesOpFactory):
  """VNExpress Scrape Articles Operation factory
  """

  def create_op(self, category: VNExpressCategories, **kwargs) -> OpDefinition:
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError:
      get_dagster_logger().error(
          "Specified category does not exist in operation factory.")
      return None
    scrape_op = VNExpressScrapeArticlesOp(category).build(**kwargs)
    return scrape_op
