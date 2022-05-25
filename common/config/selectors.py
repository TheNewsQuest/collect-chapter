from strenum import StrEnum  # pylint: disable=invalid-name


class HTMLSelectors(StrEnum):
  """List of HTML selectors
  """
  DIV = "div"
  SPAN = "span"
  HREF = "href"
  PARAGRAPH = "p"
  CLASS = "class"
  H1 = "h1"


class VNExpressSelectors(StrEnum):
  """List of VNExpress selectors
  """
  # Item selectors
  ITEM_LIST_FOLDER = "item_list_folder"
  LEAD_POST_DETAIL_ROW = "lead_post_detail row"
  NORMAL_PARAGRAPH = "Normal"
  TITLE_POST = "title_post"
  AUTHOR = "author"
  ITEM_MENU_LEFT_ACTIVE = "item_menu_left active"
  FOLDER_NAME_DETAIL = "folder_name_detail"
  # Icons
  ICON_PHOTO = "ic-photo"
  ICON_VIDEO = "ic-video"
  ICON_INFOGRAPHIC = "ic-infographic"
  ICON_INTERACTIVE = "ic-interactive"
