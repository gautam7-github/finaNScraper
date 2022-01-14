from datetime import datetime
from lxml import html
from pandas.core import base
import requests
import numpy as np
import pandas as pd
import json


def get_page(url):
    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    # is generally good practice when building a scraper
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    return requests.get(url, headers=headers)


def parse_rows(table_rows):
    parsed_rows = []
    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")
        none_count = 0
        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1
        if (none_count < 4):
            parsed_rows.append(parsed_row)
    return pd.DataFrame(parsed_rows)


def clean_data(df):
    df = df.set_index(0)
    df = df.transpose()
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)
    numeric_columns = list(df.columns)[1::]
    for column_index in range(1, len(df.columns)):
        df.iloc[:, column_index] = df.iloc[:, column_index].str.replace(
            ',', '')
        df.iloc[:, column_index] = df.iloc[:, column_index].astype(
            np.float)
    return df


def scrape_table(url):
    page = get_page(url)
    tree = html.fromstring(page.content)
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
    assert len(table_rows) > 0
    df = parse_rows(table_rows)
    df = clean_data(df)
    return df


def processMiscData(miscData=None):
    tree = html.fromstring(miscData.content)
    name = tree.xpath(
        "//*[@id=\"quote-header-info\"]/div[2]/div[1]/div[1]/h1")[0].text
    price = tree.xpath(
        "/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")[0].text
    beta = tree.xpath(
        "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]")[0].text
    return name, price, beta


def startProcessing(baseUrl=None, symbol=None):
    df_financials = scrape_table(
        f'{baseUrl}{symbol}/financials?p={symbol}')
    df_balance_sheet = scrape_table(
        f'{baseUrl}{symbol}/balance-sheet?p={symbol}')
    df_cash_flow = scrape_table(
        f'{baseUrl}{symbol}/cash-flow?p={symbol}')
    miscData = get_page(
        f"{baseUrl}{symbol}/?p={symbol}")
    name, price, beta = processMiscData(miscData)
    dfs = [df_financials, df_balance_sheet, df_cash_flow]
    ls = []
    for df in dfs:
        df.index = df["Date"]
        df.drop(labels="Date", axis=1, inplace=True)
        ls.append(json.loads(df.to_json(orient="index")))
    data = [
        {
            "details": {
                "company": name,
                "last-price": price,
                "beta": beta
            },
        },
        {
            "financials": ls[0]
        },
        {
            "balance-sheet": ls[1]
        },
        {
            "cash-flow": ls[2]
        }
    ]
    return data


def main(symbol="TATASTEEL.NS"):
    baseUrl = 'https://finance.yahoo.com/quote/'
    return startProcessing(
        baseUrl=baseUrl, symbol=symbol
    )
