import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle


def make_model(data):
    y = data.win_result.copy()
    X = data.drop(['game_id', 'win_result'], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)

    # model = LogisticRegression(max_iter=2500, penalty='l2', C=0.615848211066026)
    model = LogisticRegression(max_iter=250)
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

    return model


training_data = pd.read_csv("Data/training_data.csv")
training_data.columns = ["game_id", "win_result", "home_pts", "home_ ts_pct", "home.fta", "home.ft_pct", "home.fg3a", "home.fg3_pct", "home.ast", "home.tov", "home.oreb", "home.dreb", "home.stl", "home.blk", "home.defl", "home.lb_rec", "home.cont_2", "home.cont_3", "home.defg_pct", "home.off_rtg", "home.def_rtg", "home.pf", "away_pts", "away_ ts_pct", "away.fta", "away.ft_pct", "away.fg3a", "away.fg3_pct", "away.ast", "away.tov", "away.oreb", "away.dreb", "away.stl", "away.blk", "away.defl", "away.lb_rec", "away.cont_2", "away.cont_3", "away.defg_pct", "away.off_rtg", "away.def_rtg", "away.pf"]
LRmodel = make_model(training_data)

Pkl_Filename = "NBA_LRModel2.pkl"
with open(Pkl_Filename, 'wb') as file:
    pickle.dump(LRmodel, file)

# Use (model.predict_proba(arr)[0][1]) to find the prob for a single game

