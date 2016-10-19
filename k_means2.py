# C:\Users\mkangrga\PycharmProjects\PublicHacking\titanic.xls
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing

def handle_non_numerical_data(df):
    # handling non-numerical data: must convert.
    columns = df.columns.values

    for column in columns:
        text_digit_vals = {}

        # print(column,df[column].dtype)
        if df[column].dtype != np.int64 and df[column].dtype != np.float64:

            column_contents = df[column].values.tolist()
            # finding just the uniques
            unique_elements = set(column_contents)
            # great, found them.
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    # creating dict that contains new
                    # id per unique string
                    text_digit_vals[unique] = x
                    x += 1
            # now we map the new "id" vlaue
            # to replace the string.
            df[column] = list(map(lambda val: text_digit_vals[val], df[column]))
            # df[column] = list(map(convert_to_int, df[column]))
    return df

df = pd.read_excel('titanic.xls')
original_df = pd.DataFrame.copy(df)
df.drop(['body', 'name'], 1, inplace=True)
df.drop(['boat', 'ticket'], 1, inplace=True)
df.fillna(0, inplace=True)
print(df.head())
df = handle_non_numerical_data(df)



X = np.array(df.drop(['survived'], 1).astype(float))
X = preprocessing.scale(X)
y = np.array(df['survived'])
clf = KMeans(n_clusters=2)
clf.fit(X)

correct = 0
for i in range(len(X)):
    predict_me = np.array(X[i].astype(float))
    predict_me = predict_me.reshape(-1, len(predict_me))
    prediction = clf.predict(predict_me)
    if prediction[0] == y[i]:
        correct += 1

print(correct/len(X))


