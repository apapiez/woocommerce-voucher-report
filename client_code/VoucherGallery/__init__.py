from ._anvil_designer import VoucherGalleryTemplate
from anvil import *
import anvil.server
import anvil.users


class VoucherGallery(VoucherGalleryTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)

    if anvil.users.get_user() is None:
      anvil.users.login_with_form(show_signup_option=False)

    summaries = anvil.server.call("get_voucher_summaries")
    self.gallery_panel.items = summaries
    self.empty_label.visible = not summaries
