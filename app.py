import panel as pn
import numpy as np
from bokeh.plotting import figure

pn.extension()

x = np.linspace(0, 4 * np.pi, 100)
y = np.sin(x)

plot = figure(title="Interactive Sine Wave", width=700, height=300)
line = plot.line(x, y)

slider = pn.widgets.FloatSlider(name="Amplitude", start=0.1, end=5, value=1.0)

def update_plot(event):
    amp = slider.value
    line.data_source.data['y'] = amp * np.sin(x)

slider.param.watch(update_plot, 'value')

layout = pn.Column("# Panel App", slider, plot)
layout.servable()
