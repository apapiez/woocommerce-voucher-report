from ._anvil_designer import MonthlyCountRowTemplate
from anvil import *

FIRST_TIME_COLOR = "#2a78d6"
REPEAT_COLOR = "#eb6834"


class MonthlyCountRow(MonthlyCountRowTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)

    first_time_count = self.item["first_time_count"]
    repeat_count = self.item["total_orders"] - first_time_count

    self.chart.data = [
      {
        "type": "bar",
        "orientation": "h",
        "name": "First-time",
        "x": [first_time_count],
        "y": [""],
        "text": [str(first_time_count)],
        "textposition": "inside",
        "insidetextfont": {"color": "#ffffff"},
        "hovertemplate": "First-time: %{x}<extra></extra>",
        "marker": {"color": FIRST_TIME_COLOR, "line": {"color": "#ffffff", "width": 1}},
      },
      {
        "type": "bar",
        "orientation": "h",
        "name": "Repeat",
        "x": [repeat_count],
        "y": [""],
        "text": [str(repeat_count)],
        "textposition": "inside",
        "insidetextfont": {"color": "#ffffff"},
        "hovertemplate": "Repeat: %{x}<extra></extra>",
        "marker": {"color": REPEAT_COLOR, "line": {"color": "#ffffff", "width": 1}},
      },
    ]
    self.chart.layout = {
      "barmode": "stack",
      "showlegend": True,
      "legend": {"orientation": "h", "y": -0.3},
      "height": 110,
      "margin": {"l": 10, "r": 10, "t": 10, "b": 30},
      "xaxis": {"visible": False},
      "yaxis": {"visible": False},
      "paper_bgcolor": "rgba(0,0,0,0)",
      "plot_bgcolor": "rgba(0,0,0,0)",
    }
