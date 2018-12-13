# import required packages

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
from sklearn.model_selection import cross_validate

LAT_LONG = ["long", "lat"]
J_FOLD = 10


def model_price_knn(train, predict, ks=[3, 4, 5]):
    best_k = -1
    rmses = []
    best_rmse = np.Infinity

    for k in ks:
        neighbors_model = KNeighborsRegressor(n_neighbors=k)

        X = train[LAT_LONG]
        y = train[["target"]]
        scores = cross_validate(
            neighbors_model, X, y, cv=J_FOLD, scoring="neg_mean_squared_error"
        )

        error = np.sqrt(-np.mean(scores["test_score"]))
        rmses.append(error)

        if error < best_rmse:
            best_rmse = error
            best_k = k

    best_model = KNeighborsRegressor(n_neighbors=best_k)
    X = train[LAT_LONG]
    y = train[["target"]]
    best_model.fit(X, y)
    print("Best model with K =", best_k)

    # PREDICT

    predict = predict[LAT_LONG]
    prices = best_model.predict(predict)

    return prices, rmses, ks
