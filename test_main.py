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

from notion.index_callout.performer import index_callout_performer

#-------------------------------------------
# 작업 완료
#-------------------------------------------
#domestic_stock_chart_maker(domestic_stock_data_reader(90, "005930"), "삼성전자")
#domestic_stock_day_candle_chart_maker(domestic_stock_data_reader(90, "005930"), "삼성전자")

#index_chart_maker(index_data_reader(90, "KOSPI"))            
# 입력 가능한 항목 : "KOSPI", "KOSDAQ", "KOSPI_200", "NASDAQ", "S&P_500", "Dow_Jones", "VIX"

#index_day_candle_chart_maker(index_data_reader(90, "KOSPI"))         
# 입력 가능한 항목 : "KOSPI", "KOSDAQ", "KOSPI_200", "NASDAQ", "S&P_500", "Dow_Jones", "VIX"

#price_chart_maker(price_data_reader(90, "USD-KRW"))              
# 입력 가능한 항목 : "US2Y", "US10Y", "US30Y", "KR3Y", "KR10Y", "KR30Y", "USD-KRW", "Dolar_Index", "USD-JPY", "USD-EUR", 
#                   "KRX_Gold", "International_Gold", "Silver", "WTI_Crude_Oil", "Brent_Crude_Oil", "Natural_Gas", "Copper"

#standard_interest_chart_maker(standard_interest_data_reader(365*5, "Fed_Rate"))
# 입력 가능한 항목 : "Korea_Rate", "Fed_Rate"

#double_price_data_chart_maker(double_price_data_reader(365, "Dolar_Index", "USD-KRW"))
# 입력 가능한 항목 : "US2Y", "US10Y", "US30Y", "KR3Y", "KR10Y", "KR30Y", "USD-KRW", "Dolar_Index", "USD-JPY", "USD-EUR", 
#                   "KRX_Gold", "International_Gold", "Silver", "WTI_Crude_Oil", "Brent_Crude_Oil", "Natural_Gas", "Copper"

#index_callout_performer()


#-------------------------------------------
# 작업 중
#-------------------------------------------
