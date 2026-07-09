"""
Finviz 7 Ko'rsatkich Screener
==============================
WeGrowInvest postidagi 7 ta fundamental ko'rsatkichga asoslanib
Finviz.com'dan aksiyalarni skrining qiladi:

  1. P/E              - Narx/foyda nisbati
  2. EPS growth        - Bir aksiyaga to'g'ri keladigan foyda o'sishi
  3. Debt/Equity        - Qarzning kapitalga nisbati
  4. Price/Free Cash Flow - Erkin pul oqimiga nisbatan narx (FCF proksi)
  5. ROE                - O'z kapital rentabelligi
  6. Net Profit Margin  - Sof foyda marjasi
  7. Sales growth (5y)  - Tushum o'sish sur'ati

O'RNATISH:
    pip install finvizfinance pandas

ISHLATISH:
    python finviz_7_korsatkich_screener.py
    python finviz_7_korsatkich_screener.py --max-pe 20 --min-roe 20 --top 15
    python finviz_7_korsatkich_screener.py --sector Technology

ESLATMA: Bu skript finviz.com saytiga so'rov yuboradi (ochiq/bepul screener
sahifasi). Internet aloqasi bo'lgan kompyuteringizda ishga tushiring.
"""

import argparse
import sys
from datetime import datetime

try:
    import pandas as pd
    from finvizfinance.screener.overview import Overview
    from finvizfinance.screener.valuation import Valuation
    from finvizfinance.screener.financial import Financial
except ImportError:
    print("Kerakli kutubxonalar topilmadi. Avval quyidagini ishga tushiring:")
    print("    pip install finvizfinance pandas")
    sys.exit(1)


def build_filters(args):
    """Foydalanuvchi parametrlariga qarab Finviz server-tomon filtrlarini yig'adi.
    Bu qism so'rovni tezlashtiradi, chunki filtrlash Finviz serverida bo'ladi."""
    filters = {
        "P/E": f"Under {args.max_pe}",
        "Debt/Equity": f"Under {args.max_debt_equity}",
        "Return on Equity": f"Over +{args.min_roe}%",
        "Net Profit Margin": f"Over {args.min_margin}%",
        "EPS growththis year": "Positive (>0%)",
        "Sales growthpast 5 years": "Positive (>0%)",
        "Price/Free Cash Flow": f"Under {args.max_pfcf}",
    }
    if args.sector:
        filters["Sector"] = args.sector
    if args.market_cap:
        filters["Market Cap."] = args.market_cap
    return filters


def fetch_screened_tickers(filters, verbose=True):
    """Overview view orqali filtrlangan tikerlar ro'yxatini oladi."""
    fo = Overview()
    fo.set_filter(filters_dict=filters)
    df = fo.screener_view(verbose=1 if verbose else 0)
    return df


def enrich_with_metrics(overview_df, verbose=True):
    """Valuation va Financial view'laridan qo'shimcha ko'rsatkichlarni olib,
    tiker bo'yicha birlashtiradi."""
    if overview_df is None or overview_df.empty:
        return overview_df

    tickers = ",".join(overview_df["Ticker"].tolist())

    fv = Valuation()
    fv.set_filter(ticker=tickers)
    val_df = fv.screener_view(verbose=1 if verbose else 0)

    ff = Financial()
    ff.set_filter(ticker=tickers)
    fin_df = ff.screener_view(verbose=1 if verbose else 0)

    if verbose:
        print("Valuation ustunlari:", list(val_df.columns))
        print("Financial ustunlari:", list(fin_df.columns))

    wanted_val = ["Ticker", "P/E", "PEG", "P/FCF", "EPS this Y"]
    wanted_fin = ["Ticker", "ROE", "ROI", "Debt/Eq", "Gross M", "Oper M", "Profit M", "Sales Q/Q"]

    val_cols = [c for c in wanted_val if c in val_df.columns]
    fin_cols = [c for c in wanted_fin if c in fin_df.columns]

    merged = overview_df.merge(
        val_df[val_cols], on="Ticker", how="left", suffixes=("", "_val")
    )
    merged = merged.merge(
        fin_df[fin_cols], on="Ticker", how="left"
    )
    return merged


def to_num(series):
    """'%' va boshqa belgilarni tozalab, raqamga o'giradi."""
    return pd.to_numeric(
        series.astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False),
        errors="coerce"
    )


