#coding=utf-8

##################################################
# TODO
# evaluation
#   error propagation
# refactor
#   save Data and PlotHelper as Library
#   and put evaluation of D24 in seperate file
# some Unittests would propably be nice
##################################################

import matplotlib as mpl
mpl.use('ps')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st

from matplotlib.lines import Line2D


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
    _lin_reg = pd.DataFrame(index=['slope', 'intercept', 'r_val', 'p_val',
                                   'std_err'])

    # dicts to hand specific kwds for each df to PlotHelper
    ax_kwds_mapping = {}
    plt_kwds_mapping = {}
    # dicts to store the plots
    plots = {}

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
            # init empty dict in self.ax_kwds_mapping and in
            # self.plt_kwds_mapping
            self.ax_kwds_mapping[a] = {}
            self.plt_kwds_mapping[a] = {'label':'Messpunkte'}

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
            return_val += '{} errors:\n'.format('X' if i == 0 else 'Y')
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

    def apply_funcs(self, df_id, func, col):
        """apply function on single column"""
        df = self._data[df_id][col]
        self._data[df_id][col] = func(df)

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
                len(err) == len(self._data[df_id])):
            raise ValueError('error must be number, callable or array-like\
                             with the same length as the corresponding data')
        if which == 'x':
            self._x_errors[df_id] = err
        else:
            self._y_errors[df_id] = err

    def plot(self, which='all'):
        if which == 'all':
            # get all df_ids
            which = self._data.keys()
        if isinstance(which, str):
            # if only one string is provided, make it an iterable
            which = [which]
        for i, di in enumerate(which):
            # get plt_kwds for df
            kwds = self.plt_kwds_mapping[di]
            # make params dict to pass to PlotHelper
            params = dict(dataframe = self._data[di],
                          yerr = self._y_errors.get(di),
                          xerr = self._x_errors.get(di),
                          lin_reg = self.lin_reg.get(di),
                          lr_label = kwds.get('lr_label'),
                          legend_params = kwds.get('legend_params', ''))
            # remove the entries which would cause trouble
            self._savely_remove(kwds, 'legend_params')
            self._savely_remove(kwds, 'lr_label')
            # add the rest
            if kwds.get('func', False):
                params['func'] = kwds['func']
                self._savely_remove(kwds, 'func')
            # give params to PlotHelper and save object
            setattr(self, '{}_plot'.format(di),
                    PlotHelper(**params, plotting_params=kwds, **self.ax_kwds_mapping[di]))

    def save(self, **save_kwds):
            # =dict(orientation='landscape', papertype='a4')):
        if plt.get_backend() != 'ps':
            print('You might want to set the backend to ´ps´ for saving the figure.')
        for di in self._data.keys():
            try:
                ph = getattr(self, '{}_plot'.format(di))
            except AttributeError:
                continue
            ph.fig.savefig('{}.ps'.format(di), **save_kwds)

    def _savely_remove(self, dict_, key_):
        """helper function to savely remove entry from dict"""
        try:
            del dict_[key_]
        except KeyError:
            pass



