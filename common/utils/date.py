from datetime import datetime
from time import strptime

import pytz

from common.config.date_formats import DateFormats


def naive_datetime_to_utc(datetime_obj: datetime, zone: str) -> datetime:
  """Localize naive datetime and convert to UTC

  Args:
      datetime_obj (datetime): _description_
      zone (str): _description_

  Returns:
      datetime: _description_
  """
  local_time = pytz.timezone(zone)
  local_datetime = local_time.localize(datetime_obj)
  utc_datetime = local_datetime.astimezone(pytz.utc)
  return utc_datetime


def format_datetime_str(
    datetime_obj: datetime,
    str_format: DateFormats = DateFormats.YYYYMMDDHHMMSS) -> str:
  """Format Datetime to Datetime String with specified format

  Args:
      datetime_obj (datetime): Datetime object
      str_format (DateFormats, optional): Defaults to DateFormats.YYYYMMDDHHMMSS.

  Returns:
      str: Datetime string
  """
  return datetime_obj.strftime(str_format)


def format_datetime(
    datetime_str: str,
    str_format: DateFormats = DateFormats.YYYYMMDDHHMMSS) -> datetime:
  """Format Datetime String to Datetime Object with specified format

  Args:
      datetime_str (datetime): Datetime string
      str_format (DateFormats, optional): Defaults to DateFormats.YYYYMMDDHHMMSS.

  Returns:
      str: Datetime object
  """
  return strptime(datetime_str, str_format)
