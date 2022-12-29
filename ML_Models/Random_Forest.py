import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import matplotlib as plt
from pprint import pprint

def make_model(data):
    y = data.win_result.copy()
    # X = data[['home_pts', 'home_ ts_pct', 'home.off_rtg', 'home.def_rtg', 'home.defg_pct', 'away_pts', 'away_ts_pct', 'away.off_rtg', 'away.def_rtg', 'away.defg_pct']]
    X = data.drop(['game_id', 'win_result'], axis=1)
    # 'home.cont_2', 'home.cont_3', 'home.lb_rec', 'away.cont_2', 'away.cont_3', 'away.lb_rec'
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)

    # model = RandomForestClassifier(n_estimators=200, min_samples_leaf=4, min_samples_split=5, max_depth=10)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_test = y_test.reset_index(drop=True)

    y_pred_proba = model.predict_proba(X_test)
    results = pd.concat([y_test, pd.DataFrame(y_pred_proba)], axis=1)
    print(results.mean(axis=0))
    # results.columns = ['Correct Prediction', 'Away Win', 'Home Win']
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(results)

    print("---------------------------------------------")

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))
    print("F1:", metrics.f1_score(y_test, y_pred))
    print("AUC Score:", metrics.roc_auc_score(y_test, y_pred))

    print("---------------------------------------------")

    print(pd.Series(model.feature_importances_, index = X.columns).sort_values(ascending = False))

    return model

training_data = pd.read_csv("Data/training_data.csv")
training_data.columns = ["game_id", "win_result", "home_pts", "home_ ts_pct", "home.fta", "home.ft_pct", "home.fg3a",
                         "home.fg3_pct", "home.ast", "home.tov", "home.oreb", "home.dreb", "home.stl", "home.blk",
                         "home.defl", "home.lb_rec", "home.cont_2", "home.cont_3", "home.defg_pct", "home.off_rtg",
                         "home.def_rtg", "home.pf", "away_pts", "away_ts_pct", "away.fta", "away.ft_pct", "away.fg3a",
                         "away.fg3_pct", "away.ast", "away.tov", "away.oreb", "away.dreb", "away.stl", "away.blk",
                         "away.defl", "away.lb_rec", "away.cont_2", "away.cont_3", "away.defg_pct", "away.off_rtg",
                         "away.def_rtg", "away.pf"]

RFmodel = make_model(training_data)

Pkl_Filename = "ML_Models/models/NBA_RFModel.pkl"
with open(Pkl_Filename, 'wb') as file:
    pickle.dump(RFmodel, file)

# y = training_data.win_result.copy()
# X = training_data.drop(['game_id', 'win_result'], axis=1)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)

# model = RandomForestClassifier(n_estimators=200, min_samples_leaf=4, min_samples_split=5, max_depth=10)

# from sklearn.feature_selection import RFECV
# rfe = RFECV(model)
# rfe.fit(X_train, y_train)
# selected_features = np.array(X.columns)[rfe.get_support()]
# print(selected_features)


# Find best hyperparameters using RandomizedSearchCV
# from sklearn.model_selection import RandomizedSearchCV
# # Number of trees in random forest
# n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]

# # Number of features to consider at every split
# max_features = ['auto', 'sqrt']

# # Maximum number of levels in tree
# max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
# max_depth.append(None)

# # Minimum number of samples required to split a node
# min_samples_split = [2, 5, 10]

# # Minimum number of samples required at each leaf node
# min_samples_leaf = [1, 2, 4]

# # Method of selecting samples for training each tree
# bootstrap = [True, False]

# # Create the random grid
# random_grid = {'n_estimators': n_estimators,
#             'max_features': max_features,
#             'max_depth': max_depth,
#             'min_samples_split': min_samples_split,
#             'min_samples_leaf': min_samples_leaf,
#             'bootstrap': bootstrap}
# pprint(random_grid)

# # Use the random grid to search for best hyperparameters
# # First create the base model to tune
# rf = RandomForestClassifier()
# # Random search of parameters, using 3 fold cross validation, 
# # search across 100 different combinations, and use all available cores
# rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, n_jobs = -1)
# # Fit the random search model
# rf_random.fit(X_train, y_train)

# pprint(rf_random.best_params_)