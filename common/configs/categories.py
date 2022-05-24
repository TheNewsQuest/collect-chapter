from strenum import StrEnum  # pylint: disable=invalid-name


class VNExpressCategories(StrEnum):
  """List of categories for VNExpress
  """
  NEWS = 'news'
  BUSINESS = 'business'
  LIFE = 'life'
  WORLD = 'world'
