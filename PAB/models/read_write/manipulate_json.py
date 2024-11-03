import json
import os
from models.read_write.transport_in_BD import TransportModel

#Метод, который сохраняет наполнение сервисных таблиц в конфигурационном файле
def create_myjson(sets, file_name):
    set_data = {}
    table_data = {}
    for set in sets:
        for row_number, row in enumerate(set.data_table):
            record = {item_head: row[item_position] for item_position, item_head in enumerate(set.data_header)}
            table_data = {**table_data, **{row_number: record}}
        set_data = {**set_data, **{set.data_lable: table_data}}
    #Подготавливаем словарь для записи в конфиг
    write_json((set_data), file_name)


#Метод, который сохраняет наполнение сервисных таблиц в конфигурационном файле
def read_myjson(file_name, sheet = None, *args):
    read_data = read_json(file_name)
    if not read_data:
        return None
    if sheet:
        data_set = read_data[sheet]
        data_table = []
        firs_key = list(data_set.keys())[0]
        data_headers = list(data_set[firs_key].keys())
        for row_data in data_set.values():
            records = [row_data.get(header, None) for header in data_headers]
            data_table.append(records)
        return TransportModel(sheet, data_headers, data_table)
    else:
        sets = []
        for data_label, data_set in read_data.items():
            data_table = []
            data_headers = [row_data for row_data in data_set['0']]
            for row_data in data_set.values():
                records = [row_data.get(header, None) for header in data_headers]
                data_table.append(records)
            set = TransportModel(data_label, data_headers, data_table)
            sets.append(set)
        return sets


#Метод, который сохраняет наполнение сервисных таблиц в конфигурационном файле
def read_myjson_sheet(file_name, *args):
    read_data = read_json(file_name)
    if read_data:
        sheets = [data_label for data_label in read_data.keys()]
        return sheets
    else:
        return None

def read_myjson_head(file_name, sheet, *args):
    read_data = read_json(file_name)
    if read_data:
        try:
            firs_key = list(read_data[sheet].keys())[0]
            data_headers = list(read_data[sheet][firs_key].keys())
        except:
            data_headers = None


        return data_headers
    else:
        return None

def write_json(export_data, file_name):
    data_json = json.dumps(export_data)
    with open(file_name, 'w') as outfile:
        json.dump(data_json, outfile)

def read_json(file_name):
    if os.path.isfile(file_name):
        #Открываем ранее записанный конфиг и считываем из него данные. Преобразуем в словарь
        with open(file_name) as json_file:
            data_json = json.load(json_file)
            read_data = json.loads(data_json)
        return read_data
