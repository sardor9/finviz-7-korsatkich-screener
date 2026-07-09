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