def get_col(d, name):
    """Ustun mavjud bo'lmasa, NaN'lardan iborat seriya qaytaradi (crash bo'lmasligi uchun)."""
    if name in d.columns:
        return d[name]
    return pd.Series([float("nan")] * len(d), index=d.index)


def score_quality(df):
    """7 ta ko'rsatkichga asoslangan oddiy sifat balli (0-100).
    Bu qat'iy moliyaviy tahlil emas, balki dastlabki saralash uchun tezkor reyting."""
    d = df.copy()

    pe = to_num(get_col(d, "P/E"))
    eps_g = to_num(get_col(d, "EPS this Y"))
    debt_eq = to_num(get_col(d, "Debt/Eq"))
    pfcf = to_num(get_col(d, "P/FCF"))
    roe = to_num(get_col(d, "ROE"))
    margin = to_num(get_col(d, "Profit M"))
    sales_q = to_num(get_col(d, "Sales Q/Q"))

    def norm(x, lo, hi, invert=False):
        x = x.clip(lower=lo, upper=hi)
        s = (x - lo) / (hi - lo) * 100
        return 100 - s if invert else s

    score = (
        norm(pe, 0, 40, invert=True) * 0.15 +
        norm(eps_g, 0, 40) * 0.15 +
        norm(debt_eq, 0, 2, invert=True) * 0.15 +
        norm(pfcf, 0, 40, invert=True) * 0.15 +
        norm(roe, 0, 40) * 0.15 +
        norm(margin, 0, 30) * 0.15 +
        norm(sales_q, 0, 30) * 0.10
    )
    d["Sifat_balli"] = score.round(1)
    return d


def main():
    parser = argparse.ArgumentParser(description="Finviz 7-ko'rsatkich aksiya screener")
    parser.add_argument("--max-pe", type=int, default=25, help="Maksimal P/E (default: 25)")
    parser.add_argument("--min-roe", type=int, default=15, help="Minimal ROE %% (default: 15)")
    parser.add_argument("--min-margin", type=int, default=10, help="Minimal Net Profit Margin %% (default: 10)")
    parser.add_argument("--max-debt-equity", type=str, default="1", help="Maksimal Debt/Equity (default: 1)")
    parser.add_argument("--max-pfcf", type=int, default=30, help="Maksimal Price/Free Cash Flow (default: 30)")
    parser.add_argument("--sector", type=str, default="", help="Sektor filtri (masalan: Technology)")
    parser.add_argument("--market-cap", type=str, default="", help="Market cap filtri (masalan: +Large (over $10bln))")
    parser.add_argument("--top", type=int, default=20, help="Natijada nechta aksiya ko'rsatilsin (default: 20)")
    parser.add_argument("--out", type=str, default="finviz_natija.csv", help="Chiqish CSV fayl nomi")
    args = parser.parse_args()

    print("Finviz'dan filtrlangan aksiyalar olinmoqda...\n")
    filters = build_filters(args)
    for k, v in filters.items():
        print(f"  {k}: {v}")
    print()

    overview_df = fetch_screened_tickers(filters)
    if overview_df is None or overview_df.empty:
        print("Hech qanday aksiya topilmadi. Filtrlarni yumshating (masalan --max-pe 40).")
        return

    print(f"\n{len(overview_df)} ta aksiya dastlabki filtrdan o'tdi. Qo'shimcha ko'rsatkichlar yuklanmoqda...\n")
    full_df = enrich_with_metrics(overview_df)
    scored_df = score_quality(full_df)

    scored_df = scored_df.sort_values("Sifat_balli", ascending=False)

    cols = ["Ticker", "Company", "Sector", "Industry", "Price", "P/E", "EPS this Y",
            "Debt/Eq", "P/FCF", "ROE", "Profit M", "Sales Q/Q", "Sifat_balli"]
    cols = [c for c in cols if c in scored_df.columns]
    result = scored_df[cols].head(args.top)

    print(result.to_string(index=False))

    result.to_csv(args.out, index=False)
    print(f"\nNatija saqlandi: {args.out}")
    print(f"Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("\nESLATMA: Bu skript faqat dastlabki saralash uchun. Yakuniy qaror qilishdan "
          "oldin har bir kompaniyani alohida chuqur tahlil qiling.")


if __name__ == "__main__":
    main()