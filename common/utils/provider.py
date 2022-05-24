def build_provider_id(provider: str, identifier: str) -> str:
  """Build Identifier/Name for Job, Ops, etc. for specified provider

  Args:
      provider (str): Provider's name
      id (str): Identifier/Name

  Returns:
      str: ID/Name
  """
  return f"{provider}_{identifier}"
