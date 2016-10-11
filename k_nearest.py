import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from collections import Counter
import warnings
import random
style.use('fivethirtyeight')

dataset = {'k' : [[1,2], [2,3], [3,1]], 'r': [[6,5], [7,7], [8,6]]}
new_features = [5,7]
# [[plt.scatter(ii[0], ii[1], s=100, color=i) for ii in dataset[i]] for i in dataset]
# plt.scatter(new_features[0], new_features[1])
# plt.show()

def k_nearest_neightbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('K is set to a value less than total voting groups!')
    distances = []
    for group in data:
        for features in data[group]:
            # euclidean_distance = np.sqrt(np.sum((np.array(features)-np.array(predict))**2))
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([euclidean_distance, group])
    votes = [i[1] for i in sorted(distances)[:k]]
    vote_result = Counter(votes).most_common(1)[0][0]
    confidence = Counter(votes).most_common(1)[0][1] / k
    return vote_result, confidence

df = pd.read_csv('breast-cancer-wisconsin.data')
df.replace('?', -99999, inplace=True)
df.drop(['id'], 1, inplace=True)
full_data = df.astype(float).values.tolist()

random.shuffle(full_data)
test_size = 0.2
train_data = full_data[:-int(test_size*len(full_data))]
test_data = full_data[-int(test_size*len(full_data)):]
train_set = {2: [], 4: []}
test_set = {2: [], 4: []}

for data in train_data:
    train_set[data[-1]].append(data[:-1])

for data in test_data:
    test_set[data[-1]].append(data[:-1])

counter = 0
total = 0

for group in test_set:
    for data in test_set[group]:
        result, confidence = k_nearest_neightbors(train_set, data, k=50)
        if result == group:
            counter += 1
        total += 1

print("Accuracy: ", counter/total)



def old_code():
    df = pd.read_csv('breast-cancer-wisconsin.data')
    df.replace('?', -99999, inplace=True)
    df.drop(['id'], 1, inplace=True)

    X = np.array(df.drop(['class'], 1))
    y = np.array(df['class'])

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)

    print(accuracy)

    example_measures = np.array([[10,10,1,1,1,2,3,2,1],[4,2,1,2,2,2,3,2,1]])
    example_measures = example_measures.reshape(len(example_measures), -1)

    prediction = clf.predict(example_measures)

    print(prediction)
