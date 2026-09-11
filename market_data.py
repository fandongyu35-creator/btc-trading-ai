import requests
import pandas as pd

URL = "https://api.binance.com/api/v3/klines"

def fetch_klines(symbol="BTCUSDT", interval="1h", limit=250):
    r = requests.get(URL, params={"symbol":symbol,"interval":interval,"limit":limit}, timeout=10)
    r.raise_for_status()
    raw = r.json()
    df = pd.DataFrame(raw, columns=[
        "time","open","high","low","close","volume","close_time",
        "quote_volume","trades","taker_buy_base","taker_buy_quote","ignore"
    ])
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c])
    return df
