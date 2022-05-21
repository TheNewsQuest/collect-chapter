import os

from strenum import StrEnum  # pylint: disable=invalid-name


class EnvVariables(StrEnum):
  """ Environment Variables from dotenv file
  """
  APP_ENV = os.getenv("APP_ENV")
  APP_NAME = os.getenv("APP_NAME")
  SCHEDULE_TIMEZONE = os.getenv("SCHEDULE_TIMEZONE")
  VNEXPRESS_TIMEZONE = os.getenv("VNEXPRESS_TIMEZONE")
  VNEXPRESS_REPO_NAME = os.getenv("VNEXPRESS_REPO_NAME")
  S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
  S3_BUCKET_URI = os.getenv("S3_BUCKET_URI")
  PAGE_SCRAPING_THRESHOLD = os.getenv("PAGE_SCRAPING_THRESHOLD")
  SCRAPE_SLEEP_TIME = os.getenv("SCRAPE_SLEEP_TIME")
