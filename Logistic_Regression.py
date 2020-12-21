import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from decimal import Decimal
# import matplotlib.pyplot as plt


def make_model(data):
    y = data.result.copy()
    X = data.drop(['game_id', 'result'], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)

    model = LogisticRegression(max_iter=2500, penalty='l2', C=0.615848211066026)
    model.fit(x_train, y_train)

    # # Create regularization penalty space
    # penalty = ['none', 'l1', 'l2']
    #
    # # Create regularization hyperparameter space
    # C = np.logspace(-4, 4, 20)
    #
    # # Create hyperparameter options
    # hyperparameters = dict(C=C, penalty=penalty)
    #
    # clf = GridSearchCV(model, hyperparameters, cv=5, verbose=0, return_train_score=True, n_jobs=-1)
    # best_model = clf.fit(X, y)
    #
    # print('Best Penalty:', best_model.best_estimator_.get_params()['penalty'])
    # print('Best C:', best_model.best_estimator_.get_params()['C'])

    y_pred = pd.Series(model.predict(x_test))
    y_test = y_test.reset_index(drop=True)
    z = pd.concat([y_test, y_pred], axis=1)
    z.columns = ['Correct', 'Prediction']
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(z)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))
    print("F1:", metrics.f1_score(y_test, y_pred))
    print("AUC Score:", metrics.roc_auc_score(y_test, y_pred))

    # # graph training vs. validation accuracy
    # plt.figure(1)
    # plt.plot(history.history['accuracy'])
    # plt.plot(history.history['val_accuracy'])
    # plt.title('model accuracy')
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    #
    # # graph training vs. validation loss
    # plt.figure(2)
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()


training_data = pd.read_csv("Data/training_data.csv")
training_data.columns = ["game_id", "result", "home_pts", "home_ts_pct", "home_fta", "home_ft_pct", "home_fg3a", "home_fg3_pct", "home_ast", "home_tov", "home_oreb", "home_dreb", "home_stl", "home_blk", "home_pf", "away_pts", "away_ts_pct", "away_fta", "away_ft_pct", "away_fg3a", "away_fg3_pct", "away_ast", "away_tov", "away_oreb", "away_dreb", "away_stl", "away_blk", "away_pf"]
make_model(training_data)
# Use (model.predict_proba(arr)[0][1]) to find the proy for a single game

