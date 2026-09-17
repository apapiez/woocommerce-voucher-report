from ._anvil_designer import MonthlyCountRowTemplate
from anvil import *

from .. import Theme

FIRST_TIME_COLOR = "#2a78d6"
REPEAT_COLOR = "#eb6834"


class MonthlyCountRow(MonthlyCountRowTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.expanded = False
    self.chart_rendered = False
    self.details_panel.visible = False
    self.caret_label.text = "▸"

  def header_click(self, event):
    self.expanded = not self.expanded
    self.details_panel.visible = self.expanded
    self.caret_label.text = "▾" if self.expanded else "▸"

    if self.expanded and not self.chart_rendered:
      self._render_chart()
      self.chart_rendered = True

  def _render_chart(self):
    first_time_count = self.item["first_time_count"]
    repeat_count = self.item["total_orders"] - first_time_count

    self.chart.data = [
      {
        "type": "pie",
        "labels": ["First-time", "Repeat"],
        "values": [first_time_count, repeat_count],
        "sort": False,
        "textinfo": "value",
        "textfont": {"color": "#ffffff"},
        "hovertemplate": "%{label}: %{value}<extra></extra>",
        "marker": {
          "colors": [FIRST_TIME_COLOR, REPEAT_COLOR],
          "line": {"color": "#ffffff", "width": 2},
        },
      },
    ]
    self.chart.layout = {
      "showlegend": True,
      "legend": {"orientation": "h", "y": -0.1},
      "height": 200,
      "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
      "font": {"color": Theme.chart_colors()["font"]},
      "paper_bgcolor": "rgba(0,0,0,0)",
      "plot_bgcolor": "rgba(0,0,0,0)",
    }
