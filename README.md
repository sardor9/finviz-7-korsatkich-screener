# Finviz 7-Ko'rsatkich Screener

Finviz.com'dan aksiyalarni **7 ta asosiy fundamental ko'rsatkich** bo'yicha avtomatik skrining qiluvchi Python script.

Ko'rsatkichlar (WeGrowInvest metodologiyasi asosida):

| # | Ko'rsatkich | Nima ko'rsatadi |
|---|---|---|
| 1 | **P/E** | Narx / foyda nisbati |
| 2 | **EPS Growth** | Bir aksiyaga to'g'ri keladigan foyda o'sishi |
| 3 | **Debt/Equity** | Qarzning kapitalga nisbati |
| 4 | **P/FCF** | Erkin pul oqimiga nisbatan narx |
| 5 | **ROE** | O'z kapital rentabelligi |
| 6 | **Net Profit Margin** | Sof foyda marjasi |
| 7 | **Sales Growth (5y)** | Tushum o'sish sur'ati |

Script filtrdan o'tgan har bir aksiyaga 0–100 oralig'ida oddiy **sifat balli** hisoblab, natijani CSV faylga saqlaydi.

> ⚠️ Bu vosita moliyaviy maslahat emas — faqat dastlabki saralash uchun. Yakuniy qarordan oldin har bir kompaniyani alohida chuqur tahlil qiling.

---

## O'rnatish

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/<username>/finviz-7-korsatkich-screener.git
cd finviz-7-korsatkich-screener
```

### 2. Virtual muhit (venv) yaratish

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Muvaffaqiyatli faollashtirilsa, terminal boshida `(venv)` yozuvi paydo bo'ladi.

### 3. Kerakli kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

---

## Ishlatish

Standart sozlamalar bilan:

```bash
python finviz_7_korsatkich_screener.py
```

Parametrlarni sozlab ishlatish:

```bash
python finviz_7_korsatkich_screener.py --max-pe 20 --min-roe 20 --top 15
python finviz_7_korsatkich_screener.py --sector Technology
```

### Mavjud parametrlar

| Parametr | Tavsif | Default |
|---|---|---|
| `--max-pe` | Maksimal P/E | `25` |
| `--min-roe` | Minimal ROE (%) | `15` |
| `--min-margin` | Minimal Net Profit Margin (%) | `10` |
| `--max-debt-equity` | Maksimal Debt/Equity | `1` |
| `--max-pfcf` | Maksimal Price/Free Cash Flow | `30` |
| `--sector` | Sektor filtri (masalan `Technology`) | — |
| `--market-cap` | Market cap filtri | — |
| `--top` | Natijada nechta aksiya ko'rsatilsin | `20` |
| `--out` | Chiqish CSV fayl nomi | `finviz_natija.csv` |

---

## Natija

Script terminalda jadval chiqaradi va natijani CSV faylga saqlaydi:

```
Ticker  Company        Sector       P/E   EPS this Y   ROE   Profit M   Sifat_balli
AAPL    Apple Inc.     Technology   28.4  12.3         147.9 25.3       78.5
...
```

---

## Ishdan chiqishi mumkin bo'lgan holatlar

Finviz vaqti-vaqti bilan jadval ustunlari nomini o'zgartirib turadi. Agar `KeyError` chiqsa:

1. Script konsolga chiqargan `Valuation ustunlari:` va `Financial ustunlari:` ro'yxatini tekshiring
2. `finviz_7_korsatkich_screener.py` ichidagi `wanted_val` va `wanted_fin` ro'yxatlarini haqiqiy nomlarga moslang

---

## Talablar

- Python 3.9+
- Internet aloqasi (finviz.com ochiq screener sahifasiga so'rov yuboriladi)

## Litsenziya

Shaxsiy foydalanish uchun. Finviz.com'ning foydalanish shartlariga rioya qiling.
