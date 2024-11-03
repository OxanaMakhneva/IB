from PyQt5.QtCore import Qt, QRegExp, QDate, QModelIndex, QItemSelectionModel, QSortFilterProxyModel
from PyQt5.QtWidgets import QMenu, QFileDialog, QTableView, QDataWidgetMapper, QFormLayout, QMessageBox, QLineEdit, QSpinBox, QComboBox, QDateEdit
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlDatabase
from dataclasses import dataclass
from models.other_class_func import CustomDialog, NewItemDialog
import re
import app_logger
logger = app_logger.get_logger(__name__)


@dataclass
class DoubleRecord:
    table: str                  #Название таблицы, в которой происошло дубрирование
    column_name: str
    column_index: int           #Индекс столбца таблицы, в котором происошло дубрирование
    value: str           #Значение из-за которого произошло дублирование
    value_id: int        #Значение ключами для записи, из-за которой произошло дублирование

class ServiseModel():
    def __init__(self, table_name, map_list):
        self.table_name = table_name
        self.map_list = map_list

    def init_manipuls(self, data_model, table_name):
        if not data_model:
            self.manipul_model = self.data_model
        else:
            self.manipul_model = data_model
        if not table_name:
            self.manipul_table_name = self.table_name
        else:
            self.manipul_table_name = table_name

    #Геттер для считывания из map_list индекса столбца с prymary key для таблицы
    @property
    def prymary_idx(self):
        map_dict = {mapperfield.table: mapperfield.pkey_idx  for mapperfield in self.map_list}
        return map_dict.get(self.manipul_table_name)

    def index_by_name(self, column_name):
        map_dict = {mapperfield.column_map: mapperfield.index_map for mapperfield in self.map_list}
        return map_dict.get(column_name)

    def lable_by_name(self, column_name):
        map_dict = {mapperfield.column_map: mapperfield.lable for mapperfield in self.map_list}
        return map_dict.get(column_name)

    def check_double_record(self, record):
        shablon = r'(ОШИБКА:  повторяющееся значение ключа нарушает ограничение уникальности ")([A-Za-z]+)([_A-Za-z]+["][\s])(DETAIL:  Ключ "[(])([A-Za-z_]+)([)]=[(])(\d+)([)])'
        matched = re.search(shablon, self.manipul_model.lastError().text())
        if matched:
            #В сообщении об ошибке при создании новой записи регулярным выражением находим:
            #Находим системное название столбца, в котором возник конфликт уникального значения
            error_column = matched.group(5)
            #Находим человеческое название столбца (ярлык), в котором возник конфликт уникального значения
            error_column_lable = self.lable_by_name(error_column)
            #Находим название таблицы, в которой возник конфликт уникального значения
            error_table = matched.group(2)
            #Определяем индекс столбца, в котором возник конфликт уникального значения
            error_column_index = self.index_by_name(error_column)
            #Определяем значение, при вставке которого в БД возник конфликт уникального значения
            error_value = matched.group(7) #record.value(error_column_index)
            #Определяем значение prymary key записи, в которой в уникальном столбце значение совпало с тем,
            #которое мы пытались вставить, после чего возникла ошибка
            error_id = self.find_double_id(error_column_index, error_value)
            double_inf = DoubleRecord(error_table, error_column_lable, error_column_index, error_value, error_id)
            return double_inf
        else:
            logger.warning(self.manipul_model.lastError().text())
            return None

    def create_double_error(self, double_inf):
        if double_inf:
            Error_str = f''' Не удалось создать новую запись в таблице {double_inf.table}. {self.manipul_model.lastError().text()}.
                            Значение для столбца "{double_inf.column_name}"({double_inf.value}) новой строки совпало со значением в строке с индексом {double_inf.value_id}.
                            Изменить значение в столбце "{double_inf.column_name}" для обрабатывемой записи ?
                            "Yes" - "ДА", "No" - "Нет для одной записи", "Cancel" - "Прекратить процесс полностью"
                        '''
        else:
            Error_str = f''' Не удалось создать новую запись в таблице. Ошибка {self.manipul_model.lastError().text()}.
                             Определить название конфликтного столбца не удалось.
                        '''
        return Error_str

    #Метод, который ищет запись запись таблице, значение которой в заданном столбце совпадает с заданным значением
    def find_double_id(self, double_column_index, double_value):
        for row in range(0, self.manipul_model.rowCount()):
            if self.manipul_model.record(row).value(double_column_index) == double_value:
                return self.manipul_model.record(row).value(self.prymary_idx)

    def create_ask_dialog(self, Error_str):
        msgBox = QMessageBox()
        msgBox.setText("Конфликт уникальных значений")
        msgBox.setInformativeText(Error_str)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel);
        dialog = msgBox.exec()
        return dialog


    #Вспомогательный Подметод, который вставляет заданную запись в заданную модель и БД. Ошибки выводит на печать.
    def insert_rec(self, tab_window, record, data_model = None, table_name = None):
        logger.debug("Запущен метод init_manipuls для определения модели и имени таблицы, в которой планируются манипуляции")
        #print(record.value(1), record.value(2), record.value(3), record.value(4), record.value(5))
        self.init_manipuls(data_model, table_name)
        #Если запись не успешно добавлена в модель
        if not self.manipul_model.insertRecord(-1, record):
            Error_str = f'Не удалось записать новую строку в модель данных для таблицы {self.manipul_table_name}. Ошибка {self.manipul_model.lastError().text()}'
            logger.error(Error_str)
            _insert = 'FAIL'
        else:
            self.manipul_model.submitAll()
            if not self.manipul_model.submitAll():
                if "повторяющееся значение ключа нарушает ограничение уникальности" in self.manipul_model.lastError().text():
                    double_inf = self.check_double_record(record)
                    Error_str = self.create_double_error(double_inf)
                    dialog = self.create_ask_dialog(Error_str)
                    logger.info(Error_str + "Вызван метод removeRows для удаления из модели данных конфликтной записи")
                    #Удаляем из модели вставленную конфлитную запись
                    self.manipul_model.removeRows(self.manipul_model.rowCount() - 1, 1)
                    if dialog == QMessageBox.Yes and double_inf and double_inf.column_index != None:
                        #Запрашиваем у пользователя на что заменить конфликтное значение
                        ask_dialog = NewItemDialog(double_inf.column_name)
                        if ask_dialog.exec_():
                            new_value = ask_dialog.edit.text()
                            #Заменяем конфликтное значение в записи, которая должна быть добавлена в модель(БД)
                            record.setValue(double_inf.column_index, new_value)
                            #Заново запускаем метод, пердаем в него запись с новым значением
                            _insert = self.insert_rec(tab_window, record, self.manipul_model, table_name)
                            logger.debug("Вносим в БД значение, которые выбрано пользователем для замены конфликтного")
                        else:
                            _insert = 'DROP'
                            Inf_str = "Не введены данные для изменения дублирующих значений. Запись данных в БД не выполнена."
                            dialog = QMessageBox.warning(tab_window, "Конфликт уникальных значений", Inf_str)
                            logger.error(Inf_str)
                    elif dialog == QMessageBox.No:
                        _insert = 'PASS'
                        Inf_str = "Отказ от изменения дублирующих значений. Запись данных в БД не выполнена."
                        inf_dialog = QMessageBox.warning(tab_window, "Конфликт уникальных значений", Inf_str)
                        logger.error(Inf_str)
                    elif dialog == QMessageBox.Cancel:
                        _insert = "DROP"
                        return _insert
                elif "database is locked Unable to fetch row" in self.manipul_model.lastError().text():
                     return 'FAIL'
                else:
                    Error_str = f'Не удалось создать новую запись в таблице {self.manipul_table_name}. Ошибка {self.manipul_model.lastError().text()}'
                    logger.error(Error_str)
                    _insert = 'FAIL'
                    logger.error(Error_str)
            else:
                _insert = "DONE"
        return _insert

    #Вспомогательный Подметод, который удаляет строки с заданными номерами из заданной модели и БД. Ошибки выводит на печать.
    def remoove_rec(self, rows, data_model = None, table_name = None):
        self.init_manipuls(data_model, table_name)
        print("таблица, в которой проводяться манипуляции", self.manipul_table_name)
        if isinstance(rows, int):
            self.remoove_one_rec(rows)
            return True
        else:
            for row in rows:
                if not self.manipul_model.removeRows(row, 1):
                    logger.debug(f"Запись  (строка: {row + 1}) из БД таблицы {self.manipul_table_name} не может быть удалена.")
            if self.manipul_model.submitAll():
                return True
            else:
                Error_str = f'Записи  (строки: {rows}) из БД таблицы {self.manipul_table_name} не может быть удалена. Ошибка при вызове функции ".submitAll": {self.manipul_model.lastError().text()}'
                logger.error(Error_str)


    def remoove_one_rec(self, row):
        if self.manipul_model.removeRows(row, 1):
            if self.manipul_model.submitAll():
                logger.debug(f"Запись  (строка: {row + 1}) из БД таблицы {self.manipul_table_name} удалена.")
                return True
            else:
                Error_str = f'Запись  (строка: {row + 1}) из БД таблицы {self.manipul_table_name} не может быть удалена. Ошибка при вызове функции ".submitAll": {self.manipul_model.lastError().text()}'
                logger.error(Error_str)
        else:
            Error_str = f'Запись (строка: {row + 1}) из модели таблицы {self.manipul_table_name} не может быть удалена. Ошибка при вызове функции ".removeRows": {self.manipul_model.lastError().text()}'
            logger.error(Error_str)


    #Метод, который определяет id выделенной записи. Принимает на вход объекты класса TabModels, MainWinModel
    def find_choose_row(self, pr_name = 'ID'):
        #задаем номер колонки с пр. кей. по-умолчанию
        column_with_prkey = 999999
        if self.sel_model.currentIndex().isValid():
            #Определяем индекс столбца, в котором записан pr_key таблицы бд
            for col in range(self.data_model.columnCount()):
                if self.data_model.headerData(col, 1, Qt.DisplayRole) == pr_name:
                    column_with_prkey = col
                    break
            if  column_with_prkey == 999999:
                Error = f"Не удалось корректно определить номер столбца с pr. key. м модели данных для основной таблицы {self.table} "
                logger.error(Error)
                choose_id = None
                row = None
            else:
                #Определяем индекс выбранной строки
                row_index = self.proxy_model.mapToSource(self.sel_model.currentIndex())
                #Определяем индекс ячейки, в которой хранится ID объекта из выбранной строки
                source_index = row_index.siblingAtColumn(column_with_prkey)
                choose_id = int(self.data_model.data(source_index, Qt.DisplayRole))
                row = int(row_index.row())
        else:
            logger.warning("В таблице нет активной выбранной записи. Возвращены параметры, равные None")
            choose_id = None
            row = None
        return choose_id, row

    @staticmethod
    def update_all_windows(inital_window):
        #Обновляем модели данных основных окон
        logger.debug("Запускается метод обновления основных окон update_data_model")
        for win_main in inital_window.main_windows.values():
            win_main.update_data_model()
        #Обновляем модели данных таб-окон
        logger.debug("Запускается метод обновления таб-окон")
        for win_tab in inital_window.tab_windows.values():
            win_tab.update_tabs(tab_window = win_tab, status_act = True)


