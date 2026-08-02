# https://m.stock.naver.com/front-api/marketIndex/standardInterest?category=standardInterest&reutersCode=USA&page=1
"""
- Federal Funds Rate (Fed Rate)
- Bank of Korea Base Rate
"""

import requests
import pandas as pd
from collector.data_processor.standard_interest_data_processor import standard_interest_data_processor
from datetime import datetime, timedelta

def standard_interest_data_reader(day, code):

    today = datetime.now()

    target_day = today - timedelta(days=day)

    start = target_day
    end = today

    page = 1
    dfs = []

    code_trans = {
        "Korea_Rate": "KOR",
        "Fed_Rate": "USA"
    }

    code = code_trans[code]
    
    while True:
        url = (
            "https://m.stock.naver.com/front-api/marketIndex/standardInterest"
            f"?category=standardInterest"
            f"&reutersCode={code}"
            f"&page={page}"
        )
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://m.stock.naver.com/"
        }
        
        response = requests.get(url, headers=headers)
        
        standard_interest_data = response.json()

        if not standard_interest_data.get("result"):
            break    

        page_df = standard_interest_data_processor(standard_interest_data, code)

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

    standard_interest_data = pd.concat(dfs, ignore_index=True)

    standard_interest_data = standard_interest_data[
        (standard_interest_data["date"] >= start) &
        (standard_interest_data["date"] <= end)
    ]
    
    standard_interest_data = (
        standard_interest_data
        .sort_values("date")
        .reset_index(drop=True)
    )

    standard_interest_data["day"] = day

    return standard_interest_data  # ["date", "code", "close", "change", "rate"]
