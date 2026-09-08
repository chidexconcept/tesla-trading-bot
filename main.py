from src.stocks import run_stock_scanner
from src.memes import DexScreenerScanner

def run():
    print("==================================================")
    print("⚡ STARTING TESLA LIVE MULTI-MARKET EXECUTION ⚡")
    print("==================================================")

    # 1. Run Meme Liquidity Scanner
    scanner = DexScreenerScanner(min_liquidity_usd=15000, min_volume_5m=3000)
    meme_df = scanner.scan_market()

    if not meme_df.empty:
        print("\n⚡ HIGH-MOMENTUM DEX TOKENS FOUND ⚡")
        print(meme_df.head(5).to_string(index=False))
    else:
        print("\n[-] No meme pools matched execution velocity criteria.")

    # 2. Run Tesla Stock Algorithm
    run_stock_scanner()

if __name__ == "__main__":
    run()
