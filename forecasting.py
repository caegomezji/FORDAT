# ARIMA example
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from statsmodels.tools.eval_measures import rmse
import pmdarima as pm
from fbprophet import Prophet
from time import time
import matplotlib.pyplot as plt
import pandas as pd
import math

def BIC(y_real, y_model):
    n = len(y_real)
    k = 2
    resid = y_real - y_model
    sse = sum(resid**2)
    BIC_value = k * math.log(n) - 2 * math.log(sse)
    return BIC_value

def AIC(y_real, y_modelo):
    resid = y_real - y_modelo
    print(resid)
    sse = sum(resid**2)
    k = 1 # parameters
    AIC_value = 2*k - 2*math.log(sse)
    return AIC_value

def make_forecast(data, model='prophet'):

    data = data.interpolate()
    test_months = 6
    train, test = data[0:-test_months], data[-test_months:]
    history = [x for x in train]
    predictions = list()
    future_months = 18
    test_time = len(test)

    if model == 'prophet':
        predictions = forecast_prophet(train, future_months)
    elif model == 'autoarima':
        predictions = forecast_autoarima(train, future_months)

    return test, predictions

def forecast_autoarima(data, future_months=12):

    history = [x for x in data]

    model = pm.auto_arima(history, start_p=0, d=1, start_q=0,
                          max_p=2, max_d=2, max_q=2, start_P=0,
                          D=1, start_Q=0, max_P=2, max_D=2,
                          max_Q=2, m=12, seasonal=True,
                          error_action='warn', trace=True,
                          supress_warnings=True, stepwise=True,
                          random_state=20, n_fits=10)

    predictions = model.predict(future_months)
    
    return pd.Series(predictions)

def forecast_prophet(data, future_months=12):

    data_model = data.reset_index(name='FOBDOL')

    data_model.columns = ['ds', 'y' ]  # prophet model just understando these names
    #print(data_model.shape)
    # HERE YOU SHOULD PUT YOUR MODEL
    print('start model')
    model = Prophet(interval_width=0.95, seasonality_mode='multiplicative')

    print('model defined')
    model.fit(data_model)
    print('model fitted')
    # future_months = 12  # this variable is a slider in the app
    future = model.make_future_dataframe(periods=future_months, freq='MS')  # predict on months
    forecast = model.predict(future)
    predictions = forecast.yhat
    print('predicted')
    # in case you want to see its output
    # print(forecast.head(2))
    # print(predictions)
    return predictions[-future_months:].reset_index()['yhat']

def forcast_arima(data):
    # data[Sector ] == X
    data = data.interpolate()
    size = int(len(data) * 0.80)
    train, test = data[0:size], data[size:len(data)]
    history = [x for x in train]
    predictions = list()
    future_months = 12
    test_time = len(test)
    for t in range(test_time + future_months ):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        if t < test_time:
            obs = test[t]
            history.append(obs)
        if t >= test_time:
            history.append(yhat)

    # evaluate forecasts
   # error = np.sqrt(rmse(test, predictions))
    #print('Test RMSE: %.3f' % error)
    # plot forecasts against actual outcomes
    # plt.plot(np.array(test))
    # plt.plot(predictions, color='red')
    # plt.show()

    return test, predictions    