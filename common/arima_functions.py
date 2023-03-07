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


def find_pdq_plot(df: DataFrame, response_var: str, type: str):
    # Determine number of lags to plot - Cannot exceed 50% of sample data
    # We used 20
    NUM_LAGS = min(20, int(df[response_var].size * .4))

    # Original series for comparison
    fig, axes = plt.subplots(3, 2, sharex='col')
    axes[0, 0].plot(df[response_var])
    axes[0, 0].set_title('Original Series')
    plot_acf(df[response_var].dropna(), ax=axes[0, 1], lags=NUM_LAGS)

    # 1st Differencing
    axes[1, 0].plot(df[response_var].diff())
    axes[1, 0].set_title('1st Order Differencing')
    if type == 'p':
        plot_pacf(df[response_var].diff().dropna(), ax=axes[1, 1], lags=NUM_LAGS)
    else:
        plot_acf(df[response_var].diff().dropna(), ax=axes[1, 1], lags=NUM_LAGS)

    # 2nd Differencing
    axes[2, 0].plot(df[response_var].diff().diff())
    axes[2, 0].set_title('2nd order Differencing')
    if type == 'p':
        plot_pacf(df[response_var].diff().diff().dropna(), ax=axes[2, 1], lags=NUM_LAGS)
    else:
        plot_acf(df[response_var].diff().diff().dropna(), ax=axes[2, 1], lags=NUM_LAGS)

    # Correct tick marks:
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[2, 0].tick_params(axis='x', rotation=45)

    # Compare to stepwise algorithm - for D
    if type == 'd':
        suggested_d = ndiffs(df[response_var], test='adf')
        plt.suptitle("Analysis of Differencing Order. Suggested d = " + str(suggested_d))
    else:
        plt.suptitle("Analysis of " + str(type) + " Order.")

    return fig


def build_and_forecast(df, response_col, model_spec, train_test_date, num_predictions):
    # Build model, and fit it to the data
    model = pm.ARIMA(order=model_spec)

    # Split the data
    cutoff_date = pd.to_datetime(train_test_date)

    # Split the series by date
    df_series = df[response_col]
    before_df = df_series.loc[df_series.index <= cutoff_date]
    after_df = df_series.loc[df_series.index >= cutoff_date]

    # Fit on training data ONLY
    model.fit(before_df)

    # Predict
    fitted, confint = model.predict(n_periods=num_predictions, return_conf_int=True, start=before_df.iloc[-1],
                                    dynamic=True)
    index_of_fc = pd.bdate_range(after_df.index[0], periods=num_predictions, freq='B')

    # plot training starting backwards in time
    index_of_train = pd.bdate_range(before_df.index[-1], periods=3*num_predictions, freq='-1B')


    # make series for plotting purpose
    # fitted_predictor = pd.Series(df[COLUMN_TO_ANALYZE],
    fitted_series = pd.Series(fitted, index=index_of_fc)
    lower_conf = pd.Series(confint[:, 0], index=index_of_fc)
    upper_conf = pd.Series(confint[:, 1], index=index_of_fc)

    train_data = before_df.loc[index_of_train]
    test_data = after_df.loc[index_of_fc]

    mape_numerator = np.abs((fitted_series - test_data).dropna())
    mape_denominator = np.abs(test_data)
    mape = np.mean(mape_numerator / mape_denominator)

    fig, ax = plt.subplots()
    # Plot training data
    ax.plot(train_data, color='blue')
    # Plot testing data
    ax.plot(test_data, color='red')
    ax.plot(fitted_series, color='darkgreen')
    ax.fill_between(lower_conf.index,
                     lower_conf,
                     upper_conf,
                     color='k', alpha=.15)

    ax.set_title("ARIMA - Final Forecast - MAPE = " + str(np.around(100 * mape, 2)) + "%")
    ax.tick_params(axis='x', rotation=45)
    ax.legend(['Training Data', 'Actual', 'Predicted'])
    ax.grid()

    return fig
