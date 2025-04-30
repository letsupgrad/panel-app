import panel as pn
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import time
import threading

pn.extension()

# Static sine wave plot
x = np.linspace(0, 4 * np.pi, 100)
y = np.sin(x)

plot = figure(title="Interactive Sine Wave", width=700, height=300)
line = plot.line(x, y)

slider = pn.widgets.FloatSlider(name="Amplitude", start=0.1, end=5, value=1.0)

def update_plot(event):
    amp = slider.value
    line.data_source.data['y'] = amp * np.sin(x)

slider.param.watch(update_plot, 'value')

# ---- Time Series Chart with Animation ----
time_plot = figure(title="Real-time Sine Wave", width=700, height=300, x_axis_label='Time', y_axis_label='Value')
source = ColumnDataSource(data={'x': [], 'y': []})
time_line = time_plot.line('x', 'y', source=source)

def update_time_series():
    t = 0
    while True:
        new_x = [t]
        new_y = [np.sin(t)]
        source.stream({'x': new_x, 'y': new_y}, rollover=200)
        t += 0.1
        time.sleep(0.1)

# Start time series update in background
thread = threading.Thread(target=update_time_series)
thread.daemon = True
thread.start()

# Layout
layout = pn.Column(
    "# Panel App with Animated Time Series",
    slider,
    plot,
    pn.Spacer(height=20),
    time_plot
)

layout.servable()
