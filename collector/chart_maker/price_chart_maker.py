from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.transforms import blended_transform_factory
from matplotlib.ticker import FuncFormatter

def price_chart_maker(price_df):
    price_df = price_df.reset_index(drop=True)          # price_df index 초기화 작업(오류 방지)

    # ---------------------------------
    # 그래프 생성
    # ---------------------------------
    fig, ax = plt.subplots(figsize=(16, 9))

    x = np.arange(len(price_df))

    #-----------------------------------------------------
    # 축 설정
    #-----------------------------------------------------
    # 테두리 제거
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # y축을 오른쪽으로 이동
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")

    ax.tick_params(
        axis="x",
        bottom=False,       # 아래쪽 눈금 숨김
        labelbottom=True,   # 아래쪽 라벨 표시
        top=False,          # 위쪽 눈금 숨김
        labeltop=False      # 위쪽 라벨 숨김
    )

    ax.tick_params(
        axis="y",
        left=False,
        labelleft=False,
        right=False,
        labelright=True
    )

    # 양 옆 여백 조금 주기
    ax.set_xlim(-1, len(price_df) - 0.5)

    # 위 아래 여백 조금 주기
    price_min = price_df["close"].min()
    price_max = price_df["close"].max()

    margin = (price_max - price_min) * 0.05
    
    ax.set_ylim(
        price_min - margin,
        price_max + margin*2.5
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{int(x):,}")
    )

    # x축에 평행한 선 그리기
    ax.grid(
        axis="y",
        color="gray",
        alpha=0.15,
        linewidth=0.8
    )
    
    #-----------------------------------------------------
    # 그래프 생성
    #-----------------------------------------------------
    ax.plot(
        x,
        price_df["close"],
        linewidth=1
    )
    
    #-----------------------------------------------------
    # 날짜 표시 (매주 첫 거래일)
    #-----------------------------------------------------
    tick_positions = []
    tick_labels = []
    week_count = 0
    
    last_week = None

    if len(x) > 900:
        for i, row in price_df.iterrows():
            
            week = row["date"].isocalendar().week
        
            if week != last_week:
                if not week_count%(len(x)//50):
                    tick_positions.append(i)
                    tick_labels.append(row["date"].strftime("%Y")) 
                last_week = week
                week_count += 1

    elif len(x) > 240:
        for i, row in price_df.iterrows():
            
            week = row["date"].isocalendar().week
        
            if week != last_week:
                if not week_count%(len(x)//50):
                    tick_positions.append(i)
                    tick_labels.append(row["date"].strftime("%Y-%m"))
                last_week = week
                week_count += 1

    elif len(x) > 80:
        for i, row in defaultdict.iterrows():
            
            week = row["date"].isocalendar().week
        
            if week != last_week:
                if not week_count%(len(x)//50):
                    tick_positions.append(i)
                    tick_labels.append(row["date"].strftime("%m-%d"))
                last_week = week
                week_count += 1

    else:
        for i, row in price_df.iterrows():

            week = row["date"].isocalendar().week
        
            if week != last_week:
                tick_positions.append(i)
                tick_labels.append(row["date"].strftime("%m-%d"))
                last_week = week
    
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(
        tick_labels,
        rotation=0,
        fontsize=9
    )

    #-----------------------------------------------------
    # 최고가 최저가 표시
    #-----------------------------------------------------
    # 최고가 / 최저가
    high_idx = price_df["close"].idxmax()
    low_idx = price_df["close"].idxmin()
    
    high_price = price_df.loc[high_idx, "close"]
    low_price = price_df.loc[low_idx, "close"]
    x_offset = len(x) * 0.007
    y_offset = (price_max - price_min) * 0.01

    
    # 최고가 표시
    ax.plot(
        high_idx,                            # x 좌표
        high_price + y_offset,                 # y 좌표
        marker="v",                          # ▼ 표시
        color="gray",
        markersize = 5
    )

    if len(x)*0.5 < high_idx:
        x_cord = high_idx - x_offset
        ha = "right"
    else:
        x_cord = high_idx + x_offset
        ha = "left"
        
    ax.text(
        x_cord,                              # x 좌표
        high_price + y_offset,               # ▼와 같은 높이
        f"High Price {high_price:,}",
        va = "center",
        ha = ha,
        fontsize = 8,
        color="gray"
    )
    
    # 최저가 표시
    ax.plot(
        low_idx,
        low_price - y_offset,
        marker="^",                          # ▲ 표시
        color="gray",
        markersize = 5
    )

    if low_idx < len(x)*0.5:
        x_cord = low_idx + x_offset
        ha = "left"
    else:
        x_cord = low_idx - x_offset
        ha = "right"


    ax.text(
        x_cord,                       # x 좌표
        low_price - y_offset,           # ▲와 같은 높이
        f"Low Price {low_price:,}",
        va = "center",
        ha = ha,
        fontsize = 8,
        color="gray"
    )

    #-----------------------------------------------------
    # 현재가 표시
    #-----------------------------------------------------
    last_close = price_df.iloc[-2]["close"]
    current_close = price_df.iloc[-1]["close"]
    
    # 당일 상승/하락에 따라 색상 결정
    current_color = "#e53935" if current_close >= last_close else "#1565c0"

    transform = blended_transform_factory(
        ax.transAxes,   # x는 축 좌표
        ax.transData    # y는 데이터 좌표
    )

    triangle_height = (price_max - price_min) * 0.014
    triangle = Polygon(
        [
            [0.9998, current_close],
            [1.006, current_close + triangle_height],
            [1.006, current_close - triangle_height]
        ],
        closed=True,
        facecolor=current_color,
        edgecolor="none",
        transform=transform,
        clip_on=False
    )

    ax.add_patch(triangle)

    ax.text(
        1.0075,                 # 축의 오른쪽 바깥 0.75%
        current_close,             # 실제 현재가
        f"{current_close:,}",
        transform=transform,
        ha="left",
        va="center",
        fontsize=9,
        color="white",
        bbox=dict(
            boxstyle="round,pad=0.3",
            fc=current_color,
            ec="none"
        )
    )
    
    # ---------------------------------
    # 화면 출력
    # ---------------------------------
    plt.show()

    # 저장
    plt.tight_layout()

    code_trans = {
        "US2YT%3DRR": "US2Y",
        "US10YT%3DRR": "US10Y",
        "US30YT%3DRR": "US30Y",
        "KR3YT%3DRR": "KR3Y",
        "KR10YT%3DRR": "KR10Y",
        "KR30YT%3DRR": "KR30Y",
        "FX_USDKRW": "USD-KRW",
        ".DXY": "Dolar_Index",
        "USDJPY": "USD-JPY",
        "USDEUR": "USD-EUR",
        "M04020000": "KRX_Gold",
        "GCcv1": "International_Gold",
        "SIcv1": "Silver",
        "CLcv1": "WTI_Crude_Oil",
        "LCOcv1": "Brent_Crude_Oil",
        "NGcv1": "Natural_Gas",
        "CMCU0": "Copper"
    }
    
    name = code_trans[price_df.iloc[0]["code"]]
    day = price_df.iloc[0]["day"]

    title = f"data/image/price/{name}_{day}days_chart.png"

    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
