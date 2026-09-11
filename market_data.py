import requests
import pandas as pd


URL = "https://www.okx.com/api/v5/market/candles"


def fetch_klines(symbol="BTC-USDT", interval="1H", limit=250):

    params = {
        "instId": symbol,
        "bar": interval,
        "limit": limit
    }

    r = requests.get(URL, params=params)
    r.raise_for_status()

    raw = r.json()["data"]

    df = pd.DataFrame(
        raw,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "volCcy",
            "volCcyQuote",
            "confirm"
        ]
    )

    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c])

    return df
