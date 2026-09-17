from ._anvil_designer import MonthlyCountRowTemplate
from anvil import *


class MonthlyCountRow(MonthlyCountRowTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
