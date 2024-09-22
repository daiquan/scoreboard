import re

def to_snake_case(text):
  """
  Converts a given string to snake_case.

  Args:
      text: The string to convert.

  Returns:
      The snake_case version of the string.
  """

  # Replace spaces and dashes with underscores
  text = text.replace(" ", "_").replace("-", "_")

  # Convert to lowercase and remove any non-alphanumeric characters
  text = re.sub(r'[^a-zA-Z0-9_]', '', text.lower())

  return text