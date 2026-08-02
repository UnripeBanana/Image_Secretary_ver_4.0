from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.transforms import blended_transform_factory
from matplotlib.ticker import FuncFormatter

def double_price_data_chart_maker(price_df):
    price_df1, price_df2 = price_df

    price_df1 = price_df1.reset_index(drop=True)          # price_df1 index 초기화 작업(오류 방지)
    price_df2 = price_df2.reset_index(drop=True)          # price_df2 index 초기화 작업(오류 방지)

    merged = pd.merge(
        price_df1,
        price_df2,
        on="date",
        suffixes=("_1", "_2")
    )

    color_data_set = {
        "US2YT%3DRR": "#64B5F6",
        "US10YT%3DRR": "#1E88E5",
        "US30YT%3DRR": "#0D47A1",
        "KR3YT%3DRR": "#E57373",
        "KR10YT%3DRR": "#E53935",
        "KR30YT%3DRR": "#B71C1C",
        "FX_USDKRW": "#4CAF50",
        ".DXY": "#2E7D32",
        "USDJPY": "#00897B",
        "USDEUR": "#7B1FA2",
        "M04020000": "#FFD700",
        "GCcv1": "#D4AF37",
        "SIcv1": "#C0C0C0",
        "CLcv1": "#1A1A1A",
        "LCOcv1": "#333333",
        "NGcv1": "#29B6F6",
        "CMCU0": "#B87333"
    }

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

    # ---------------------------------
    # 그래프 생성
    # ---------------------------------
    fig, ax_l = plt.subplots(figsize=(16, 9))
    ax_r = ax_l.twinx()

    x = np.arange(len(merged))


    #-----------------------------------------------------
    # 축 설정
    #-----------------------------------------------------
    # 테두리 제거
    for ax in (ax_l, ax_r):
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # y축을 이동
    ax_l.yaxis.tick_right()
    ax_l.yaxis.set_label_position("right")

    ax_r.yaxis.tick_right()
    ax_r.yaxis.set_label_position("right")

    ax_l.tick_params(
        axis="x",
        bottom=False,       # 아래쪽 눈금 숨김
        labelbottom=True,   # 아래쪽 라벨 표시
        top=False,          # 위쪽 눈금 숨김
        labeltop=False      # 위쪽 라벨 숨김
    )

    ax_l.tick_params(
        axis="y",
        left=False,
        labelleft=True,
        right=False,
        labelright=False
    )

    ax_r.tick_params(
        axis="y",
        left=False,
        labelleft=False,
        right=False,
        labelright=True
    )

    # 양 옆 여백 조금 주기
    ax_l.set_xlim(-1, len(merged) - 0.5)

    # 위 아래 여백 조금 주기
    price_min1 = price_df1["close"].min()
    price_max1 = price_df1["close"].max()

    margin1 = (price_max1 - price_min1) * 0.05

    ax_l.set_ylim(
        price_min1 - margin1,
        price_max1 + margin1 * 2.5
    )

    price_min2 = price_df2["close"].min()
    price_max2 = price_df2["close"].max()

    margin2 = (price_max2 - price_min2) * 0.05

    ax_r.set_ylim(
        price_min2 - margin2,
        price_max2 + margin2 * 2.5
    )

    ax_l.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x:.2f}")
    )

    ax_r.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x:.2f}")
    )

    ax_l.tick_params(axis="y", colors=color_data_set[merged.iloc[0]["code_1"]])
    ax_r.tick_params(axis="y", colors=color_data_set[merged.iloc[0]["code_2"]])

    # -----------------------------------------------------
    # 상단 정보 표시 (단위 및 지표명)
    # -----------------------------------------------------
    # 좌측 상단 (Price 1 지표명 & 단위)
    ax_l.text(
        0.01, 0.99,                          # x, y 상대 위치 (0.01 = 왼쪽 끝, 0.96 = 상단)
        f"{code_trans[merged.iloc[0]["code_1"]]} ({merged.iloc[0]["currency_1"]})",                      # 표시할 텍스트 (지표명 + 단위)
        transform=ax_l.transAxes,
        fontsize=10,
        fontweight="bold",
        color=color_data_set[merged.iloc[0]["code_1"]],
        ha="left", va="top"
    )

    # 우측 상단 (Price 2 지표명 & 단위)
    ax_r.text(
        0.99, 0.99,                          # x, y 상대 위치 (0.99 = 오른쪽 끝, 0.96 = 상단)
        f"{code_trans[merged.iloc[0]["code_2"]]} ({merged.iloc[0]["currency_2"]})",                      # 표시할 텍스트
        transform=ax_r.transAxes,
        fontsize=10,
        fontweight="bold",
        color=color_data_set[merged.iloc[0]["code_2"]],
        ha="right", va="top"
    )

    #-----------------------------------------------------
    # 그래프 생성
    #-----------------------------------------------------
    ax_l.plot(
        x,
        merged["close_1"],
        color=color_data_set[merged.iloc[0]["code_1"]],
        linewidth=1.5,
        label="Price 1"
    )

    ax_r.plot(
        x,
        merged["close_2"],
        color=color_data_set[merged.iloc[0]["code_2"]],
        linewidth=1.5,
        label="Price 2"
    )

    #-----------------------------------------------------
    # 날짜 표시 (개선된 동적 간격 로직)
    #-----------------------------------------------------
    total_len = len(merged)
    
    # 1. 화면에 표시할 최대 라벨 개수 설정 (16:9 비율 기준 15~20개가 적당함)
    max_labels = 12
    step = max(1, total_len // max_labels)
    
    # 2. 데이터 기간(날짜) 차이에 따라 포맷 자동 지정
    date_range_days = (merged["date"].max() - merged["date"].min()).days
    
    if date_range_days > 1500:        # 3년 초과 -> 연도만
        date_format = "%Y"
    elif date_range_days > 900:           # 3개월 초과 -> 연-월
        date_format = "%Y-%m"
    else:                                # 3개월 이하 -> 월-일
        date_format = "%m-%d"

    # 3. 일정 간격(step)으로 인덱스 추출
    tick_positions = list(range(0, total_len, step))
    tick_labels = [merged.loc[i, "date"].strftime(date_format) for i in tick_positions]

    # 4. 축 적용
    ax_l.set_xticks(tick_positions)
    ax_l.set_xticklabels(
        tick_labels,
        rotation=0,
        fontsize=9,
        ha="center"
    )

    #-----------------------------------------------------
    # 최고가 최저가 표시
    #-----------------------------------------------------
    # 최고가 / 최저가
    high_idx1 = merged["close_1"].idxmax()
    low_idx1 = merged["close_1"].idxmin()

    high_price1 = merged.loc[high_idx1, "close_1"]
    low_price1 = merged.loc[low_idx1, "close_1"]
    x_offset = len(x) * 0.007
    y_offset1 = (price_max1 - price_min1) * 0.01


    # 최고가 표시
    ax_l.plot(
        high_idx1,                            # x 좌표
        high_price1 + y_offset1,                 # y 좌표
        marker="v",                          # ▼ 표시
        color=color_data_set[merged.iloc[0]["code_1"]],
        markersize = 5
    )

    if len(x)*0.5 < high_idx1:
        x_cord = high_idx1 - x_offset
        ha = "right"
    else:
        x_cord = high_idx1 + x_offset
        ha = "left"

    ax_l.text(
        x_cord,                              # x 좌표
        high_price1 + y_offset1,               # ▼와 같은 높이
        f"High Price {high_price1:,}",
        va = "center",
        ha = ha,
        fontsize = 8,
        color=color_data_set[merged.iloc[0]["code_1"]]
    )

    # 최저가 표시
    ax_l.plot(
        low_idx1,
        low_price1 - y_offset1,
        marker="^",                          # ▲ 표시
        color=color_data_set[merged.iloc[0]["code_1"]],
        markersize = 5
    )

    if low_idx1 < len(x)*0.5:
        x_cord = low_idx1 + x_offset
        ha = "left"
    else:
        x_cord = low_idx1 - x_offset
        ha = "right"


    ax_l.text(
        x_cord,                       # x 좌표
        low_price1 - y_offset1,           # ▲와 같은 높이
        f"Low Price {low_price1:,}",
        va = "center",
        ha = ha,
        fontsize = 8,
        color=color_data_set[merged.iloc[0]["code_1"]]
    )

    ##########################

    # 최고가 / 최저가
    high_idx2 = merged["close_2"].idxmax()
    low_idx2 = merged["close_2"].idxmin()

    high_price2 = merged.loc[high_idx2, "close_2"]
    low_price2 = merged.loc[low_idx2, "close_2"]
    y_offset2 = (price_max2 - price_min2) * 0.01


    # 최고가 표시
    ax_r.plot(
        high_idx2,                            # x 좌표
        high_price2 + y_offset2,                 # y 좌표
        marker="v",                          # ▼ 표시
        color=color_data_set[merged.iloc[0]["code_2"]],
        markersize = 5
    )

    if len(x)*0.5 < high_idx2:
        x_cord = high_idx2 - x_offset
        ha = "right"
    else:
        x_cord = high_idx2 + x_offset
        ha = "left"

    ax_r.text(
        x_cord,                              # x 좌표
        high_price2 + y_offset2,               # ▼와 같은 높이
        f"High Price {high_price2:,}",
        va = "center",
        ha = ha,
        fontsize = 8,
        color=color_data_set[merged.iloc[0]["code_2"]]
    )

    # 최저가 표시
    ax_r.plot(
        low_idx2,
        low_price2 - y_offset2,
        marker="^",                          # ▲ 표시
        color=color_data_set[merged.iloc[0]["code_2"]],
        markersize = 5
    )

    if low_idx2 < len(x)*0.5:
        x_cord = low_idx2 + x_offset
        ha = "left"
    else:
        x_cord = low_idx2 - x_offset
        ha = "right"


    ax_r.text(
        x_cord,                       # x 좌표
        low_price2 - y_offset2,           # ▲와 같은 높이
        f"Low Price {low_price2:,}",
        va = "center",
        ha = ha,
        fontsize = 8,
        color=color_data_set[merged.iloc[0]["code_2"]]
    )

    #-----------------------------------------------------
    # 현재가 표시
    #-----------------------------------------------------
    current_close1 = merged.iloc[-1]["close_1"]

    transform = blended_transform_factory(
        ax_l.transAxes,   # x는 축 좌표
        ax_l.transData    # y는 데이터 좌표
    )

    triangle_height = (price_max1 - price_min1) * 0.014
    triangle = Polygon(
        [
            [0.0002, current_close1],
            [-0.006, current_close1 + triangle_height],
            [-0.006, current_close1 - triangle_height]
        ],
        closed=True,
        facecolor=color_data_set[merged.iloc[0]["code_1"]],
        edgecolor="none",
        transform=transform,
        clip_on=False
    )

    ax_l.add_patch(triangle)

    ax_l.text(
        -0.0075,                 # 축의 오른쪽 바깥 0.75%
        current_close1,             # 실제 현재가
        f"{current_close1:,}",
        transform=transform,
        ha="right",
        va="center",
        fontsize=9,
        color="white",
        bbox=dict(
            boxstyle="round,pad=0.3",
            fc=color_data_set[merged.iloc[0]["code_1"]],
            ec="none"
        )
    )

    ax_l.axhline(
        y=current_close1,                            # 선을 그릴 Y축 높이
        color=color_data_set[merged.iloc[0]["code_1"]], # 지정된 색상
        linestyle="-",                              # 선 스타일 (':', '--', '-' 등)
        linewidth=0.8,                               # 선 굵기
        alpha=0.3,                                   # 투명도 (0.0 ~ 1.0)
        zorder=2                                     # 그리드/라인 간의 앞뒤 레이어 순서
    )

    ##############################################
    current_close2 = merged.iloc[-1]["close_2"]

    transform = blended_transform_factory(
        ax_r.transAxes,   # x는 축 좌표
        ax_r.transData    # y는 데이터 좌표
    )

    triangle_height = (price_max2 - price_min2) * 0.014
    triangle = Polygon(
        [
            [0.9998, current_close2],
            [1.006, current_close2 + triangle_height],
            [1.006, current_close2 - triangle_height]
        ],
        closed=True,
        facecolor=color_data_set[merged.iloc[0]["code_2"]],
        edgecolor="none",
        transform=transform,
        clip_on=False
    )

    ax_r.add_patch(triangle)

    ax_r.text(
        1.0075,                 # 축의 오른쪽 바깥 0.75%
        current_close2,             # 실제 현재가
        f"{current_close2:,}",
        transform=transform,
        ha="left",
        va="center",
        fontsize=9,
        color="white",
        bbox=dict(
            boxstyle="round,pad=0.3",
            fc=color_data_set[merged.iloc[0]["code_2"]],
            ec="none"
        )
    )

    # ---------------------------------
    # 화면 출력
    # ---------------------------------
    plt.show()

    # 저장
    plt.tight_layout()

    name1 = code_trans[merged.iloc[0]["code_1"]]
    name2 = code_trans[merged.iloc[0]["code_2"]]
    day = merged.iloc[0]["day_1"]

    title = f"data/image/price/{name1}_X_{name2}_{day}days_chart.png"

    plt.savefig(
        title,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
