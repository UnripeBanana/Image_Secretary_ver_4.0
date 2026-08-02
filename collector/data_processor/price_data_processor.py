import pandas as pd

def price_data_processor(data, code):

    # 네이버 증권에서 받은 오리지널 데이터
    price_df = pd.DataFrame(data["result"])

    # 오리지널 데이터에서 불필요한 부분 제거
    price_df = price_df[["localTradedAt", "closePrice", "fluctuations", "fluctuationsRatio"]]

    # 기존에 사용 중인 명칭으로 변경
    price_df = price_df.rename(columns={
        "localTradedAt": "date",
        "closePrice": "close",
        "fluctuations": "change",
        "fluctuationsRatio": "rate"
    })

    # str -> int
    price_df["close"] = (
        price_df["close"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -. int
    price_df["change"] = (
        price_df["change"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -> float
    price_df["rate"] = (
        price_df["rate"]
        .astype(float)
    )

    # 사용자로부터 입력받은 데이터 입력
    price_df["code"] = code

    # 데이터프레임 컬럼 순서 설정
    price_df = price_df[
        ["date", "code", "close", "change", "rate"]
    ]

    # 날짜 순으로 정렬 후 return
    return (
        price_df
        .sort_values("date")
        .reset_index(drop=True)
    )
