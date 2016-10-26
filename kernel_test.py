from sklearn import svm, model_selection, preprocessing
import numpy as np
import matplotlib.pyplot as plt
import math

# X = list(zip(range(1, 20), map(lambda x: x**2, range(1, 20))))
# y = list(zip(range(1, 20), map(lambda x: x**3 + 20, range(1, 20))))

X = list(map(lambda x: x, range(1, 200, 20)))
y = list(map(lambda x: x**2, range(1, 200, 20)))

print(X, len(X))
print(y, len(y))

# [plt.scatter(point[0], point[1], color='k') for point in X]
# [plt.scatter(point[0], point[1], color='r') for point in y]
plt.show()

X = np.array(X).reshape(-1,1)
print(len(X), len(y))

c = 10
clf = svm.SVR(kernel='rbf', C=c)

while True:

    clf = svm.SVR(kernel='rbf', C=c, gamma=0.000001)
    clf.fit(X, y)
    if clf.score(X, y) < 0.999:
        c *= 2
        print("score %s; status: %s" % (clf.score(X, y), clf.fit_status_))
    else:
        break

print("Score: %s; min C: %.0E; Support Vectors: %s" % (clf.score(X, y), c, len(clf.support_vectors_)))
X_predict = np.array(list(map(lambda x: x, range(1, 400)))).reshape(-1, 1)
y_rbf = clf.predict(X_predict)
plt.scatter(X, y)
plt.plot(X_predict, y_rbf)
plt.show()


