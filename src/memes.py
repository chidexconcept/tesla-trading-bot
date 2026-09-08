import requests
import pandas as pd

class DexScreenerScanner:
    def __init__(self, min_liquidity_usd=10000, min_volume_5m=2500):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.min_liquidity_usd = min_liquidity_usd
        self.min_volume_5m = min_volume_5m

    def scan_market(self, search_terms=["SOL", "PEPE"]):
        print("\n--- Scanning DEX Meme Liquidity Pools ---")
        signals = []

        for term in search_terms:
            try:
                res = requests.get(f"{self.base_url}/search?q={term}", timeout=10)
                if res.status_code == 200:
                    pairs = res.json().get('pairs', [])
                    for pair in pairs:
                        liquidity = float(pair.get('liquidity', {}).get('usd', 0) or 0)
                        vol_5m = float(pair.get('volume', {}).get('m5', 0) or 0)

                        if liquidity >= self.min_liquidity_usd and vol_5m >= self.min_volume_5m:
                            signals.append({
                                "chain": pair.get('chainId'),
                                "symbol": pair.get('baseToken', {}).get('symbol'),
                                "price": float(pair.get('priceUsd', 0) or 0),
                                "liquidity": liquidity,
                                "vol_5m": vol_5m,
                                "velocity": round(vol_5m / liquidity, 3)
                            })
            except Exception as e:
                print(f"[!] Error fetching {term}: {e}")

        df = pd.DataFrame(signals)
        if not df.empty:
            df = df.drop_duplicates(subset=['symbol']).sort_values(by='velocity', ascending=False)
        return df
