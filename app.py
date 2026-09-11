from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from market_data import fetch_klines
from signal_engine import analyze
from paper_trading import PaperAccount

app = FastAPI(title="BTC Trading AI V1")
account = PaperAccount(10000)

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(open("index.html").read())

@app.get("/api/signal")
def signal():
    data = fetch_klines("BTCUSDT", "1h", 250)
    result = analyze(data)
    result["paper_balance"] = account.balance
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
