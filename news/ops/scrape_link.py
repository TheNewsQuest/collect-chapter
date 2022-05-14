import requests
from bs4 import BeautifulSoup
from dagster import get_dagster_logger, op
from news.utils import is_covid_content, is_photo_content


@op(config_schema={"page": int})
def scrape_link(context) -> None:
  """Scrape list of links from a single VNExpress news page

  Args:
      context: Context object of Dagster
  """
  page = context.op_config['page']
  formatted_url = f"https://e.vnexpress.net/category/listcategory/category_id/1003894/page/{page}"
  try:
    resp = requests.get(formatted_url)
    get_dagster_logger().info(f"Request status: {resp.status_code}")
  except requests.exceptions.RequestException as err:
    get_dagster_logger().error(err)
    return
  json_data = resp.json()
  soup = BeautifulSoup(json_data['html'], "html.parser")  # Init BeautifulSoup
  get_dagster_logger().info(f"Now scraping: {formatted_url}")
  folder_items = soup.find_all("div", class_="item_list_folder")
  get_dagster_logger().info(f"Found {len(folder_items)} items.")
  links = []
  for item in folder_items:
    thumb_div = item.div.div
    if is_photo_content(thumb_div):
      continue
    if is_covid_content(thumb_div.a['href']):
      continue
    links.append(thumb_div.a['href'])
  # Display links
  for link in links:
    print(link, end='\n' * 2)
  get_dagster_logger().info(f"Found {len(links)} links.")
