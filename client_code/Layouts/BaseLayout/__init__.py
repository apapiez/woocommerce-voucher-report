from ._anvil_designer import BaseLayoutTemplate
from anvil import *
import anvil.users


class BaseLayout(BaseLayoutTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)

  @handle("logout_link", "click")
  def logout_link_click(self, **event_args):
    anvil.users.logout()
    open_form("Form1")
