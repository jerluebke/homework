#coding=utf-8

import matplotlib
matplotlib.use('ps')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def plot_phase_trajectories(f, inits, xbound, ybound, t=(0, 10), steps=100,
                            axis=None,
                            sivp_kwargs={}, plt_kwargs={'c': 'b', 'lw': .7}):
    """Plots phase trajectory of given ODE with scipy.integrate.solve_ivp
    Returns list of matplotlib-artist objects"""
    if axis is None:
        axis = plt.gca()

    def f_neg(t, x):
        # for solution backwards in time
        return -f(t, x)

    artists = []
    tt = np.linspace(*t, steps)
    for ff in (f, f_neg):
        for i in inits:
            # solve_ivp(..., dense_output=True).sol holds a ´OdeSolution´ object
            # which interpolates the solution and allows its evaluation at
            # arbitrary points
            # Returns array with shape(n,) corresponding to the RHS of the
            # given ODE
            sol = solve_ivp(ff, t, i, dense_output=1, **sivp_kwargs).sol
            sol_eval = sol(tt)
            sol_x_ma = np.ma.masked_outside(sol_eval[0], *xbound)
            sol_y_ma = np.ma.masked_outside(sol_eval[1], *ybound)
            artists.append(axis.plot(sol_x_ma, sol_y_ma, **plt_kwargs))

    axis.set_xlim(xbound)
    axis.set_ylim(ybound)
    return artists


ppt = plot_phase_trajectories


inits = lambda a, e, s: np.array([(i, j) for i in np.arange(1, 4)
                                  for j in np.arange(a, e, s)])


def kepler(t, x, c=2):
    u, v = x
    du = v
    dv = 1 / u - c / u**2
    return np.array([du, dv])


def duffing(t, x):
    u, v = x
    du = v
    dv = (u**3)/6 - u
    return np.array([du, dv])


def make_plot(name='phase_plot'):
    f, axarr = plt.subplots(2, figsize=(8, 12))
    for f, i, b, a, t in zip((kepler, duffing),             # function
                            ((-1.5, 2, .5), (-2, 3, 1)),    # initial values
                                                            #  (start, stop, step)
                            (((0, 4), (-3, 3)),             # boundaries
                             ((-4, 4), (-3, 3))),
                            axarr,                          # axis
                            ('Kepler', 'Duffing')):         # title
        ppt(f, inits(*i), b[0], b[1], axis=a)
        a.set_title(t)
        a.grid(True)
    plt.savefig(name+'.ps', dpi=100, papertype='a4', orientation='portrait')


# ~$ python3 -c "import code_15012018 as code; code.make_plot('name')"
