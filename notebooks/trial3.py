# %load https://raw.githubusercontent.com/bokeh/bokeh/master/examples/app/sliders.py
''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve sliders.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/sliders

in your browser.

'''
import numpy as np

from bokeh.plotting import Figure, hplot, vplot
from bokeh.models import ColumnDataSource, HBox, VBoxForm
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc

import pandas as pd

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)

file_list_raw = pd.read_csv('file_list.csv', names=['fname'])
file_list = file_list_raw.fname.values

k2c2_yso_all_info = pd.read_csv('../analysis/K2C02_YSO_kplr_match.csv')


file = file_list[5]
raw_lc = pd.read_csv(file, index_col=False)

xlc = raw_lc['BJD - 2454833'].values
ylc = raw_lc[' Corrected Flux'].values

xx = k2c2_yso_all_info.logiqr.values
yy = k2c2_yso_all_info.logstd.values

x0 = xx[0:1]
y0 = yy[0:1]

source = ColumnDataSource(data=dict(x=x0, y=y0))
source2 = ColumnDataSource(data=dict(x=xlc, y=ylc))


# Set up plot
plot = Figure(tools="crosshair,pan,reset,resize,save,wheel_zoom",
              plot_width=400, plot_height=400, title=None,
              x_range=[-4, 0], y_range=[-4, 0])

plot2 = Figure(tools="crosshair,pan,reset,resize,save,wheel_zoom",
               plot_width=400, plot_height=400, title=None,
              x_range=[2060, 2105], y_range=[0.95, 1.05])


plot.scatter(xx, yy, size=3, color="#3A5785", alpha=0.1)
plot.scatter('x', 'y', source=source, size=15, color="#FF0000", alpha=1.0)

plot2.line('x', 'y', source=source2, line_width=3, line_alpha=0.6)

# Set up widgets
offset = Slider(title="offset", value=0, start=0, end=200, step=1)

#layout = hplot(plot, plot2, width=800, height=500)


def update_data(attrname, old, new):

    # Get the current slider values
    b = offset.value

    file = file_list[b]
    raw_lc = pd.read_csv(file, index_col=False)

    xlc = raw_lc['BJD - 2454833'].values
    ylc = raw_lc[' Corrected Flux'].values

    source.data = dict(x=xx[b:b+1], y=yy[b:b+1])
    source2.data = dict(x=xlc, y=ylc)

for w in [offset]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = VBoxForm(children=[offset])

curdoc().add_root(HBox(children=[inputs, plot, plot2], width=1200))

