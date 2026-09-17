from ._anvil_designer import Form1Template
from anvil import *


class Form1(Form1Template):
  def __init__(self, **properties):
    super().__init__(**properties)

  @handle("upload_button", "click")
  def upload_button_click(self, **event_args):
    open_form("UploadOrders")

  @handle("report_button", "click")
  def report_button_click(self, **event_args):
    open_form("VoucherReport")
