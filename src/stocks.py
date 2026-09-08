import os
import alpaca_trade_api as tradeapi

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

def run_stock_scanner():
    print("\n--- Running Tesla Stock Strategy Engine ---")
    if not API_KEY or not SECRET_KEY:
        print("[!] Alpaca keys missing. Skipping stock execution.")
        return

    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    symbol = "TSLA"

    try:
        bars = api.get_bars(symbol, "15Min", limit=30).df
        if bars.empty:
            print(f"[-] No market data returned for {symbol}.")
            return

        current_price = bars['close'].iloc[-1]
        sma_fast = bars['close'].tail(10).mean()
        sma_slow = bars['close'].tail(30).mean()

        print(f"Current TSLA Price: ${current_price:.2f} | Fast SMA: ${sma_fast:.2f} | Slow SMA: ${sma_slow:.2f}")

        if sma_fast > sma_slow:
            qty_to_buy = max(1, int(1000 // current_price))
            print(f"📈 BUY Signal! Placing paper order for {qty_to_buy} shares of TSLA.")
            api.submit_order(
                symbol=symbol,
                qty=qty_to_buy,
                side='buy',
                type='market',
                time_in_force='gtc',
                order_class='bracket',
                stop_loss={'stop_price': round(current_price * 0.96, 2)}
            )
        else:
            print("[-] Signal Neutral/Bearish. Holding position.")

    except Exception as e:
        print(f"[!] Stock Execution Error: {e}")
