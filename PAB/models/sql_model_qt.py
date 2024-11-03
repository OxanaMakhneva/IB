from PyQt5 import QtSql, QtGui
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtCore import Qt, QDate, QSortFilterProxyModel
from PyQt5 import QtCore
import re

import app_logger
logger = app_logger.get_logger(__name__)

# Созданная на основе <QSqlQueryModel> модель представления данных,
#адаптированная под конкпетный sql-запрос.
#1. Изменяет отображение столбцов, в которых содержатся даты, преобразую дату из JulianDay в читабельную.
#2. Выделяет розовым дату окончаня аттестата, если до нее осталось менее 5 месяцев
#3. Выделяет красным дату окончаня аттестата, если она уже прошла
class CustomSqlModel(QtSql.QSqlQueryModel):
    def __init__(self, name_colums = (), nodisplay_colums = (), date_colums = {}):
        super().__init__()
        #Список столбцов, в которых хранятся даты с параметрами раскраски
        self.date_colums = date_colums
        #Список столбцов, в которых хранятся названия, которые надо поместить в кавычки
        self.name_colums = name_colums
        #Список столбцов, в которых хранятся названия, значения которых не надо показывать
        self.nodisplay_colums = nodisplay_colums

    #Метод, который определяет цвет закраски фона в зависимости от того на каком отрезке
    #находиться дата, записанная в results. Границы отрезка в виде 'less_then_element', 'more_then_element' и
    #соответсвующие цвета 'color_less', 'color_between', 'color_more' задаются в именованном кортеже,
    #закрепленном за прокси-моделью <self.date_colums>
    def colculate_color(self, results, index_colum):
        try:
            result = QDate.fromString(results, "yyyy-MM-dd")
        except:
            logger.debug(f"Не удалось перевести ячейку с датой {results} из столбца {index_colum} в QDate")
            return None
        date_colum = self.date_colums[index_colum]
        if date_colum.more_then_element != None and date_colum.less_then_element != None:
            Error_str = f' Дата, закрепленная в переменной more_then_element должна быть больше, чем дата из переменной less_then_element. Исправьте файл конфигурации, строка словаря DATE_COLUMS с ключом {index_colum}: ({self.date_colums[index_colum]})'
            assert date_colum.more_then_element > date_colum.less_then_element, (Error_str)
            if result < date_colum.more_then_element and result > date_colum.less_then_element:
                color = date_colum.color_between
            elif result < date_colum.less_then_element or result == date_colum.less_then_element:
                color = date_colum.color_less
            elif result > date_colum.more_then_element or result == date_colum.more_then_element:
                color = date_colum.color_more
            else:
                return None
        elif date_colum.more_then_element != None and date_colum.less_then_element == None:
            Error_str = f' Дата, закрепленная в переменной more_then_element должна быть меньше текущего числа. Исправьте файл конфигурации, строка словаря DATE_COLUMS с ключом {index_colum}: ({self.date_colums[index_colum]})'
            assert date_colum.more_then_element < QDate.currentDate(), (Error_str)
            if result < date_colum.more_then_element or result == date_colum.more_then_element:
                color = date_colum.color_more
            else:
                return None
        elif date_colum.more_then_element == None and date_colum.less_then_element != None:
            if result > date_colum.less_then_element or result == date_colum.less_then_element:
                color = date_colum.color_less
            else:
                return None
        else:
            return None
        return color
#Адаптированный под кокретный формат данных метод обработки данных, которые генерирутся
#в результате SQL-запроса <results = self.query()> в виде объекта типа <QSqlQuery>
#1. Каждый раз когда от виджета отображения типа <QTableView()> в объект оступает запрос
#на отображение данных <role == Qt.DisplayRole> для конкретных строки <index.column()>
#и столбца <index.row()> метод перемещается на строку результатов query-запроса
#<results.seek(index.row())>, соответствующую запрошенному индексу <index.row()> и
#1.1. если столбцы находятся в списке столбцов с датами <self.date_colums.keys()>,
#меняет формат отображения
#1.2 если в столбце, для которого не надо печатать значения <self.nodisplay_colums>, пасует
#для остальных столбцов - вовращает значение.
#2. Каждый раз когда в объект оступает запрос на стилизацию данных <role == Qt.BackgroundRole>
#если необходимо отобразить данные для столбцов с датами <self.date_colums.keys()>,
#с помощью вспомогательного метода определяет  цвет фона и возвращает его
#3 Каждый раз когда от виджета отображения типа <QTableView()> в объект оступает запрос
#на стилизацию данных <role == Qt.DecorationRole> если необходимо отобразить данные
#из <self.nodisplay_colums> возвращает ярлыки в зависимости от значения данных
    def data(self, index, role):
        #results = query()
        results = super().data(index, role)
        #return results
        if role == Qt.DisplayRole:
            if (results !='' and index.column() in self.date_colums.keys()):
                try:
                    value_d = QDate.fromString(results, "yyyy-MM-dd")
                    value = value_d.toString("dd.MM.yyyy")
                except:
                    value = results
                return value
            if  index.column() in self.nodisplay_colums:
                pass
            else:
                return results
        elif role == Qt.BackgroundRole:
            results = self.query().value(index.column())
            if index.column() in self.date_colums.keys() and results !='':
                color = self.colculate_color(results, index.column())
                if color != None:
                    return QtGui.QColor(color)
                else:
                    pass
        elif (role == Qt.DecorationRole and index.column() in self.nodisplay_colums):
            res = self.query().value(index.column())
            if res == 1:
                return QtGui.QIcon("tick.png")
            elif res == 2:
                return QtGui.QIcon("cross.png")
            elif res == 3:
                return QtGui.QIcon("balloon.png")
            else:
                return res

