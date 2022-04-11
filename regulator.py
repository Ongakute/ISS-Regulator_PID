import math
from bokeh.plotting import ColumnDataSource,figure, show
from bokeh.models import CustomJS, Slider, Button
from bokeh.layouts import column, row
from bokeh.io import curdoc

global source


def wykres():
  X, Y, Z, Q = obliczenia(0.15, 3.0, 0.025, 8.0, 3.0)
  source = ColumnDataSource(data=dict(x=X, y=Y))
  source2 = ColumnDataSource(data=dict(x=X, y=Z))
  source3 = ColumnDataSource(data=dict(x=X, y=Q))
  p = figure(plot_width=600, plot_height=600, title="H")
  p.line(source=source, line_width=2)
  p2 = figure(plot_width=600, plot_height=600, title="e")
  p2.line(source=source2, line_width=2)
  p3 = figure(plot_width=600, plot_height=600, title="Qd")
  p3.line(source=source3, line_width=2)

  kpSlider = Slider(title="kp", value=0.15, start=0.05, end=1.0, step=0.05)
  unSlider = Slider(title="un", value=3.0, start=0.5, end=10.0, step=0.5)
  TpSlider = Slider(title="Tp", value=0.025, start=0.005, end=1.0, step=0.005)
  TiSlider = Slider(title="Ti", value=8.0, start=0.5, end=20.0, step=0.5)
  TdSlider = Slider(title="Td", value=3.0, start=0.5, end=20.0, step=0.5)

  def update_data(event):
    kp = kpSlider.value
    un = unSlider.value
    Tp = TpSlider.value
    Ti = TiSlider.value
    Td = TdSlider.value

    X, Y,Z,Q = obliczenia(kp, un, Tp, Ti, Td)
    source.data = dict(x=X, y=Y)
    source2.data = dict(x=X, y=Z)
    source3.data = dict(x=X, y=Q)

  button = Button(label = "Calculate")
  button.on_click(update_data)

  inputs = column(kpSlider, unSlider, TpSlider, TiSlider, TdSlider, button)
  inputs2 = column(p,p2,p3)
  curdoc().add_root(row(inputs, inputs2))
  

  

def obliczenia(kp, un, Tp, Ti, Td):
  n = 1
  hn = [1.5]
  e = [0.0]
  Qd = [0.0]
  x = [0]
  for i in range(1,25000):
    e.append(un - hn[-1])
    x.append(i)
    Ui = (Tp / Ti) * sum(e)
    Ud = (Td / Tp )* (e[n] - e[n-1])
    Up = kp * (e[n] + Ui + Ud)
    Qd.append(0.005 * Up)
    n = n + 1
    hn.append(hn[-1] + Qd[-1])
  return (x, hn,e,Qd)
  
  wykres() 

wykres()