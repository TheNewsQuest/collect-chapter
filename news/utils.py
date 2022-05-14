from bs4 import ResultSet


def is_photo_content(div: ResultSet) -> bool:
  """Check if the article's content is photo slideshow.

  Args:
      div (ResultSet): HTML element (div)

  Returns:
      bool: True if it's photo slideshow  || False if not
  """
  return div.span is not None and div.span.i['class'][1] == 'ic-photo'


def is_covid_content(link: str) -> bool:
  """Check if the article is linked to the COVID-19 Report of VN-Express.

  Args:
      link (str): Link of article

  Returns:
      bool: True if it's photo slideshow || False if not
  """
  return link == 'https://e.vnexpress.net/covid-19/covid-19-viet-nam'
