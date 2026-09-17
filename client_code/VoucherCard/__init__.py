from ._anvil_designer import VoucherCardTemplate
from anvil import *


class VoucherCard(VoucherCardTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)

  def card_click(self, event):
    open_form("VoucherReport", voucher_code=self.item["voucher_code"])
