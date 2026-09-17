from ._anvil_designer import VoucherReportTemplate
from anvil import *
import anvil.server


class VoucherReport(VoucherReportTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.unmatched_label.visible = False
    self.voucher_dropdown.items = anvil.server.call("get_voucher_options")

  @handle("home_link", "click")
  def home_link_click(self, **event_args):
    open_form("Form1")

  @handle("voucher_dropdown", "change")
  def voucher_dropdown_change(self, **event_args):
    voucher_code = self.voucher_dropdown.selected_value
    if not voucher_code:
      self.monthly_panel.items = []
      self.unmatched_label.visible = False
      return

    report = anvil.server.call("get_first_time_report", voucher_code)
    self.monthly_panel.items = report["monthly"]

    unmatched = report["unmatched_orders"]
    if unmatched:
      self.unmatched_label.text = (
        f"{len(unmatched)} order(s) using this voucher have no matching Sage account yet: "
        + ", ".join(unmatched)
      )
      self.unmatched_label.visible = True
    else:
      self.unmatched_label.visible = False
