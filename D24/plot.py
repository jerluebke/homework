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
    # dict for error values corresbonding to self.data
    _errors = {}
    # DataFrame for linreg values of df from self.data
    # Is filled by self.make_linreg, where the df which are to be processed can
    # be specified 
    _lin_reg = pd.DataFrame(index=['slope', 'intercept', 'r_val', 'p_val', 'std_err'])

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

    @property
    def data(self):
        return self._data

    @property
    def lin_reg(self):
        return self._lin_reg

    @property
    def errors(self):
        return self._errors

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

    def add_errors(self, df_id, error, which):
        """Adds error values to specified df (named by df_id)
        errors can be scalar, array-like or a callable function
        which specifies the axis to process the errors for (x or y)"""
        # TODO:
        # sort error for x and y
        # find good way to organize (in terms of structure)
        if df_id not in self._data:
            raise KeyError('{} is not found in the data dict. Add it\
                           first!'.format(df_id))
        if which not in self._data[df_id].columns:
            raise KeyError('No column named {0} is found in {1}. Add it\
                           first!'.format(which, df_id))
        if callable(error):
            pass
        # self._errors[df_id] = error



def make_plot(DataObject):
    """makes scatter plot of specified data"""
    data = DataObject.data
    lin_reg = DataObject.lin_reg
    for k, v in data.items():
        v.plot.scatter(*v.columns, title=k.replace('_', ' '))

        v0 = v[v.columns[0]]
        x = np.linspace(min(v0), max(v0))
        lr = lin_reg[k]
        plt.plot(x, x*lr.slope+lr.intercept, label='m={}+-{}'.format(lr.slope,
                                                                    lr.std_err))
        plt.legend()



d = Data('data_a1', 'data_a2a', 'data_a2b')
d.col_diff('data_a2a', 'U1', 'U2', 'U_H', rm=True)
d.col_diff('data_a2b', 'U1', 'U2', 'U_H', rm=True)
d.make_linreg()
