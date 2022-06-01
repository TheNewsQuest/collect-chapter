from strenum import StrEnum


class Providers(StrEnum):
  """Enum of provider's names

  """
  VNEXPRESS = "vnexpress"
  CBSNEWS = "cbsnews"
  HISTORY = "history"  # Generalized provider from historical records
