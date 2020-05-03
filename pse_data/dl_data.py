import io
import sys
import zipfile

import pandas as pd
import requests


def data_to_file():
    """Convert data.csv from https://github.com/r-phinvest/r-phinvest.github.io/blob/master/data.zip to each file"""

    print("retrieving data.csv")
    url = "https://github.com/r-phinvest/r-phinvest.github.io/raw/master/data.zip"
    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    df = pd.read_csv(
        z.open("data.csv"),
        header=None,
        names=["symbol", "date", "open", "high", "low", "close", "volume"],
        parse_dates=[1],
    )
    z.close()
    r.close()

    while len(df):
        symbol = df.iloc[0, 0]
        print("processing {}...".format(symbol))
        data = df[df["symbol"] == symbol].copy()
        idxs = data.index.values.tolist()
        data.set_index("date", inplace=True)
        data.drop(columns="symbol", inplace=True)

        data.to_csv("data/{}.csv".format(symbol))
        print("saving {}.csv...".format(symbol))
        df.drop(index=idxs, inplace=True)


if __name__ == "__main__":
    data_to_file()