class PlotHelper:
    """class for creating and handling the plots"""
    # these dicts hold default information for plotting
    # to be adjusted and expanded according to what is needed
    _fig_params = dict(figsize = (12, 8),
                       dpi = 100)
    _line_options = dict(color = 'blue',
                         linestyle = 'solid',
                         linewidth = 1,
                         zorder = 2)
    _scatter_options = dict(s = 80,      # markersize
                            linewidth = 1,
                            facecolor = 'white',
                            edgecolors = 'red',
                            marker = 'o',
                            zorder = 3)
    _errorbar_options = dict(ecolor = 'black',
                             #elinewidth = .8,
                             capsize = 5,
                             #capthick = 1,
                             marker = 'o',
                             markeredgecolor = 'red',
                             markeredgewidth = 1,
                             markerfacecolor = 'white',
                             markersize = 8,
                             zorder = 3,
                             linestyle = ' ')
    _grid_major = dict(which = 'major',
                       color = 'gray',
                       linewidth = 0.5,
                       linestyle = '-')
    _grid_minor = dict(which = 'minor',
                       color = 'gray',
                       linewidth = 0.25,
                       linestyle = ':')
    # map function to its options-dict
    # to be expanded
    func_mapping = dict(line = (plt.plot, _line_options),
                        scatter = (plt.scatter, _scatter_options),
                        errorbar = (plt.errorbar, _errorbar_options))

    def __init__(self,
                 dataframe,
                 yerr=None, xerr=None,
                 lin_reg=None, lr_label=None,
                 func='errorbar',
                 plotting_params=None,
                 legend_params=None,
                 save=False,
                 **axis_params):
        """
        =========
        Arguments
        =========
        dataframe    :  pandas.DataFrame containing data to be plotted
        errors       :  scalar, array-like or callable for ´plt.errorbar´
        lin_reg      :  Object with linear regression data
        func         :  a pyplot function for plotting
                        (currently available: ´plot´, ´scatter´, ´errorbar´;
                        for more expand ´self.func_mapping´)
        plotting_params :  parameters to pass to the chosen pyplot function
        legend_params:  parameters to control the legend
        axis_params  :  parameters to control behaviour of the used axis
        """
        # extract data
        self.cols = dataframe.columns
        self.x = dataframe[self.cols[0]]
        self.y = dataframe[self.cols[1]]
        # set axis_params, merge default with given
        self.axis_params = {**dict(xlim = (min(self.x), max(self.x)),
                                   ylim = (min(self.y), max(self.y)),
                                   xlabel = self.cols[0],
                                   ylabel = self.cols[1]),
                            **axis_params}
        # get desired pyplot function from func_mapping and
        # merge plotting params from default and given values
        if func in self.func_mapping:
            self.func = self.func_mapping[func][0]
            self.plotting_params = dict(**self.func_mapping[func][1],
                                        **plotting_params)
        else:
            raise KeyError('{} not found in func_mapping! Implement it first.'\
                           .format(func))
        # make figure and axis and store them as attributes
        self.fig, self.ax = plt.subplots(subplot_kw=self.axis_params,
                                         **self._fig_params)
        # add error data in case an errorbar is to be plotted
        if func == 'errorbar':
            self.plotting_params['yerr'] = yerr
            self.plotting_params['xerr'] = xerr
        # store given params for later use as instance attributes
        self.lin_reg = lin_reg
        self.lr_label = lr_label
        self.legend_params = legend_params
        # invoke plotting
        self.plot()

    def plot(self, clear=True):
        # clear axis befor plotting again
        if clear:
            self.ax.cla()
        # do the actual plotting here
        # func is a pyplot function
        self.func(self.x, self.y, **self.plotting_params)
        # for some reason the following entries appear in axis_params (I
        # HAVE NO IDEA, WHERE THEY COME FROM!) and those fuckers make
        # trouble, so they have to be removed befor passing the dict to the
        # axis
        # fuckers
        for prop in ('sharey', 'sharex'):
            if prop in self.axis_params:
                del self.axis_params[prop]
        self.ax.set(**self.axis_params)
        # plot linear regression if provided
        if self.lin_reg is not None:
            if not self.lr_label:
                self.lr_label = r'm={0}$\pm${1}'.format(self.lin_reg.slope,
                                                        self.lin_reg.std_err)
            xlim = self.axis_params.get('xlim')
            x_span = np.linspace(*xlim)
            y_vals = lambda x: x * self.lin_reg.slope + self.lin_reg.intercept
            self.ax.plot(x_span, y_vals(x_span), label=self.lr_label,
                         **self._line_options)
        # make grid
        self.set_grid()
        # if not legend params are not specified, make legend without arguments
        # to avoid misbehaviour
        if self.legend_params:
            plt.legend(**self.legend_params)
        else:
            plt.legend()

    def set_grid(self):
        self.ax.grid(**self._grid_major)
        if any(self._grid_minor):
            self.ax.minorticks_on()
            self.ax.grid(**self._grid_minor)

    def add_text_with_newline_using_latex(self, text_with_newline):
        # For some reason it is not possible to add a newline (it
        # just gives a huge traceback, even with usetex=False)
        # Since I'm tired of this shit and I have better things to debug
        # this shit, I'm just solving it with this ugly hack hoping it
        # won't break any other shit...
        # Note: text.latex.preview should be False in any other case!
        # Otherwith just some ugly shit happens
        # fuckers...
        mpl.rcParams['text.latex.preview'] = True
        self.ax.set_title(text_with_newline)
        mpl.rcParams['text.latex.preview'] = False

    # an alias for above function since I don't even consider typing this
    # long ass name every fucking time I need it
    # so here you go...
    atwnul = add_text_with_newline_using_latex



########################
# Process data for D24 #
########################

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
legend_params = dict(handles=[Line2D([], [], c='r', ls='', marker='o',
                                     fillstyle='none', label='Messpunkte'),
                              Line2D([], [], c='b', ls='-',
                                     label='Regressionsgerade')],
                     numpoints=2)
for di in d.data.keys():
    d.plt_kwds_mapping[di].update({'legend_params':legend_params})
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

d.plot()
d.data_a1_plot.atwnul('Bestimmung der Leitfähigkeit von Kupfer\nU gegen I\n')
d.data_a2a_plot.ax.set_yticklabels([i for i in np.arange(6)])
d.data_a2a_plot.atwnul('Hallspannung in Abhängigkeit des Querstroms\n')
d.data_a2b_plot.ax.set_xticklabels([i for i in np.arange(50, 450, 50)])
d.data_a2b_plot.ax.set_yticklabels([i for i in np.arange(0.5, 4, 0.5)])
d.data_a2b_plot.atwnul('Hallspannung in Abhängigkeit des Magnetfeldes\n')

d.save(papertype='a4', orientation='landscape')
