from collector.data_reader.domestic_stock_data_reader import domestic_stock_data_reader
from collector.data_reader.index_data_reader import index_data_reader
from collector.data_reader.price_data_reader import price_data_reader
from collector.data_reader.standard_interest_data_reader import standard_interest_data_reader
from collector.data_reader.double_price_data_reader import double_price_data_reader

from collector.chart_maker.domestic_stock_chart_maker import domestic_stock_chart_maker
from collector.chart_maker.domestic_stock_day_candle_chart_maker import domestic_stock_day_candle_chart_maker
from collector.chart_maker.index_chart_maker import index_chart_maker
from collector.chart_maker.index_day_candle_chart_maker import index_day_candle_chart_maker
from collector.chart_maker.price_chart_maker import price_chart_maker
from collector.chart_maker.standard_interest_chart_maker import standard_interest_chart_maker
from collector.chart_maker.double_price_data_chart_maker import double_price_data_chart_maker

from notion.get_all_pages import get_all_pages
from notion.config import NOTION_DOMESTIC_STOCK_INFO_DB_ID

for day in [90, 365, 365*3, 365*5, 365*10]:
    for page in get_all_pages(NOTION_DOMESTIC_STOCK_INFO_DB_ID):
    
        ticker_data = page["properties"]["티커"]["rich_text"]
    
        if not ticker_data:
            continue
    
        ticker = ticker_data[0]["plain_text"]
    
        name_data = page["properties"]["종목"]["title"]
        name = name_data[0]["text"]["content"]
    
        domestic_stock_chart_maker(domestic_stock_data_reader(day, ticker), name)
        domestic_stock_day_candle_chart_maker(domestic_stock_data_reader(day, ticker), name)
    
    for index in ["KOSPI", "KOSDAQ", "KOSPI_200", "NASDAQ", "S&P_500", "Dow_Jones", "VIX"]:
        index_chart_maker(index_data_reader(day, index))
        index_day_candle_chart_maker(index_data_reader(day, index))

    for price_1 in ["US2Y", "US10Y", "US30Y", "KR3Y", "KR10Y", "KR30Y", "USD-KRW", "Dolar_Index", "USD-JPY", "USD-EUR", "KRX_Gold", "International_Gold", "Silver", "WTI_Crude_Oil", "Brent_Crude_Oil", "Natural_Gas", "Copper"]:
        price_chart_maker(price_data_reader(day, price_1))
        for price_2 in ["US2Y", "US10Y", "US30Y", "KR3Y", "KR10Y", "KR30Y", "USD-KRW", "Dolar_Index", "USD-JPY", "USD-EUR", "KRX_Gold", "International_Gold", "Silver", "WTI_Crude_Oil", "Brent_Crude_Oil", "Natural_Gas", "Copper"]:
            if price_1 == price_2: continue

            double_price_data_chart_maker(double_price_data_reader(day, price_1, price_2))

    for standard_interest in ["Korea_Rate", "Fed_Rate"]:
        standard_interest_chart_maker(standard_interest_data_reader(day, standard_interest))
