from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.transforms import blended_transform_factory
from matplotlib.ticker import FuncFormatter

def standard_interest_chart_maker(standard_interest_df):
    standard_interest_df = standard_interest_df.reset_index(drop=True)          # standard_interest_df index 초기화 작업(오류 방지)

    # ---------------------------------
    # 그래프 생성
    # ---------------------------------
    fig, ax = plt.subplots(figsize=(16, 9))

    x = np.arange(len(standard_interest_df))

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
    ax.set_xlim(-1, len(standard_interest_df) - 0.5)

    # 위 아래 여백 조금 주기
    price_min = standard_interest_df["close"].min()
    price_max = standard_interest_df["close"].max()

    margin = (price_max - price_min) * 0.05
    
    ax.set_ylim(
        price_min - margin,
        price_max + margin*2.5
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x:.2f}")
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
        standard_interest_df["close"],
        linewidth=1,
        drawstyle="steps-post"
    )
    
    #-----------------------------------------------------
    # 날짜 표시 
    #-----------------------------------------------------
    total_len = len(standard_interest_df)
    
    # 1. 화면에 표시할 최대 라벨 개수 설정 (16:9 비율 기준 15~20개가 적당함)
    max_labels = 12
    step = max(1, total_len // max_labels)
    
    # 2. 데이터 기간(날짜) 차이에 따라 포맷 자동 지정
    date_range_days = (standard_interest_df["date"].max() - standard_interest_df["date"].min()).days
    
    if date_range_days > 4500:        # 3년 초과 -> 연도만
        date_format = "%Y"
    elif date_range_days > 2700:           # 3개월 초과 -> 연-월
        date_format = "%Y-%m"
    else:                                # 3개월 이하 -> 월-일
        date_format = "%m-%d"

    # 3. 일정 간격(step)으로 인덱스 추출
    tick_positions = list(range(0, total_len, step))
    tick_labels = [standard_interest_df.loc[i, "date"].strftime(date_format) for i in tick_positions]

    # 4. 축 적용
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(
        tick_labels,
        rotation=0,
        fontsize=9,
        ha="center"
    )

    #-----------------------------------------------------
    # 최고가 최저가 표시
    #-----------------------------------------------------
    # 최고가 / 최저가
    high_idx = standard_interest_df["close"].idxmax()
    low_idx = standard_interest_df["close"].idxmin()
    
    high_price = standard_interest_df.loc[high_idx, "close"]
    low_price = standard_interest_df.loc[low_idx, "close"]
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
    last_close = standard_interest_df.iloc[-2]["close"]
    current_close = standard_interest_df.iloc[-1]["close"]
    
    # 당일 상승/하락에 따라 색상 결정
    current_color = "#e53935" if current_close > last_close else "#1565c0" if current_close > last_close else "#000000"

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
        "KOR": "Korea_Rate",
        "USA": "Fed_Rate"
    }
    
    name = code_trans[standard_interest_df.iloc[0]["code"]]
    day = standard_interest_df.iloc[0]["day"]

    title = f"data/image/standard_interest/{name}_{day}days_chart.png"

    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)
