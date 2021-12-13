# -*- coding: utf-8 -*-
"""
Functions for saving and loading the variables.

"""
import pickle


def save_variable(v, filename):
    """
    Save the variables in a file.

    Parameters
    ----------
    v : a list of variables to save.
    filename : specify a file name to save.

    Returns
    -------
    filename : the name of the saved file.

    """
    f = open(filename, 'wb')
    pickle.dump(v, f)
    f.close()
    return filename


def load_variable(filename):
    """
    Load the variables from the file.

    Parameters
    ----------
    filename : the file name of the file to read.

    Returns
    -------
    r : a list of the loaded variables.

    """
    f = open(filename, 'rb')
    r = pickle.load(f)
    f.close()
    return r