class CustomProxyModel(QSortFilterProxyModel):
    def __init__(self, view_model, texts = {}, dates = {}, **kwargs):
        super().__init__(view_model)
        #Словарь с введенными в полях фильтрации (edit, combobox) значениями (из метода start_filter)
        self.texts = texts
        #Словарь  с введенными в полях фильтрации (qdateedit) значениями из метода (start_filter, set_filter_dates)
        self.dates = dates

    #Переписанный метод прокси-модели. Возвращает True если для всех ячеек в стороке из модели данных <source_row>
    #c индексами <source_index> содержаться данные, соответсвующие введенным в поля фильтрации значениям
    #Данный метод вызывается методами прокси- модели и входные данные передаются в него автоматически
    def filterAcceptsRow(self, source_row: int, source_index):
        #Определяем список столбцов, для которых определены фильтры по датам
        dates_for_filtr = [key[0] for key in self.dates.keys()][::2]
        #Определяем индексы элементов, где храняться строковые значения
        text_proxy_indexes = {idx: self.sourceModel().index(source_row, idx, source_index) for idx in range(0, self.sourceModel().columnCount()) if idx not in self.sourceModel().date_colums.keys()}
        #Определяем индексы элементов в proxy-модели, где храняться даты, для столбцов которых есть фильтры по датам
        date_proxy_indexes = {idx: self.sourceModel().index(source_row, idx, source_index) for idx in dates_for_filtr}
        #Формируем словари из значений с отобранными индексами, где ключи - номера столбцов
        text_proxy_strings = {idx: self.sourceModel().data(text_proxy_indexes[idx], Qt.DisplayRole) for idx in text_proxy_indexes.keys()}
        date_proxy_strings = {idx: QDate.fromString(self.sourceModel().data(date_proxy_indexes[idx], Qt.DisplayRole), "dd.MM.yyyy") for idx in date_proxy_indexes.keys() if self.sourceModel().data(date_proxy_indexes[idx], Qt.DisplayRole) != ""}
        #Проверяем выполнение каждого условия.
        #Проверяем, содержиться ли в данных ячейки введеннаяпользрвателем в поле фильтрации строка. Если нет - возвращается None
        text_checks = [re.search(self.texts[idx], text_proxy_strings[idx]) for idx in self.texts.keys()]
        #Если фильтрация по датам включена (словарь с датами не пустой)
        if self.dates != {}:
            #Если дата находиться вне заданного пользователем диапазона возвращается False
            date_checks = [False for key, str in date_proxy_strings.items() if (str > self.dates.get((key, 1)) or str < self.dates.get((key, 0)))]
        else:
            date_checks = []
        #Если все условия для строки выполняются, возвращаем True
        if None not in text_checks and False not in date_checks:
            return True
        else:
            return False

    #Метод, который создает и передает в прокси-модель словарь с введенными
    #в полях фильтрации (edit, combobox) значениями
    def set_texts(self, edits_params, combos_params):
        edit_dict = {edit.table_column: edit.dict["obj"].text() for edit in edits_params}
        combo_dict = {combo.table_column: combo.dict["obj"].currentText() for combo in combos_params}
        texts = {**edit_dict, **combo_dict}
        self.texts = texts

    #Метод, который создает и передает в прокси-модель словарь с введенными
    #в полях фильтрации (qdateedit) значениями
    def set_dates(self, dates_params):
        date_dict = {(date.table_column, date.border): date.dict["obj"].date() for date in dates_params}
        self.dates = date_dict


    #Конец метода data для класса CustomSqlModel
#Конец описания класса CustomSqlModel
