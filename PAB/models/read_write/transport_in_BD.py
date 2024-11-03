import re
import datetime
from PyQt5.QtCore import QDate
import app_logger
logger = app_logger.get_logger(__name__)

#Класс, для управления экспортом данных
class TransportModel():
    def __init__(self, data_lable: "str", data_header: list, data_table: list):
        self.data_lable = data_lable
        self.data_header = data_header
        self.data_table = data_table
    def __str__(self):
        return f'Объект {self.__class__.__name__}, хранящий список названий столбцов(заголовок){self.data_header} и список со строками таблицы с данными {self.data_table} для вкладки {self.data_lable}'

    def __repr__(self):
        return (f'{self.__class__.__name__}'
        f' (data_lable: {self.data_lable}, data_header: {self.data_header}, data_table: {self.data_table}')

    #Подметод, который добавляет к данным одной таблицы (таблица, заголовок) столбец с № пп.
    def add_number_of_row(self):
        new_data_table = []
        #вставляем в строку с заголовками "№ пп."
        new_data_header = ["№ пп.",]
        new_data_header.extend(self.data_header)
        #вставляем в данные таблицы столбец с порядковыми номерами
        for idy, old_row in enumerate(self.data_table):
            new_row = [f'{idy + 1}']
            new_row.extend(old_row)
            #Пересобираем таблицу
            new_data_table.append(new_row)
        self.data_header = new_data_header
        self.data_table = new_data_table

    def del_enter_from_header(self):
        clean_header = [re.sub('\n', ' ', head) for head in self.data_header]
        self.data_header = clean_header

    def change_date_in_data_table(self, etalon_dict):
        change_data = []
        date_colums_list = [column_numb for column_numb in etalon_dict.keys() if etalon_dict[column_numb][1] != None]
        for record in self.data_table:
            change_record = []
            for position, item in enumerate(record):
                if position in date_colums_list:
                    #Если попало из БД(QT)
                    if isinstance(item, datetime.datetime):
                        new_item = item.strftime('%Y-%m-%d')
                        print("1", new_item, position)
                    #Если обрабатываем строковую переменную
                    elif isinstance(item, str):
                        new_item = (QDate.fromString(item, etalon_dict[position][1])).toString("yyyy-MM-dd")
                        if not new_item:
                            new_item = '1990-01-01'
                            Err_str = f'Неверно указан формат даты для столбца номер {position}, назначена дата по - умолчанию "1990-01-01"'
                            logger.error(Inf_str)
                    else:
                        Err_str = f'Не указана дата для столбца номер {position}, назначена дата по - умолчанию "1990-01-01"'
                        logger.error(Inf_str)
                        new_item = '1990-01-01'
                else:
                    new_item = item
                change_record.append(new_item)
            change_data.append(change_record)
        self.data_table = change_data

    #Выбирает из считанных данных те столбцы, названия которых сопоставлены с эталонными заголловками в
    #словаре etalon_dict {"номер столбца заголовка, который надо вставить в итоговые данные": "номер столбца заголовка, который надо искать в считанных данных"}
    def choose_data_with_header(self, etalon_dict):
        change_data = []
        index_list = [etalon_dict[position][0] for position in range(0, len(etalon_dict.keys()))]
        change_header = [self.data_header[position - 1] if position > 0 else None for position in index_list]
        for record in self.data_table:
            change_record = [record[position - 1] if position > 0 else None for position in index_list]
            change_data.append(change_record)
        self.data_table = change_data
        self.data_header = change_header
