from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# OTC to Binance symbol converter
def convert_symbol(pair):
    mapping = {
        "AUD/USD": "AUDUSDT",
        "EUR/USD": "EURUSDT",
        "GBP/USD": "GBPUSDT",
        "USD/JPY": "USDJPY",
        "USD/CHF": "USDCHF",
        "USD/CAD": "USDCAD",
        "NZD/USD": "NZDUSDT",
        "BTC/USD": "BTCUSDT",
        "ETH/USD": "ETHUSDT",
        "LTC/USD": "LTCUSDT",
        "DOGE/USD": "DOGEUSDT",
        "XRP/USD": "XRPUSDT",
        "USD/BRL": "USDTBRL",
        "EUR/GBP": "EURGBP",
        "EUR/JPY": "EURJPY",
        "AUD/JPY": "AUDJPY",
        "GBP/JPY": "GBPJPY",
        "AUD/CHF": "AUDCHF",
        "CHF/JPY": "CHFJPY",
        "EUR/AUD": "EURAUD",
        "EUR/CHF": "EURCHF",
        "USD/NOK": "USDNOK",
        "USD/TRY": "USDTRY",
        "USD/ZAR": "USDZAR",
        "AUD/NZD": "AUDNZD"
        # Add more if needed
    }

    # Remove " (OTC)" from pair name
    pair_clean = pair.replace(" (OTC)", "")
    return mapping.get(pair_clean, pair_clean.replace("/", "") + "USDT")

# High-accuracy AI-style logic
def calculate_momentum(closes):
    return (closes[-1] - closes[-5]) / closes[-5] * 100

def calculate_volatility(closes):
    return max(closes[-5:]) - min(closes[-5:])

def calculate_trend_strength(closes):
    short_avg = sum(closes[-5:]) / 5
    long_avg = sum(closes[-20:]) / 20
    return short_avg - long_avg

def final_ai_decision(closes):
    momentum = calculate_momentum(closes)
    volatility = calculate_volatility(closes)
    strength = calculate_trend_strength(closes)

    score = 0
    if momentum > 0: score += 1
    else: score -= 1

    if volatility > 0.3: score += 1
    else: score -= 1

    if strength > 0: score += 1
    else: score -= 1

    signal = "UP 🔼" if score >= 1 else "DOWN 🔽"
    return signal, round(momentum, 2), round(volatility, 4), round(strength, 4)

@app.route('/get-signal', methods=['POST'])
def get_signal():
    data = request.json
    pair = data.get("pair", "ETH/USD")
    interval = data.get("interval", "1m")
    symbol = convert_symbol(pair)

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"

    try:
        response = requests.get(url)
        candles = response.json()
        closes = [float(c[4]) for c in candles]

        signal, momentum, volatility, strength = final_ai_decision(closes)
        return jsonify({
            "symbol": symbol,
            "signal": signal,
            "momentum": momentum,
            "volatility": volatility,
            "trend_strength": strength
        })

    except Exception as e:
        return jsonify({ "error": str(e) })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
