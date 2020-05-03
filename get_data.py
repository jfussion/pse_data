import datetime as dt
import os

import pandas as pd

PATH = os.path.dirname(__file__) + "/data/{symbol}.csv"


def get_data(symbol, start=None, end=None, resolution="D"):
    """
    Parameters
    ----------
    symbols : {str, List[str]}
        String symbol of like of symbols
    start : string, int, date, datetime, Timestamp
        Starting date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980')
    end : string, int, date, datetime, Timestamp
        Ending date
    resolution : string
        Resolution. (e.g. 'D', 'W', 'M')
    """

    if not start and not end:
        end = dt.date.today()
        start = end - dt.timedelta(days=365 * 5)

    df = pd.read_csv(PATH.format(symbol=symbol), index_col="date", parse_dates=["date"])

    start = pd.to_datetime(start).floor("D")
    end = pd.to_datetime(end).floor("D")

    mask = (df.index >= start) & (df.index <= end)

    if resolution == "D":
        return df.loc[mask]

    if resolution == "M":
        rule = "BMS"
        offset = None
    elif resolution == "W":
        rule = "W"
        offset = pd.offsets.timedelta(days=-6)
    else:
        return df.loc[mask]

    return (
        df.loc[mask]
        .resample(rule, loffset=offset)
        .apply(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        )
    )
