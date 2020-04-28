import io
import os
import sys
import zlib

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from symbols import TICKERS


def update():
    url = "https://www.pse.com.ph/stockMarket/companyInfoCharts.html"
    headers = {"Referer": "https://www.pse.com.ph", "Host": "www.pse.com.ph"}

    for ticker in TICKERS:
        path = "data/{}.csv".format(ticker)

        params = {"method": "getAnyStockStockData", "symbol": ticker}
        s = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504]
        )
        s.mount("http://", HTTPAdapter(max_retries=retries))

        print("fetching {}...".format(ticker))
        r = s.get(url, params=params, headers=headers, timeout=5)
        if not r.content:
            print("skipping {}...".format(ticker))
            continue

        raw = zlib.decompress(r.content)
        df = pd.read_csv(
            io.BytesIO(raw),
            parse_dates=[0],
            names=["date", "open", "high", "low", "close", "volume"],
            index_col="date",
        ).sort_index()

        if not os.path.isfile(path):
            print("creating {}...".format(path))
            new = df
        else:
            print("updating {}...".format(ticker))
            orig = pd.read_csv(path, index_col="date", parse_dates=["date"])
            new = orig.combine_first(df)

        new["volume"] = new["volume"].apply(lambda x: int(x))
        new.to_csv(path)


if __name__ == "__main__":
    update()
