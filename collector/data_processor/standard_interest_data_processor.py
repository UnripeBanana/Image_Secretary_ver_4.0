import pandas as pd

def standard_interest_data_processor(data, code):

    # 네이버 증권에서 받은 오리지널 데이터
    standard_interest_df = pd.DataFrame(data["result"])

    # 오리지널 데이터에서 불필요한 부분 제거
    standard_interest_df = standard_interest_df[["localTradedAt", "closePrice", "fluctuations"]]

    # 기존에 사용 중인 명칭으로 변경
    standard_interest_df = standard_interest_df.rename(columns={
        "localTradedAt": "date",
        "closePrice": "close",
        "fluctuations": "change"
    })

    if standard_interest_df["close"][0] in ["-", None]:
        standard_interest_df["date"] = standard_interest_df["date"][1:]
        standard_interest_df["close"] = standard_interest_df["close"][1:]
        standard_interest_df["change"] = standard_interest_df["change"][1:]
        

    # str -> int
    standard_interest_df["close"] = (
        standard_interest_df["close"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # str -. int
    standard_interest_df["change"] = (
        standard_interest_df["change"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # 사용자로부터 입력받은 데이터 입력
    standard_interest_df["code"] = code

    # 데이터프레임 컬럼 순서 설정
    standard_interest_df = standard_interest_df[
        ["date", "code", "close", "change"]
    ]

    # 날짜 순으로 정렬 후 return
    return (standard_interest_df.sort_values("date").reset_index(drop=True))
