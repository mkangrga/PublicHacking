#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys
from bs4 import BeautifulSoup
import urllib.request
import datetime
import pandas as pd
import pickle
from pandas_datareader import data as web
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from yahoo_finance import Share
import quandl

api_key = "AazaK8bSUJLemayFzakF"

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

def HPI_Benchmark:
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.rename(columns={"Value": "United States"}, inplace=True)
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100.0
    return df

def main():
    # grab_initial_state_data()
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    HPI_data = pd.read_pickle('fiddy_states3.pickle')
    benchmark = HPI_Benchmark()

    HPI_data.plot(ax = ax1)
    benchmark.plot(ax)
    plt.legend().remove()
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

# Gather our code in a main() function
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
