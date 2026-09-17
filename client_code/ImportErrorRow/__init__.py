from ._anvil_designer import ImportErrorRowTemplate
from anvil import *


class ImportErrorRow(ImportErrorRowTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
