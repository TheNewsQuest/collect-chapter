from dataclasses import dataclass

import requests
from dagster import ResourceDefinition, resource
from dataclasses_json import DataClassJsonMixin

from common.config.env import EnvVariables


@dataclass
class GeneratedQuest(DataClassJsonMixin):
  """Generated Quest dataclass from Alchemy model API result
  """
  # pylint: disable=invalid-name
  answerText: str
  distractors: list[str]
  questionText: str


class AlchemyClient:
  """Alchemy Client for API calls, and many more interaction methods!
  """

  def __init__(self) -> None:
    self._api_url: str = EnvVariables.ALCHEMY_API_URL

  @property
  def api_url(self) -> str:
    return self._api_url

  def get_questgen_endpoint(self) -> str:
    """Get quest generation endpoint from Alchemy API
    """
    return f"{self.api_url}/questgen"

  def generate_quests(self, content: str) -> list[GeneratedQuest]:
    """Generate list of quests from input content

    Args:
        content (str): Content of articles/books/etc.

    Returns:
        list[GeneratedQuest]: List of quests
    """
    payload = {"content": content}
    questgen_endpoint = self.get_questgen_endpoint()
    resp_text = requests.post(url=questgen_endpoint, json=payload).text
    quests = GeneratedQuest.schema().loads(resp_text, many=True)
    return quests


@resource()
def get_alchemy_client() -> ResourceDefinition:
  """Get Alchemy client to interact with the API intuitively
  """
  return AlchemyClient()
