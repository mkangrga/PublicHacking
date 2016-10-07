import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import datetime
from matplotlib import style
import pickle
import re
style.use('ggplot')

api_key = open('api_key.txt', 'r').read()


def get_dataset(quandl_code):
    df = quandl.get(quandl_code, authtoken=api_key)
    code = re.search(r'(\w+)/(\w+)', quandl_code).group(2)
    df[code + "_PCT_CHG"] = np.log(df["Close"] / df["Open"]) * 100.0
    df.rename(columns={"Open": code + "_open", "Close": code + "_close"}, inplace=True)
    df = df[[code + "_open", code + "_close", code + "_PCT_CHG"]]
    return df


def refresh_vix_pickle():
    main_df = pd.DataFrame()

    for i in range(1, 10):
        df = get_dataset("CHRIS/CBOE_VX" + str(i))
        if main_df.empty:
            main_df = pd.DataFrame(df)
        else:
            main_df = main_df.join(df)
        print("getting " + str(i) + " out of 9")

    list_of_stuff = ["YAHOO/INDEX_GSPC",
                     "YAHOO/INDEX_RUT",
                     "YAHOO/INDEX_SPY",
                     "YAHOO/VXX",
                     "GOOG/NYSEARCA_UVXY"]

    for code in list_of_stuff:
        df = get_dataset(code)
        if main_df.empty:
            main_df = pd.DataFrame(df)
        else:
            main_df = main_df.join(df)
        print("getting " + code)

    main_df.to_pickle('vix_data.pickle')
    print(main_df.tail())

df = pd.read_pickle('vix_data.pickle')

print(df.tail())
print(df.head())

forecast_col = 'CBOE_VX1_PCT_CHG'
df.fillna(-99999, inplace=True)

forecast_out = 1 # forecast_out = int(math.ceil(0.01 * len(df)))
print(forecast_out)

# df[forecast_col] = df[forecast_col].shift(-forecast_out)

X = np.array(df.drop([forecast_col], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
# X = X[:-forecast_out]
df.dropna(inplace=True)
y = np.array(df[forecast_col])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)
df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 24*60*60
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

