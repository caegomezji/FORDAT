# ARIMA example
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from statsmodels.tools.eval_measures import rmse


def forcast_arima(data):
    # data[Sector ] == X
    data = data.interpolate()
    size = int(len(data) * 0.66)
    train, test = data[0:size], data[size:len(data)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)

    # evaluate forecasts
    error = np.sqrt(rmse(test, predictions))
    print('Test RMSE: %.3f' % error)
    # plot forecasts against actual outcomes
    # plt.plot(np.array(test))
    # plt.plot(predictions, color='red')
    # plt.show()

    return test, predictions