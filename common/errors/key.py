from dagster import get_dagster_logger


class CategoryKeyError(Exception):
  """Category Key Exception raised for wrong input category

  Attributes:
    valid_values (list[str]): List of valid category values
    message (str): Exception Message
  """

  def __init__(self, valid_values: list[str]) -> None:
    self.message: str = f"CategoryKeyError: Specified category is not valid. Please either choose one of these [{', '.join(list(map(lambda v: f'{v}',valid_values)))}]"
    get_dagster_logger().error(self.message)
    super().__init__(self.message)
