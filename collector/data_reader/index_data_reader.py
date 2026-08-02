#https://m.stock.naver.com/front-api/stock/domestic/index/price/list?code=KOSPI&page=1&pageSize=50
#(일봉, 주봉, 월봉 그리기 가능)
"""
- KOSPI
- KOSDAQ
- S&P 500
- NASDAQ
- VIX
"""

import requests
import pandas as pd
from collector.data_processor.index_data_processor import index_data_processor
from datetime import datetime, timedelta

def index_data_reader(day, code):

    today = datetime.now()

    target_day = today - timedelta(days=day)

    start = target_day
    end = today

    page = 1
    dfs = []

    code_trans = {
        "KOSPI": "KOSPI",
        "KOSDAQ": "KOSDAQ",
        "KOSPI_200": "KPI200",
        "NASDAQ": ".IXIC",
        "S&P_500": ".INX",
        "Dow_Jones": ".DJI",
        "VIX": ".VIX"
    }

    if code in ["KOSPI", "KOSDAQ", "KOSPI_200"]:
        is_foreign = "domestic"
        code = code_trans[code]
    else:
        is_foreign = "foreign"
        code = code_trans[code]

    # https://m.stock.naver.com/front-api/stock/domestic/index/price/list?code=KOSPI&page=1&pageSize=10
    while True:
        url = (
            f"https://m.stock.naver.com/front-api/stock/{is_foreign}/index/price/list"
            f"?code={code}"
            f"&page={page}"
            "&pageSize=50"
        )
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://m.stock.naver.com/"
        }
        
        response = requests.get(url, headers=headers)
        
        index_data = response.json()

        if not index_data.get("result"):
            break    

        page_df = index_data_processor(index_data, code)

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

    index_data = pd.concat(dfs, ignore_index=True)

    index_data = index_data[
        (index_data["date"] >= start) &
        (index_data["date"] <= end)
    ]
    
    index_data = (
        index_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    index_data["day"] = day

    return index_data
