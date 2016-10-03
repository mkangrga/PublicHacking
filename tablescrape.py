#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys
from bs4 import BeautifulSoup
import urllib.request
import datetime
import pandas as pd
import pickle
import numpy as np

from pandas_datareader import data as web
import matplotlib.pyplot as plt
from matplotlib import style
from yahoo_finance import Share
import quandl
style.use('fivethirtyeight')


api_key = "AazaK8bSUJLemayFzakF"


def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start='1975-01-01', authtoken=api_key)
    df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
    df.rename(columns={"Value": "M30"}, inplace=True)
    # df = df.resample('D')
    df = df.resample("M").mean()
    return df


def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start='1975-01-01', authtoken=api_key)
    df['Adjusted Close'] = (df["Adjusted Close"] - df["Adjusted Close"][0]) / df["Adjusted Close"][0] * 100.0
    df = df.resample("M").last()
    df.rename(columns={"Adjusted Close": "sp500"}, inplace=True)
    df = df["sp500"]
    return df


def gdp_data():
    df = quandl.get("BCB/4385", trim_start='1975-01-01', authtoken=api_key)
    df['Value'] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
    df = df.resample("M").last()
    df.rename(columns={"Value": "GDP"}, inplace=True)
    df = df["GDP"]
    return df


def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start='1975-01-01', authtoken=api_key)
    df['Unemployment Rate'] = (df["Unemployment Rate"] - df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df = df.resample("M").mean()
    return df

def main():
    housing_data = pd.read_pickle('HPI.pickle')
    housing_data = housing_data.pct_change()



    print(housing_data.head())

    housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    housing_data.dropna(inplace=True)




def main6():
    sp500 = sp500_data()
    US_GDP = gdp_data()
    US_umeployment = us_unemployment()

    m30 = mortgage_30y()
    HPI_data = pd.read_pickle("fiddy_states3.pickle")
    HPI_bench = HPI_Benchmark()

    HPI = HPI_data.join([m30, US_umeployment, US_GDP, sp500])
    HPI.dropna(inplace=True)

    print(HPI)
    print(HPI.corr())

    HPI.to_pickle('HPI.pickle')


def main5():
    df = mortgage_30y()
    print(df)

    m30 = mortgage_30y()
    HPI_data = pd.read_pickle('fiddy_states3.pickle')
    HPI_Bench = HPI_Benchmark()

    state_HPI_M30 = HPI_data.join(m30)

    # print(state_HPI_M30.corr()['M30'].describe())

    M30_rolling_corr = state_HPI_M30.rolling(window=12).corr(state_HPI_M30['M30'])
    # print(M30_rolling_corr)

    # bridge_height = {'meters': [10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}
    # df = pd.DataFrame(bridge_height)
    # df['STD'] = pd.rolling_std(df['meters'], 2)
    # print (df)
    #
    # df_std = df.describe()['meters']['std']
    # df = df[(df['STD'] < df_std * 2)]
    #
    # print(df_std)
    #
    # df.plot()
    # plt.show()




def state_list():
    fiddy_states = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
    return fiddy_states[0][0][1:]

def grab_initial_state_data():

    states = state_list()
    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        df = quandl.get(query, authtoken=api_key)
        df.rename(columns={"Value": str(abbv)}, inplace=True)
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    pickle_out = open('fiddy_states3.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.rename(columns={"Value": "United States"}, inplace=True)
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100.0
    return df

def main1():
    # grab_initial_state_data()
    fig = plt.figure()
    ax1 = plt.subplot2grid((2, 1), (0, 0))
    ax2 = plt.subplot2grid((2, 1), (1, 0), sharex=ax1)

    HPI_data = pd.read_pickle('fiddy_states3.pickle')
    # TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
    TX_AK_12corr = HPI_data['TX'].rolling(window=12).corr(HPI_data['AK'])

    HPI_data['TX'].plot(ax=ax1, label='TX HPI')
    HPI_data['AK'].plot(ax=ax1, label='AK HPI')
    ax1.legend(loc=4)

    TX_AK_12corr.plot(ax=ax2, label='TX/AK Corr')

    plt.legend(loc=4)
    plt.show()


    # df = pd.read_csv("ZILL-Z84501_MLP.csv")
    # df.set_index("Date", inplace=True)
    # print(df.head())
    # df.to_csv('newcsv2.csv')
    # df = pd.read_csv('newcsv2.csv', index_col=0)
    # df.columns = ['Austin_HPI']
    # print(df.head())

def main3():
    yahoo = Share('YHOO')
    # df = pd.DataFrame(yahoo.get_historical('2016-01-01', '2016-09-21'))
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2016, 9, 1)
    df = web.DataReader("XOM", "yahoo", start, end)
    print(df.head()) #print(df['Close'])
    df['Adj Close'].plot()
    plt.show()

def main2():
    my_url = "https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20160316.htm"
    soup = BeautifulSoup(urllib.request.urlopen(my_url).read(), "lxml")
    table_dfs = pd.read_html(str(soup.find_all("table")))
    writer = pd.ExcelWriter("pandas_file.xlsx", engine="xlsxwriter")
    tableTitles = ["Main"]

    table_dfs.pop(0)
    table_dfs.pop(0)
    table_dfs.pop(0)

    # Get table titles
    for each in soup.find_all("span", attrs={"class":"tablesubhead"}):
        tableTitles.append(each.string)

    for table, name in zip(table_dfs, tableTitles):
        table.to_excel(writer, sheet_name=name)

    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
