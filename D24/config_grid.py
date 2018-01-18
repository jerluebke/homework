#coding=utf-8

import matplotlib.pyplot as plt

def set_grid(ax):
    ax.minorticks_on()
    ax.grid(
        which='major', color='gray',
        linewidth=0.5, linestyle='-'
        )
    ax.grid(
        which='minor', color='gray',
        linewidth=0.25, linestyle=':'
        )
    return ax
