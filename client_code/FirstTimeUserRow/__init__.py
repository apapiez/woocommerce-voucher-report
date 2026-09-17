from ._anvil_designer import FirstTimeUserRowTemplate
from anvil import *


class FirstTimeUserRow(FirstTimeUserRowTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
