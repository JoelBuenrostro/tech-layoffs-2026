"""
enrich_stock_data.py
Consulta Yahoo Finance para obtener la reacción de bolsa en la fecha del despido.
Solo aplica a empresas públicas — las privadas se marcan como "N/A".

Requisito: pip install yfinance
Uso:       python3 scripts/enrich_stock_data.py
"""

import csv
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "tech_layoffs_2026_tracker.csv"

# ── Mapa empresa → ticker ─────────────────────────────────────────────────
# Empresas privadas o sin bolsa se marcan como None
TICKERS = {
    "Meta":       "META",
    "Playtika":   "PLTK",
    "Cyberark":   "CYBR",
    "TrueCar":    "TRUE",
    "WiseTech":   "WTC.AX",   # ASX (Australia)
    "C3.ai":      "AI",
    "Deliveroo":  "ROO.L",    # London Stock Exchange
    "Stone":      "STNE",
    "Spotify":    "SPOT",
    "Snap":       "SNAP",
    # Privadas — no tienen cotización
    "eToro":      None,
    "Aleph Alpha":None,
    "Tipalti":    None,
    "Polygon":    None,
    "Moon Active":None,
    "Kiwi.com":   None,
    "Zupee":      None,
    "Huawei":     None,
    "Axonius":    None,
    "Zendesk":    None,   # Tomada privada en 2022
    "Epic Games": None,
    "Enpal":      None,
    "Monzo":      None,
    "UKG":        None,
    "Shutterfly": None,
}

def get_stock_reaction(ticker: str, date_str: str) -> tuple[str, float | None]:
    """
    Devuelve (reacción, pct_change) para el día del anuncio.
    Umbral: >1% = Positive, <-1% = Negative, resto = Neutral
    """
    try:
        dt     = datetime.strptime(date_str, "%Y-%m-%d")
        start  = (dt - timedelta(days=5)).strftime("%Y-%m-%d")
        end    = (dt + timedelta(days=2)).strftime("%Y-%m-%d")

        hist = yf.Ticker(ticker).history(start=start, end=end)
        if hist.empty or len(hist) < 2:
            return "N/D", None

        # Buscar la fila más cercana a la fecha del anuncio
        hist.index = hist.index.tz_localize(None) if hist.index.tz else hist.index
        closest = min(hist.index, key=lambda x: abs((x - dt).days))
        idx     = hist.index.get_loc(closest)

        if idx == 0:
            return "N/D", None

        prev_close = hist["Close"].iloc[idx - 1]
        day_close  = hist["Close"].iloc[idx]
        pct        = ((day_close - prev_close) / prev_close) * 100

        if pct > 1.0:
            reaction = "Positive"
        elif pct < -1.0:
            reaction = "Negative"
        else:
            reaction = "Neutral"

        return reaction, round(pct, 2)

    except Exception as e:
        print(f"  ⚠ Error con {ticker}: {e}")
        return "N/D", None


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    updated = 0
    for row in rows:
        if row.get("stock_reaction", "").strip():
            continue  # Ya tiene datos

        company = row["company"]
        date    = row["layoff_date"]
        ticker  = TICKERS.get(company)

        if ticker is None:
            row["stock_reaction"] = "N/A"
            print(f"  ⏭  {company:25} → privada (N/A)")
            updated += 1
            continue

        print(f"  📈 {company:25} ({ticker}) @ {date}...", end=" ", flush=True)
        reaction, pct = get_stock_reaction(ticker, date)
        row["stock_reaction"] = reaction

        if pct is not None:
            row["stock_change_day_pct"] = pct
            print(f"{reaction} ({pct:+.2f}%)")
        else:
            print(f"{reaction}")
        updated += 1

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ {updated} registros actualizados en {CSV_PATH.name}")
    print("   Corre: python3 scripts/process_data.py para regenerar los JSONs")


if __name__ == "__main__":
    main()
