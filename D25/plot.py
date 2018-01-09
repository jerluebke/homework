#coding=utf-8

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress


x = np.linspace(0, 80)
d = pd.read_table('data', sep=',')
c = d.columns

def y(col):
    return np.array([elem/col[0] for elem in col])

def lr(y_data, x_data=d[c[0]], s0=None, s1=None):
    if not (s0 or s1):
        return linregress(x_data, np.log(y(y_data)))
    return linregress(x_data[s0:s1], np.log(y(y_data[s0:s1])))

pp = lr(d['pp'])
ct = lr(np.array(d['ct']), s0=2)
cc = lr(d['cc'])


def scatter_data():
    for elem in c[1:]:
        plt.scatter(d[c[0]], y(d[elem]), marker='o')

def plot_linreg(lr_data=(pp, ct, cc), names=c[1:], offset=(0, -0.15, 0)):
    for l, n, o in zip(lr_data, names, offset):
        plt.plot(x, np.exp(l[0]*x+l[1]+o), label='{}, mu={}'.format(n, l[0]))
    plt.legend()


plt.gca()
# plt.yscale('log', basey=np.e)
plt.yscale('log')   # base 10
