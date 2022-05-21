from strenum import StrEnum  # pylint: disable=invalid-name


class DateFormats(StrEnum):
  """Date format enums
  """
  VNEXPRESS_DATE_POSTED = "%B %d, %Y | %I:%M %p"
  YYYYMMDDHHMMSS = "%Y-%m-%d %H:%M:%S"
  YYYYMMDD = "%Y-%m-%d"
