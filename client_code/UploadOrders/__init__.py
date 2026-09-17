from ._anvil_designer import UploadOrdersTemplate
from anvil import *
import anvil.server


class UploadOrders(UploadOrdersTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)

  @handle("home_link", "click")
  def home_link_click(self, **event_args):
    open_form("Form1")

  @handle("file_loader", "change")
  def file_loader_change(self, file, **event_args):
    self.import_button.enabled = file is not None

  @handle("import_button", "click")
  def import_button_click(self, **event_args):
    file = self.file_loader.file
    if file is None:
      return

    self.import_button.enabled = False
    self.import_button.text = "Importing..."
    try:
      result = anvil.server.call("import_orders_csv", file)
    finally:
      self.import_button.enabled = True
      self.import_button.text = "Import orders"

    summary = f"Imported {result['created']} new order(s), updated {result['updated']}."
    if result["errors"]:
      summary += f" {len(result['errors'])} row(s) skipped — see details below."
    self.result_label.text = summary
    self.result_label.visible = True

    self.errors_panel.items = result["errors"]
    self.errors_panel.visible = bool(result["errors"])
