from dagster import get_dagster_logger
from strenum import StrEnum


class CategoryKeyError(Exception):
  """Category Key Exception raised for wrong input category

  Attributes:
    valid_values (list[str]): List of valid category values
    message (str): Exception Message
  """

  def __init__(self, category_enum: StrEnum) -> None:
    category_values = list(category_enum)
    enum_name = type(category_enum)
    self.message: str = f"CategoryKeyError: Specified category is not valid. Please either choose one of these [{', '.join(category_values)}] for {enum_name}"
    get_dagster_logger().error(self.message)
    super().__init__(self.message)
