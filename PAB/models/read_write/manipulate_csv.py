import csv
import os
from models.read_write.transport_in_BD import TransportModel

#Метод, который сохраняет наполнение сервисных таблиц в конфигурационном файле
def create_mycsv(sets, file_name):
    for idx, set in enumerate(sets):
        header = set.data_header
        table_data = []
        for row_number, row in enumerate(set.data_table):
            #print(row_number)
            record = {item_head: str(row[item_position]) for item_position, item_head in enumerate(set.data_header)}
            table_data.append(record)
        #Записываем файл для первой вкладки
        write_csv(header, table_data, file_name)

def write_csv(export_header, export_data, file_name):
    #Для тго, чтобы не возникало проблем с кодированием добавляем при открытии файла encoding="utf-8"
    with open(file_name, 'w', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames = export_header)
        writer.writeheader()
        for idx, row in enumerate(export_data):
            try:
                writer.writerow(row)
            except:
                print(row)


#МЕТОД НЕ ПРОВЕРЕН
def read_csv(file_name):
    if os.path.isfile(file_name):
        #Открываем ранее записанный конфиг и считываем из него данные. Преобразуем в словарь
        with open(file_name, encoding="utf-8") as csv_file:
            #data_json = json.load(json_file)
            #read_data = json.loads(data_json)
            reader = csv.reader(csv_file)
            for row in reader:
                print(row)
        return reader



