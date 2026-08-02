from collector.data_reader.index_data_reader import index_data_reader
from collector.data_reader.price_data_reader import price_data_reader
from datetime import datetime, timedelta
from notion.client import notion
from notion.index_callout.updator import index_callout_updator

def index_callout_performer():
    #-----------------------------------------------------------------------------------
    # 1. 지표 데이터 일괄 수집 및 데이터 세팅
    #-----------------------------------------------------------------------------------
    today = datetime.now()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    targets = [
        {
            "call_out_ID": "0f76e5aee083829397d581bb68dc9a93",
            "title": "KOSPI",
            "df": index_data_reader(yesterday_str, today_str, "KOSPI"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Asset_Secretary_ver_3.0/main/data/image/market_index/KOSPI_chart.png"
        },
        {
            "call_out_ID": "a526e5aee0838342b3b081d421b59416",
            "title": "달러/원 환율",
            "df": price_data_reader(yesterday_str, today_str, "USD-KRW"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Asset_Secretary_ver_3.0/main/data/image/price/USD-KRW_chart.png"
        },
        {
            "call_out_ID": "3f66e5aee083824499ac014d399b9eb5",
            "title": "국제금 / 달러 인덱스",
            "df": price_data_reader(yesterday_str, today_str, "International_Gold"),
            "chart_url": "https://raw.githubusercontent.com/UnripeBanana/Asset_Secretary_ver_3.0/main/data/image/price/Dolar_Index_X_International_Gold_chart.png"
        }
    ]
    
    for target in targets:
        index_callout_updator(target)
