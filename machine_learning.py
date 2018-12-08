# import required packages
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np


def model_price_knn(train, predict, k=[3,4,5]):

    # SPLIT DATA FOR TRAIN / TEST
    train, test = train_test_split(train, test_size=0.4)

    train_X = train[['pos_x', 'pos_y']]
    train_target = train[['target']]

    test_X = test[['pos_x', 'pos_y']]
    test_target = test[['target']]

    # SCALE THE FEATURES
    scaler_x = MinMaxScaler(feature_range=(0, 1))
    scaler_target = MinMaxScaler(feature_range=(0, 1))

    train_X = scaler_x.fit_transform(train_X)
    train_target = scaler_target.fit_transform(train_target)

    test_X = scaler_x.fit_transform(test_X)
    test_target = scaler_target.fit_transform(test_target)

    # FIND BEST MODEL
    best_model = None
    best_rmse = np.Infinity

    rmse_val = []  # to store rmse values for different k
    for K in k:
        model = neighbors.KNeighborsRegressor(n_neighbors=K)
        model.fit(train_X, train_target)  # fit the model
        pred = model.predict(test_X)  # make prediction on test set
        error = sqrt(mean_squared_error(test_target, pred))  # calculate rmse
        rmse_val.append(error)  # store rmse values

        if (error < best_rmse):
            best_model = model
            best_rmse = error
            best_K = K

    print("Best model with K=", best_K)

    # PREDICT

    predict = scaler_x.fit_transform(predict)
    prices = best_model.predict(predict)

    return scaler_target.inverse_transform(prices), rmse_val
