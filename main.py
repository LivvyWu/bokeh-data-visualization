from bokeh.client import push_session
from bokeh.io import curdoc
import pandas as pd
from bokeh.charts import Line, show, output_notebook
from bokeh.models.widgets import Select
from bokeh.plotting import Figure, ColumnDataSource
from bokeh.layouts import column, row
from bokeh.models import HoverTool, NumeralTickFormatter, LinearAxis, Range1d

fruit=[("pineapple","鳳梨"),("strawberry","草莓")]
select = Select(title="水果", value="pineapple", options=fruit)

output_notebook()
df = pd.read_excel('fruit_price.xls',sheetname=None)

def select_fruit(fruit_val):
    return dict(
        date = df[fruit_val]['date'],
        amt = [str(x*y) for x,y in zip(df[fruit_val]['QTY'], df[fruit_val]['avg_price'])],
        price=df[fruit_val]['avg_price'],
        qty=df[fruit_val]['QTY'],
        tipdate=[x.strftime("%Y-%m-%d") for x in df[fruit_val]['date']]
    )
source = ColumnDataSource(data=select_fruit(select.value))

def update(attr, old, new):
    source.data = select_fruit(select.value)
select.on_change('value', update)    

TOOLS = ['box_zoom', 'box_select', 'wheel_zoom', 'reset', 'pan', 'resize', 'save']
hover = HoverTool(
        tooltips=[
            ("DATE", "@tipdate"),
            ("AVG_PRICE","@price"),
            ("QTY", "@qty"),
            ("AMOUNT", "@amt")
        ]
    )

f2 = Figure(plot_width=1200, plot_height=600, x_axis_type="datetime", x_axis_label='日期', y_axis_label='交易量 x 價格',tools=TOOLS +[hover])
#f2.line('date','amt', line_width=3, source = source)
f2.yaxis.formatter = NumeralTickFormatter(format="0,000")
f2.line('date','amt', line_width=3, source = source)
f2.yaxis.formatter = NumeralTickFormatter(format="0,000")


layout = column(row(select, width=400), row(f2))

curdoc().add_root(layout)
