# ARIMA example
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from statsmodels.tools.eval_measures import rmse
import pmdarima as pm
#from fbprophet import Prophet

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

def forecast_autoarima(data):

    # data[Sector ] == X
    data = data.interpolate()
    size = -6 #int(len(data) * 0.80)
    train, test = data[0:size], data[size:len(data)]
    history = [x for x in train]
    predictions = list()
    future_months = 18
    test_time = len(test)

    model = pm.auto_arima(history, start_p=0, d=1, start_q=0,
                          max_p=2, max_d=2, max_q=2, start_P=0,
                          D=1, start_Q=0, max_P=2, max_D=2,
                          max_Q=2, m=12, seasonal=True,
                          error_action='warn', trace=True,
                          supress_warnings=True, stepwise=True,
                          random_state=20, n_fits=10)

    predictions = model.predict(future_months)

    return test, predictions


def forecast_prophet(data):

    # data[Sector ] == X
    #data = data.interpolate()
    size = -6 #int(len(data) * 0.80)
    train, test = data[0:size], data[size:len(data)]
    history = [x for x in train]
    predictions = list()
    future_months = 18
    test_time = len(test)

    data_model = userInterest[["FOBDOL", "Date"]]
    data_model.columns = ["y", "ds"]  # prophet model just understando these names

    nan_value = float("NaN")
    data_model.replace("", nan_value, inplace=True)
    data_model.dropna(inplace=True)

    print(data_model.shape)
    # if data_model.shape[0] > 3:
    # HERE YOU SHOULD PUT YOUR MODEL
    model = Prophet(interval_width=0.95, seasonality_mode='multiplicative')
    model.fit(data_model)


    return