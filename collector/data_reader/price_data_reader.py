# https://m.stock.naver.com/front-api/marketIndex/prices?category=bond&reutersCode=US2YT%3DRR&page=1
"""
- US 2-Year Treasury Yield
- US 10-Year Treasury Yield
- US 30-Year Treasury Yield
- KR 3-Year Government Bond Yield
- KR 10-Year Government Bond Yield
- KR 30-Year Government Bond Yield
- USD/KRW
- Dollar Index (DXY)
- USD/JPY
- EUR/USD
- Gold
- Silver
- WTI Crude Oil
- Brent Crude Oil
- Natural Gas
- Copper
"""

import requests
import pandas as pd
from collector.data_processor.price_data_processor import price_data_processor
from datetime import datetime, timedelta

def price_data_reader(day, code):

    today = datetime.now()

    target_day = today - timedelta(days=day)

    start = target_day
    end = today

    page = 1
    dfs = []

    code_trans = {
        "US2Y": "US2YT%3DRR",
        "US10Y": "US10YT%3DRR",
        "US30Y": "US30YT%3DRR",
        "KR3Y": "KR3YT%3DRR",
        "KR10Y": "KR10YT%3DRR",
        "KR30Y": "KR30YT%3DRR",
        "USD-KRW": "FX_USDKRW",
        "Dolar_Index": ".DXY",
        "USD-JPY": "USDJPY",
        "USD-EUR": "USDEUR",
        "KRX_Gold": "M04020000",
        "International_Gold": "GCcv1",
        "Silver": "SIcv1",
        "WTI_Crude_Oil": "CLcv1",
        "Brent_Crude_Oil": "LCOcv1",
        "Natural_Gas": "NGcv1",
        "Copper": "CMCU0"
    }

    code = code_trans[code]

    if code in ["US2YT%3DRR", "US10YT%3DRR", "US30YT%3DRR", "KR3YT%3DRR", "KR10YT%3DRR", "KR30YT%3DRR"]:
        category = "bond"
    elif code in ["M04020000", "GCcv1", "SIcv1", "CLcv1", "LCOcv1", "NGcv1", "CMCU0"]:
        category = "metals"
    elif code in ["FX_USDKRW", ".DXY"]:
        category = "exchange"
    elif code in ["USDJPY", "USDEUR"]:
        category = "exchangeWorld"
    else:
        raise ValueError(f"Invalid code: {code}")

    currency_list = {
        "US2YT%3DRR": "%",
        "US10YT%3DRR": "%",
        "US30YT%3DRR": "%",
        "KR3YT%3DRR": "%",
        "KR10YT%3DRR": "%",
        "KR30YT%3DRR": "%",
        "M04020000": "KRW/g",
        "GCcv1": "USD/OZS",
        "SIcv1": "USD/OZS",
        "CLcv1": "USD/BBL",
        "LCOcv1": "USD/BBL",
        "NGcv1": "USD/MMBTU",
        "CMCU0": "USD/TONNE",
        "FX_USDKRW": "USD/KRW",
        ".DXY": "-",
        "USDJPY": "USD/JPY",
        "USDEUR": "USD/EUR"
    }


    while True:
        url = (
            "https://m.stock.naver.com/front-api/marketIndex/prices"
            f"?category={category}"
            f"&reutersCode={code}"
            f"&page={page}"
        )

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://m.stock.naver.com/"
        }

        response = requests.get(url, headers=headers)

        price_data = response.json()

        if not price_data.get("result"):
            break

        page_df = price_data_processor(price_data, code)

        page_df["date"] = (
            pd.to_datetime(page_df["date"], utc=True)
              .dt.date
        )
        page_df["date"] = pd.to_datetime(page_df["date"])

        dfs.append(page_df)

        oldest = page_df["date"].min()


        if oldest <= start:
            break

        page += 1

    price_data = pd.concat(dfs, ignore_index=True)

    price_data["currency"] = currency_list[code]

    price_data = price_data[
        (price_data["date"] >= start) &
        (price_data["date"] <= end)
    ]

    price_data = (
        price_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    price_data["day"] = day

    return price_data  # ["date", "code", "close", "change", "rate", "currency"]
