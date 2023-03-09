explanations = {
    'pre_upload': 'Welcome to ARIMA Studio! To begin, upload a CSV with your time series data below. '
                  'We recommend using kaggle for this purpose. If you do not have access to time series data'
                  'right now, feel free to use the default Microsoft stock price data by pressing "Use Our MSFT Data" ',
    'data_selection': 'Nice, your data has successfully been uploaded. Now, you must properly tag your data. We do not '
                      'know the name of your Date column, nor the name of the variable of interest. Look through your '
                      'data below and write the name of the Date column, along with the column that represents your '
                      'response variable. Then, input a start date for your time series. Everything before this date'
                      ' will be ignored.',
    'exploration': 'All pre-processing is done, your data is ready to go. Now you can use statistics to build your '
                   'ARIMA model and use it to predict future data points!',
    'decomposition': 'Any time series can be decomposed into different components. The trend encodes the general '
                     'shape'
                     'of the series, while the seasonality can give hints about if there are internal '
                     'cycles in your'
                     'data. Finding the frequency of these cycles can be helpful when building SARIMA models. \n'
                     'Time series can be decomposed multiplicatively or additively. Choose the one that has residuals'
                     'that have a mean of zero and constant variance.',
    'pdq': 'To determine the order of your ARIMA model, you need to find the order of P, D, and Q. The easiest of  '
           'these is D, and is a good place to start. Choose a level of differencing such that the autocorrelations'
           'of each lag goes to zero quickly. Be careful not to overdifference the model, which happens if the lags'
           'immediately have negative autocorrelations. We can instead use a hypothesis test to find D, which is'
           'printed in the title of the plot for your convenience \n'
           'Once you determine D, find P by pressing Determine P Order and '
           ' counting the number of lags that are above the significance line, for your '
           'chosen D \n'
           'Once you determine P, find Q by pressing Determine Q order and counting the number of lags that are'
           'above the significance line, for your chosen D. \n'
           'Once you have a value for P, D, and Q, build and forecast your model below',
    'build_forecast': 'Enter your values for P, D, and Q from above. Then, choose a forecast start date. This is '
                      'important because all data after this date will be testing data, and all data before this date '
                      'will be training data. A good place to start is a 75% 25% train/test split. Then, choose a '
                      'number of test points to predict. You can either try and predict your entire testing data,'
                      'or only test some of it. You can also see the summary statistics of your model, and determine'
                      'if any coefficients are not statistically significant, with a p value of over 0.05. If this is'
                      'the case, you may want to re-define your model. Finally, the MAPE is our preferred accuracy'
                      'metric. ',
    'automatically': 'Seasonal models, called SARIMA, are difficult to fully parameterize by hand. Therefore, for '
                     'SARIMA, we use the auto_arima function from pmdarima to perform stepwise model selection. '
                     'However, as a statistician, you must determine the frequency of your seasonality, the m '
                     'parameter.'
                     'We recommend using the seasonal decomposition tab above to do this. \n'
                     'WARNING: Auto SARIMA is a long process. This operation may take upwards of 10 seconds '
}
