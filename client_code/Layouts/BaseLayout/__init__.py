from ._anvil_designer import BaseLayoutTemplate
from anvil import *
import anvil.users

from ... import Theme


class BaseLayout(BaseLayoutTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self._update_theme_link(Theme.get_theme())
    Theme.apply_theme(Theme.get_theme())

  def _update_theme_link(self, theme):
    self.theme_link.text = "☀️ Light mode" if theme == "dark" else "🌙 Dark mode"

  @handle("theme_link", "click")
  def theme_link_click(self, **event_args):
    new_theme = Theme.toggle_theme()
    self._update_theme_link(new_theme)

  @handle("vouchers_link", "click")
  def vouchers_link_click(self, **event_args):
    open_form("VoucherGallery")

  @handle("upload_link", "click")
  def upload_link_click(self, **event_args):
    open_form("UploadOrders")

  @handle("logout_link", "click")
  def logout_link_click(self, **event_args):
    anvil.users.logout()
    open_form("VoucherGallery")
