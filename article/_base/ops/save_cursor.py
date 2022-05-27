from __future__ import annotations

from typing import Optional, Set

from strenum import StrEnum

from article._base.ops.base_op import BaseCategorizedOp
from common.config.env import EnvVariables
from common.config.resource_keys import ResourceKeys
from common.utils.resource import build_resource_key


class BaseSaveCursorOp(BaseCategorizedOp):
  """Base Save Cursor Operation

  Args:
      BaseOp: Base Operation class
  """

  def __init__(self,
               category: StrEnum,
               provider: str,
               required_resource_keys: Optional[Set[str]] = None) -> None:
    super().__init__(category, provider, required_resource_keys)

  def _build_file_uri(self, context) -> str:
    """Build cursors file URI on S3 Bucket

    Args:
        context: Dagster Context object

    Returns:
        str: File's URI on S3 Bucket
    """
    s3_resource = getattr(
        context.resources,
        build_resource_key(self.provider, ResourceKeys.S3_RESOURCE_PREFIX))
    file_uri = f"{s3_resource}/{EnvVariables.ARTICLE_CURSORS_FILENAME}"
    return file_uri
