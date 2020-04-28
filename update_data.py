import io
import sys
import zlib

import pandas as pd
import requests

from symbols import TICKERS


def update():
    url = "https://www.pse.com.ph/stockMarket/companyInfoCharts.html"
    headers = {"Referer": "https://www.pse.com.ph", "Host": "www.pse.com.ph"}

    for ticker in TICKERS:
        print("fetching {}...".format(ticker))
        params = {"method": "getAnyStockStockData", "symbol": ticker}
        path = "data/{}.csv".format(ticker)

        r = requests.get(url, params=params, headers=headers)
        raw = zlib.decompress(r.content)

        df = pd.read_csv(
            io.BytesIO(raw),
            parse_dates=[0],
            names=["date", "open", "high", "low", "close", "volume"],
            index_col="date",
        ).sort_index()

        orig = pd.read_csv(path, index_col="date", parse_dates=["date"])

        print("updating {}...".format(ticker))
        new = orig.combine_first(df)
        new["volume"] = new["volume"].apply(lambda x: int(x))
        new.to_csv(path)


update()
