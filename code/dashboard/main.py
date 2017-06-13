''' Create a simple stocks correlation dashboard.

Choose stocks to compare in the drop down widgets, and make selections
on the plots to update the summary and histograms accordingly.

.. note::
    Running this example requires downloading sample data. See
    the included `README`_ for more information.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve stocks

at your command prompt. Then navigate to the URL

    http://localhost:5006/stocks

.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md

'''
try:
    from functools import lru_cache
except ImportError:
    # Python 2 does stdlib does not have lru_cache so let's just
    # create a dummy decorator to avoid crashing
    print ("WARNING: Cache for this example is available on Python 3 only.")
    def lru_cache():
        def dec(f):
            def _(*args, **kws):
                return f(*args, **kws)
            return _
        return dec

from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure

DATA_DIR = join(dirname(__file__), 'daily')

DEFAULT_TICKERS = ['AAPL', 'GOOG', 'INTC', 'BRCM', 'YHOO']

k2_c2 = pd.read_csv('/Users/gully/GitHub/kinder/analysis/K2C02_YSO_sim_WISE.csv')
k2_c2_periods = pd.read_csv('/Users/gully/GitHub/kinder/analysis/K2C02_periods.csv')

k2_subset = k2_c2_periods[['EPIC_ID', 'top_MT_per00', 'top_MT_per01']]

def nix(val, lst):
    return [x for x in lst if x != val]

@lru_cache()
def load_ticker(ticker):
    fname = join(DATA_DIR, 'table_%s.csv' % ticker.lower())
    data = pd.read_csv(fname, header=None, parse_dates=['date'],
                       names=['date', 'foo', 'o', 'h', 'l', 'c', 'v'])
    data = data.set_index('date')
    return pd.DataFrame({ticker: data.c, ticker+'_returns': data.c.diff()})

@lru_cache()
def get_data(t1, t2):
    data = k2_subset
    return data

# set up widgets

stats = PreText(text='', width=500)
ticker1 = Select(value='AAPL', options=nix('GOOG', DEFAULT_TICKERS))
ticker2 = Select(value='GOOG', options=nix('AAPL', DEFAULT_TICKERS))

# set up plots

source = ColumnDataSource(data=dict(date=[], t1=[], t2=[], t1_returns=[], t2_returns=[]))
source_static = ColumnDataSource(data=dict(time=[], flux=[]))
tools = 'pan,wheel_zoom,xbox_select,reset'

corr = figure(plot_width=350, plot_height=350,
              tools='pan,tap,wheel_zoom,box_select,reset')
corr.circle('top_MT_per00', 'top_MT_per01', size=10, source=source,
            selection_color="orange", alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.8)

ts1 = figure(plot_width=900, plot_height=200, tools=tools, active_drag="xbox_select")
ts1.line('time', 'flux', source=source_static)


# set up callbacks

def ticker1_change(attrname, old, new):
    update()


def update(selected=None):
    t1, t2 = ticker1.value, 'GOOG'

    data = get_data(t1, t2)
    source.data = source.from_df(data[['top_MT_per00', 'top_MT_per01']])
    path1 = '/Users/gully/GitHub/kinder/data/'
    file1 = 'hlsp_k2sff_k2_lightcurve_205657404-c02_kepler_v1_llc-default-aper.txt'
    df = pd.read_csv(path1+file1, index_col=False, names=['time', 'flux'], skiprows=1)
    source_static.data = source_static.from_df(df)

    corr.title.text = 'Lomb-Scargle Period 1 vs 2'
    ts1.title.text = 'Lightcurve'

ticker1.on_change('value', ticker1_change)

def selection_change(attrname, old, new):
    t1, t2 = ticker1.value, ticker2.value
    data = get_data(t1, t2)
    selected = source.selected['1d']['indices']
    print(selected, k2_c2.fname[selected].values[0][8:])
    path1 = '/Users/gully/GitHub/kinder/data/'
    file1 = k2_c2.fname[selected].values[0][8:]
    df = pd.read_csv(path1+file1, index_col=False, names=['time', 'flux'], skiprows=1)
    source_static.data = source_static.from_df(df)
    #if selected:
    #    data = data.iloc[selected, :]
    #update_stats(data, t1, t2)

source.on_change('selected', selection_change)

# set up layout
widgets = column(ticker1)
main_row = row(corr, widgets)
series = column(ts1)
layout = column(main_row, series)

# initialize
update()

curdoc().add_root(layout)
curdoc().title = "Stocks"
