from ._anvil_designer import VoucherReportTemplate
from anvil import *
import anvil.server

from .. import Theme


class VoucherReport(VoucherReportTemplate):
  def __init__(self, voucher_code=None, **properties):
    super().__init__(**properties)
    self.unmatched_label.visible = False
    self.usage_heading.visible = False
    self.usage_chart.visible = False

    if not voucher_code:
      self.label_1.text = "Voucher report"
      self.monthly_panel.items = []
      return

    self.label_1.text = f"Voucher report: {voucher_code}"

    report = anvil.server.call("get_first_time_report", voucher_code)
    self.monthly_panel.items = report["monthly"]

    if report["monthly"]:
      chart_colors = Theme.chart_colors()
      self.usage_chart.data = [
        {
          "type": "bar",
          "x": [month["month_label"] for month in report["monthly"]],
          "y": [month["total_orders"] for month in report["monthly"]],
          "text": [str(month["total_orders"]) for month in report["monthly"]],
          "textposition": "outside",
          "customdata": [month["total_owing_display"] for month in report["monthly"]],
          "hovertemplate": "%{x}: %{y} use(s)<br>Payable: %{customdata}<extra></extra>",
          "marker": {"color": "#176b87"},
        }
      ]
      self.usage_chart.layout = {
        "height": 260,
        "margin": {"l": 40, "r": 20, "t": 20, "b": 60},
        "showlegend": False,
        "font": {"color": chart_colors["font"]},
        "xaxis": {"tickangle": -30},
        "yaxis": {"gridcolor": chart_colors["grid"], "zeroline": False, "rangemode": "tozero"},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
      }
      self.usage_heading.visible = True
      self.usage_chart.visible = True

    unmatched = report["unmatched_orders"]
    if unmatched:
      self.unmatched_label.text = (
        f"{len(unmatched)} order(s) using this voucher have no matching Sage account yet: "
        + ", ".join(unmatched)
      )
      self.unmatched_label.visible = True
