import pandas as pd
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt


def make_model(data):
    y = data.result.copy()
    X = data.drop(['game_id', 'result'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True)

    model = LogisticRegression(max_iter=2000)

    model.fit(X_train, y_train)
    y_pred = pd.Series(model.predict(X_test))
    y_test = y_test.reset_index(drop=True)
    z = pd.concat([y_test, y_pred], axis=1)
    z.columns = ['Correct', 'Prediction']
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(z)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))

    # # graph training vs. validation accuracy
    # plt.figure(1)
    # plt.plot(history.history['accuracy'])
    # plt.plot(history.history['val_accuracy'])
    # plt.title('model accuracy')
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    #
    # # graph training vs. validation loss over epochs
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
