import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1, 2],
             [1.5, 1.8],
             [5, 8],
             [8, 8],
             [1, 0.6],
             [9, 11]],)

# plt.scatter(X[:, 0], X[:, 1], s=150)
# plt.show()

class K_means:
    def __init__(self, k=2, tol=0.001, max_iter=300):
        self.k = k
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, data):
        self.centroids = {}

        for i in range(self.k):
            self.centroids[i] = data[i]

        for i in range(self.max_iter):
            self.classifications = {}

            for i in range(self.k):
                self.classifications[i] = []

            for featureset in data:
                distances = [np.linalg.norm(featureset-self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classifications[classification].append(featureset)

            prev_centroids = dict(self.centroids)

            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification], axis=0)

            optimized = True

            for c in self.centroids:
                original_centroid = prev_centroids[c]
                current_centroid = self.centroids[c]
                if np.sum((current_centroid-original_centroid)/original_centroid*100.0) > self.tol:
                    optimized = False

            if optimized:
                break


    def visualize_2D(self, data):
        colors = ["g.", "r.", "c.", "b.", "k.", "o."]*10
        centroids = np.array(list(self.centroids.values()))
        for i in range(len(data)):
            plt.plot(data[i][0], data[i][1], colors[self.predict(data[i])], markersize=25)
        plt.scatter(centroids[:, 0], centroids[:, 1], marker="x", s=150, linewidths=5)
        plt.show()

    def predict(self, data):
        distances = [np.linalg.norm(data-self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification

clf = K_means(k=2)
unknowns = np.array([[1, 3],
                     [8, 9],
                     [0, 3],
                     [5, 4],
                     [6, 4], ])

clf.fit(X)
clf.visualize_2D(X)
colors = ["g", "r", "c", "b", "k", "o"]*10

clf.visualize_2D(unknowns)

# for unknown in unknowns:
#     classification = clf.predict(unknown)
#     plt.scatter(unknown[0], unknown[1], marker='*', color=colors[classification], s=150, linewidth=5)
#
# plt.show()