from collector.data_reader.price_data_reader import price_data_reader

def double_price_data_reader(day, code_1, code_2):
    data_1 = price_data_reader(day, code_1)
    data_2 = price_data_reader(day, code_2)
    return data_1, data_2
