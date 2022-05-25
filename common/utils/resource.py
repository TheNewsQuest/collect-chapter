def build_resource_key(provider: str, key: str) -> str:
  """Build Provider-based resource key

  Args:
      provider (str): Provider's name
      key (str): Resource key

  Returns:
      str: Provider-based resource key
  """
  return f"{provider}_{key}"
