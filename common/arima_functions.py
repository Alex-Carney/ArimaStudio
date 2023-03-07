import numpy as np
import pandas as pd
from pandas import DataFrame
from statsmodels.tsa.stattools import adfuller
from pmdarima.arima.utils import ndiffs
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
from statsmodels.tsa.seasonal import seasonal_decompose
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes


def decompose_data(df: DataFrame, response_var: str):
    """
    WARNING: Assumes data has been properly pre-processed
    :param d:
    :param df:
    :return:
    """
    # Multiplicative Decomposition
    result_mul = seasonal_decompose(df[response_var], model='multiplicative', extrapolate_trend='freq')
    # Additive Decomposition
    result_add = seasonal_decompose(df[response_var], model='additive', extrapolate_trend='freq')
    return result_mul, result_add
