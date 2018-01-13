#coding=utf-8

import sys
import matplotlib as mpl
mpl.use('ps')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress

sys.path.append('/home/jeremiah/Dokumente/Studium/G-Praktikum/')
from config_grid import set_grid


x = np.linspace(-2, 80)
d = pd.read_table('data', sep=',')
c = d.columns

def y(col):
    """calc y values: N(x)/N(0)"""
    return np.array([elem/col[0] for elem in col])

def lr(y_data, x_data=d[c[0]], s0=None, s1=None):
    """do linear regression
    s0 and s1 are for adjusting the data with slicing,
    i.e. y = y[s0:s1]"""
    if not (s0 or s1):
        return linregress(x_data, np.log(y(y_data)))
    return linregress(x_data[s0:s1], np.log(y(y_data[s0:s1])))

pp = lr(d['pp'])
ct = lr(np.array(d['ct']), s0=2)
cc = lr(d['cc'])

def make_cmap(cmap, ids):
    return [cmap(i) for i in ids]

cmap = plt.get_cmap('tab20')
scatter_colors = make_cmap(cmap, (0, 6, 4))
plot_colors = make_cmap(cmap, (1, 7, 5))


def scatter_data(colors=scatter_colors, sizes=(90, 65, 40),
                 kwds=dict(marker='o', c='white')):
    for elem, clr, sz in zip(c[1:], colors, sizes):
        plt.scatter(d[c[0]], y(d[elem]), edgecolors=clr, s=sz,
                    **kwds, zorder=2)


def plot_linreg(lr_data=(pp, ct, cc), names=('PP', 'CT', 'CC'),
                offset=(0, -0.15, 0), colors=plot_colors,
                labels=('', '_{eff}', '_{eff}'), kwds=dict()):
    for l, n, o, cl, lb in zip(lr_data, names, offset, colors, labels):
        plt.plot(x, np.exp(l[0]*x+l[1]+o), color=cl,
                 label='{0}, $\mu{1}$={2:.4f}'.format(n, lb, abs(l[0])),
                 **kwds, zorder=1)
    plt.legend()


def do_plotting():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = set_grid(ax)

    ax.set_yscale('log', basey=np.e)
    ticks = lambda x, pos: r'$e^{{{0}}}$'.format(int(np.log(x)))
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(ticks))

    plt.title(r'Ereignismenge $\frac{N(x)}{N(0)}$ gegen Absorberdicke d'
          +'\nHalblogarithmisch zur Basis e\n')
    plt.xlabel(r'$d/mm$')
    plt.ylabel(r'$\frac{N(x)}{N(0)}$')
    plt.xlim(-2, 80)

    plot_linreg()
    scatter_data()


def save(name):
    do_plotting()
    plt.savefig(name+'.ps', dpi=100, papertype='a4', orientation='landscape')


def print_eval(data=(pp, ct, cc), names=c[1:]):
    print('\nname', 'mu', 'stderr', 'rel', 'r-val', 'r-val**2\n', sep='\t')
    for d, n in zip(data, names):
        print(n, '{0:.4f}  {1:.4f}  {2:.3f}%  {3:.4f}  {4:.4f}'.format(
              abs(d[0]), d[4], abs(d[4]/d[0])*100, abs(d[2]), d[2]**2), sep='\t')
    print()
