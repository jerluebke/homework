#coding=utf-8

##################################################
# TODO
# automate and adjust plotting
#   integrate config_grid and delete old file
# error handling
#   add errors to __repr__
# evaluation
#   error propagation
##################################################

# import matplotlib as mpl
# mpl.use('ps')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st


class Data():
    """Class for creating and handling data in pandas.DataFrame (df) objects"""

    # dict to store df
    _data = {}
    # dicts for error values corresbonding to self.data
    _x_errors = {}
    _y_errors = {}
    # DataFrame for linreg values of df from self.data
    # Is filled by self.make_linreg, where the df which are to be processed can
    # be specified 
    _lin_reg = pd.DataFrame(index=['slope', 'intercept', 'r_val', 'p_val', 'std_err'])

    # dicts for plotting, can be modified
    fig_kwds = dict(figsize=(12, 8))
    line_options = dict(color = 'blue',
                        linestyle = 'solid',
                        linewidth = .8,
                        zorder = 1)
    scatter_options = dict(#s = 6,      # markersize
                           #linewidth = .8,
                           facecolor = 'white',
                           edgecolors = 'blue',
                           marker = 'o',
                           zorder = 2)
    errorbar_options = dict(ecolor = 'black',
                            #elinewidth = .8,
                            capsize = 6,
                            #capthick = 1,
                            marker = 'o',
                            markeredgecolor = 'blue',
                            #markeredgewidth = .6,
                            markerfacecolor = 'white',
                            #markersize = 6,
                            #zorder = 2
                            linestyle = None)
    '''
    plt_kwds_mapping = dict(# Examples
                            default_line = dict(kind = 'line',
                                                **line_options,
                                                label = 'default line'),
                            default_scatter = dict(kind = 'scatter',
                                                   x = 'X', y = 'Y',  # columnnames
                                                   **scatter_options,
                                                   label = 'dafault scatter'),
                            default_error = dict(**errorbar_options,
                                                 title = 'default_errorbar',
                                                 #yerr = self._y_errors['example'],
                                                 #xerr = self._x_errors['example'],
                                                 xlim = (0, 20), ylim = (0, 10))
                           )
    '''
    plt_kwds_mapping = {}

    def __init__(self, *args, _sep='\t'):
        """Takes filenames of data sheets. For each one a df is created and
        stored in self.data, where its key is the given filename
        Adjust _sep, if needed"""
        for a in args:
            table = pd.read_table(a, sep=_sep)
            # save table in dict for easy processing
            self._data[a] = table
            # set table as attribute for easy access
            setattr(self, a, table)
            # init empty dict in self.plt_kwds_mapping
            self.plt_kwds_mapping[a] = {}

    @property
    def data(self):
        return self._data

    @property
    def lin_reg(self):
        return self._lin_reg

    @property
    def errors(self):
        self.repr_err()
        return {'x': self._x_errors, 'y': self._y_errors}

    def repr_err(self):
        """evaluate and print error values for each df and axis
        TODO: switch printing order of axis and df_id"""
        return_val = ''
        for i, err in enumerate((self._x_errors, self._y_errors)):
            return_val += '{} errors:\n'.format('X' if i==0 else 'Y')
            for df_id, e in err.items():
                return_val += '\t{}:\n'.format(df_id)
                df = self._data[df_id]
                d = df[df.columns[i]]
                if callable(e):
                    vals = [e(point) for point in d]
                elif isinstance(e, (float, int)):
                    vals = [e]*len(d)
                else:
                    vals = e
                for j, val in enumerate(vals):
                    return_val += '\t{0:<4}:\t\t{1:>}\n'.format(j, val)
                return_val += '\n'
            return_val += '\n\n'
        print(return_val)


    def __repr__(self):
        """Object representation
        Essentially prints self.data"""
        return_val = ''
        for df_id in self._data:
            return_val += df_id + '\n' + repr(self._data[df_id]) + '\n\n'
        return return_val

    def col_diff(self, df_id, col1, col2, new_col='diff_12', rm=False):
        """Adds difference of col1 and col2 of df as new column
        df is specified by df_id (its name)
        If desired, col1 and col2 can be deleted afterwards"""
        df = self._data[df_id]
        df[new_col] = np.abs(df[col1] - df[col2])
        if rm:
            del df[col1], df[col2]
        self._data[df_id] = df

    def apply_funcs(self, df_id, funcs, cols=None):
        """wrapper for df.aggregate"""
        df = self._data[df_id]
        if isinstance(cols, str):
            cols = [cols]
        if callable(funcs):
            funcs = [funcs]
        if not cols:
            self._data[df_id] = df.agg(funcs)
        else:
            kwds = {c:f for c, f in zip(cols, funcs)}
            self._data[df_id] = df.agg(kwds)

    def make_linreg(self, df_ids=[]):
        """Perform scipy.stats.linregress for df specified in df_ids
        If nothing is give, linreg is performed for all df in self.data"""
        if not df_ids:
            df_ids = self._data.keys()
        for di in df_ids:
            # The result of linregress needs to be converted to a list in order
            # to be added to the self.lin_reg df
            # Adds result in new column
            # Indices of self_linreg name the components of the result
            lr = list(st.linregress(self._data[di]))
            self._lin_reg[di] = lr

    def _plot_linreg(self, df_id, label=True):
        """for plotting linear regression
        returns x: np.linspace
                y: x*lr.slope+lr.intercept"""
        lr = self.lin_reg[df_id]
        kwds = self.plt_kwds_mapping[df_id]
        xlim = kwds.get('xlim')
        if not xlim:
            raise ValueError('x limits in plt_kwds_mapping[{}] not\
                             found!'.format(df_id))
        x = np.linspace(*xlim)
        y = lambda x: x * lr.slope + lr.intercept
        if label:
            return dict(xdata=x, ydata=y(x),
                        label='m={0}$\stackrel{+}{-}${1}'.format(lr.slope, lr.intercept))
        return x, y(x)

    def add_errors(self, df_id, err, which):
        """Adds error values to specified df (named by df_id)
        errors can be scalar, array-like or a callable function
        which specifies the axis to process the errors for (x or y)"""
        if df_id not in self._data:
            raise KeyError('{} is not found in the data dict. Add it\
                           first!'.format(df_id))
        if which not in ('x', 'y'):
            raise KeyError('´which´ needs to be ´x´ or ´y´!')
        if not (isinstance(err, float) or callable(err) or
                len(err)==len(self._data[df_id])):
            raise ValueError('error must be number, callable or array-like\
                             with the same length as the corresponding data')
        if which == 'x':
            self._x_errors[df_id] = err
        else:
            self._y_errors[df_id] = err

    def plot(self, which='all'):
        if which == 'all':
            which = self._data.keys()
        if isinstance(which, str):
            which = [which]
        for i, di in enumerate(which):
            kwds = self.plt_kwds_mapping[di]
            plot_linreg = kwds.get('plot_linreg', False)
            self._save_remove(kwds, 'plot_linreg')
            df = self._data[di]
            plt.figure(i, **self.fig_kwds)
            df.plot(**kwds)
            if plot_linreg:
                plt.plot(self._plot_linreg(di, label=True), **self.line_options)
            plt.legend(self.legend_options)

    def _save_remove(self, dict_, key_):
        """helper function to savely remove item form dict"""
        try:
            del dict_[key_]
        except KeyError:
            pass




d = Data('data_a1', 'data_a2a', 'data_a2b')
d.col_diff('data_a2a', 'U1', 'U2', 'U_H', rm=True)
d.col_diff('data_a2b', 'U1', 'U2', 'U_H', rm=True)
idx = lambda x: x
factor_e_minus5 = lambda x: x*1e-5
d.apply_funcs('data_a2a', [idx, factor_e_minus5], ['I', 'U_H'])
d.apply_funcs('data_a2b', [idx, factor_e_minus5], ['B', 'U_H'])
d.make_linreg()
d.add_errors('data_a1', 0.05, 'x')
du = [5, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
du = [0.005*10**(-u) for u in du]
d.add_errors('data_a1', du, 'y')
d.add_errors('data_a2a', 0.05, 'x')
d.add_errors('data_a2a', 0.01e-5, 'y')
d.add_errors('data_a2b', 0.5, 'x')
d.add_errors('data_a2b', 0.01e-5, 'y')
