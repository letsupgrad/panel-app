import panel as pn
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import threading
import time

pn.extension(sizing_mode="stretch_width")

# ----- STYLES -----
pn.config.raw_css.append("""
body {
    background-color: #f0f2f5;
}
h2 {
    color: #2c3e50;
    font-size: 28px;
    font-family: 'Segoe UI', sans-serif;
    margin-bottom: 15px;
}
.pn-styled-box {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
""")

# ----- Chart 1: Dynamic Sine Wave -----
x = np.linspace(0, 4 * np.pi, 100)
y = np.sin(x)

plot1 = figure(title="Dynamic Sine Wave", width=700, height=300)
line = plot1.line(x, y, line_width=2, color="dodgerblue")

slider = pn.widgets.FloatSlider(name="Amplitude", start=0.1, end=5, value=1.0)

def update_amplitude(event):
    line.data_source.data['y'] = slider.value * np.sin(x)

slider.param.watch(update_amplitude, 'value')

# ----- Chart 2: Real-time Streaming -----
source = ColumnDataSource(data={'x': [], 'y': []})

plot2 = figure(title="Real-time Sensor Stream", width=700, height=300,
               x_axis_label='Time (s)', y_axis_label='Sensor Value')
plot2.line('x', 'y', source=source, line_width=2, color="seagreen")

def stream_data():
    t = 0
    while True:
        new_x = [t]
        new_y = [np.sin(t) + np.random.normal(0, 0.2)]
        source.stream({'x': new_x, 'y': new_y}, rollover=200)
        t += 0.1
        time.sleep(0.1)

thread = threading.Thread(target=stream_data)
thread.daemon = True
thread.start()

# ----- Layout -----
dashboard = pn.Column(
    pn.Spacer(height=20),
    pn.pane.Markdown("## 🚀 Smart IoT Dashboard"),
    pn.Row(
        pn.Column(
            pn.pane.Markdown("### 📈 Amplitude Control"),
            slider,
            plot1,
            css_classes=["pn-styled-box"]
        ),
        pn.Column(
            pn.pane.Markdown("### 🔁 Real-time Feed"),
            plot2,
            css_classes=["pn-styled-box"]
        )
    ),
    sizing_mode="stretch_width"
)

dashboard.servable()
