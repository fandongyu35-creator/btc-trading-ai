import pandas as pd

def analyze(df):
    d=df.copy()
    d["ema20"]=d.close.ewm(span=20,adjust=False).mean()
    d["ema50"]=d.close.ewm(span=50,adjust=False).mean()
    d["ema200"]=d.close.ewm(span=200,adjust=False).mean()

    delta=d.close.diff()
    gain=delta.clip(lower=0).rolling(14).mean()
    loss=(-delta.clip(upper=0)).rolling(14).mean()
    rs=gain/loss.replace(0, float("nan"))
    d["rsi"]=100-(100/(1+rs))

    last=d.iloc[-1]
    price=float(last.close)

    if last.ema20 > last.ema50 > last.ema200 and last.rsi < 70:
        direction="LONG"
        grade="A"
    elif last.ema20 < last.ema50 < last.ema200 and last.rsi > 30:
        direction="SHORT"
        grade="A"
    else:
        direction="NO TRADE"
        grade="C"

    # 仅示例风险模型：固定1.5%止损距离
    if direction=="LONG":
        entry_low=price*0.997
        entry_high=price*1.001
        stop=entry_low*0.985
        tp1=entry_high+(entry_high-stop)*2
        tp2=entry_high+(entry_high-stop)*3
    elif direction=="SHORT":
        entry_low=price*0.999
        entry_high=price*1.003
        stop=entry_high*1.015
        tp1=entry_low-(stop-entry_low)*2
        tp2=entry_low-(stop-entry_low)*3
    else:
        entry_low=entry_high=stop=tp1=tp2=None

    rr=2.0 if direction!="NO TRADE" else 0

    return {
        "symbol":"BTCUSDT",
        "price":round(price,2),
        "direction":direction,
        "grade":grade,
        "confidence":0.65 if grade=="A" else 0.35,
        "ema20":round(float(last.ema20),2),
        "ema50":round(float(last.ema50),2),
        "ema200":round(float(last.ema200),2),
        "rsi":round(float(last.rsi),2) if pd.notna(last.rsi) else None,
        "entry_low":round(entry_low,2) if entry_low else None,
        "entry_high":round(entry_high,2) if entry_high else None,
        "stop_loss":round(stop,2) if stop else None,
        "tp1":round(tp1,2) if tp1 else None,
        "tp2":round(tp2,2) if tp2 else None,
        "risk_reward":rr,
        "warning":"规则引擎示例，非个性化投资建议；首版仅模拟交易。"
    }
