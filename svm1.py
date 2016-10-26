import numpy as np
from sklearn import preprocessing, model_selection, neighbors, svm
from sklearn.svm import SVR
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from collections import Counter
import warnings
import random
style.use('fivethirtyeight')


df = pd.read_csv('breast-cancer-wisconsin.data')
df.replace('?', -99999, inplace=True)
df.drop(['id'], 1, inplace=True)
accuracy = []


for i in range(10):
    X = np.array(df.drop(['class'], 1))
    y = np.array(df['class'])

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

    clf = svm.SVR(kernel='rbf')
    clf.fit(X_train, y_train)

    accuracy.append(clf.score(X_test, y_test))
    # print(accuracy)

    example_measures = np.array([[10,10,1,1,1,2,3,2,1],[4,2,1,2,2,2,3,2,1]])
    example_measures = example_measures.reshape(len(example_measures), -1)

    prediction = clf.predict(example_measures)
    print(prediction, clf.score(X_test, y_test))

    # print("|", end="")

print("\n\nAccuracy: ", sum(accuracy)/len(accuracy))



