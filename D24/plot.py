#coding=utf-8

"""
Process D24-data
"""

from matplotlib.lines import Line2D
import numpy as np
from PlotHelper import Data

d = Data('data_a1', 'data_a2a', 'data_a2b')
d.col_diff('data_a2a', 'U1', 'U2', 'U_H', rm=True)
d.col_diff('data_a2b', 'U1', 'U2', 'U_H', rm=True)
idx = lambda x: x
def make_factor(f):
    return lambda x: x*f
d.apply_funcs('data_a2a', make_factor(1e-5), 'U_H')
d.apply_funcs('data_a2b', make_factor(1e-5), 'U_H')
d.apply_funcs('data_a2b', make_factor(1e-3), 'B')
d.make_linreg()
# d.add_errors('data_a1', 0.05, 'x')
# du = [5, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
# du = [0.005*10**(-u) for u in du]
# d.add_errors('data_a1', du, 'y')

lr_a1 = d.lin_reg.data_a1
lr_a2a = d.lin_reg.data_a2a
lr_a2b = d.lin_reg.data_a2b
lr_label_dict = dict(data_a1='{:.3e} $\pm$ {:.1e}'.format(lr_a1.slope, lr_a1.std_err),
                     data_a2a='{:.2e} $\pm$ {:.1e}'.format(lr_a2a.slope, lr_a2a.std_err),
                     data_a2b='{:.2e} $\pm$ {:.1e}'.format(lr_a2b.slope, lr_a2b.std_err))

for di, l in lr_label_dict.items():
    d.plt_kwds_mapping[di].update({
            'legend_params':dict(
                    handles=[Line2D([], [], c='r', ls='', marker='o',
                                    fillstyle='none', label='Messpunkte'),
                             Line2D([], [], c='b', ls='-',
                                    label='Regressionsgerade\nSteigung: {}'.format(l))
                             ],
                    numpoints=2)
            })

titles = dict(data_a1 = 'Bestimmung der Leitfähigkeit von Kupfer\nU gegen I\n',
              data_a2a = 'Hallspannung in Abhängigkeit des Querstroms\n',
              data_a2b = 'Hallspannung in Abhängigkeit des Magnetfeldes\n')
for di, t in titles.items():
    d.plt_kwds_mapping[di].update({'title':t})

d.ax_kwds_mapping['data_a1'] = dict(xlim=(-.5, 20.5), ylim=(-0.002, 0.053),
                                    xlabel='I/A', ylabel='U/A')
# d.add_errors('data_a2a', 0.05, 'x')
d.add_errors('data_a2a', 0.01e-5, 'y')
d.ax_kwds_mapping['data_a2a'] = dict(xlim=(.5, 12.5), ylim=(0, 5e-6),
                                     xlabel=r'$I_{quer}$/A', ylabel=r'$U_{H}$/$\mu$V')
# d.add_errors('data_a2b', 0.5e-3, 'x')
d.add_errors('data_a2b', 0.01e-5, 'y')
d.ax_kwds_mapping['data_a2b'] = dict(xlim=(.08, .42), ylim=(5e-7, 3.5e-6),
                                     xlabel=r'B/mT', ylabel=r'$U_{H}$/$\mu$V')

def do_plotting():
    d.plot()
    d.data_a2a_plot.ax.set_yticklabels([i for i in np.arange(6)])
    d.data_a2b_plot.ax.set_xticklabels([i for i in np.arange(50, 450, 50)])
    d.data_a2b_plot.ax.set_yticklabels([i for i in np.arange(0.5, 4, 0.5)])

# d.save()
