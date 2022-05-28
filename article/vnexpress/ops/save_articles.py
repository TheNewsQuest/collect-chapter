from __future__ import annotations

from dagster import OpDefinition
from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOpFactory
from article._base.ops.save_articles import BaseSaveArticlesOp
from common.config.categories import VNExpressCategories
from common.config.providers import Providers
from common.config.resource_keys import ResourceKeys
from common.errors.key import CategoryKeyError
from common.utils import build_resource_key


class VNExpressSaveArticlesOp(BaseSaveArticlesOp):
  """VNExpress Save Articles Operation

  Args:
      BaseSaveArticlesOp: Base Save Article Operation class
  """

  def __init__(
      self,
      category: StrEnum,
  ) -> None:
    super().__init__(category=category, provider=Providers.VNEXPRESS)
    self.required_resource_keys = {
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_URI)
    }


class VNExpressSaveArticlesOpFactory(BaseCategorizedOpFactory):
  """Op Factory for creating Save Articles Op for specified category

  Args:
      BaseCategorizedOpFactory: Base Categorized Op Factory
  """

  def create_op(self, category: VNExpressCategories, **kwargs) -> OpDefinition:
    """Creating Save Articles operation based on specified category of VNExpress

    Args:
        category (StrEnum): Enum of Category

    Returns:
        OpDefinition: Dagster's Op Definition
    """
    try:
      category = VNExpressCategories[category.upper()]
    except KeyError:
      raise CategoryKeyError(VNExpressCategories) from KeyError
    save_articles_op = VNExpressSaveArticlesOp(category).build(**kwargs)
    return save_articles_op
