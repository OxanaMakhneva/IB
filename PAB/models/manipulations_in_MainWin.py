# Модуль, который будет создавать окно со списком ВП
import sys
import re
import importlib
import os
from datetime import datetime
from dataclasses import dataclass

from PyQt5.QtCore import QItemSelectionModel, QRegExp, QSize, Qt, QDate, QVariant, QObject, QModelIndex, QSortFilterProxyModel
from PyQt5 import QtCore, QtWidgets, QtSql, QtGui
from PyQt5.QtWidgets import QProgressBar, QFileDialog, QMessageBox, QHeaderView, QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QToolBar, QAction, QStatusBar, QLabel, QCheckBox, QDialog, QDialogButtonBox, QMessageBox,  QMenu, QStyle,  QTableView, QLineEdit, QHBoxLayout, QFormLayout, QSpinBox, QComboBox, QDoubleSpinBox, QDataWidgetMapper, QComboBox, QDateEdit, QGridLayout, QListView, QTabWidget
from PyQt5.QtGui import QWindow, QColor, QPalette, QIcon, QKeySequence
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate, QSqlQuery, QSqlQueryModel, QSqlRecord

from models import read_write, table_model_qt, sql_model_qt, manipulations_in_MainWin
from models.table_model_qt import CustomTableView, CustomQSortFilterProxyModel
from models.sql_model_qt import CustomSqlModel, CustomProxyModel
from models.manipulations_in_TabWin import TabModels
from models.read_write import export_in_BD, import_in_BD, transport_in_BD, manipulate_json
from models.read_write.export_in_BD import ExportModel
from models.read_write.import_in_BD import ImportModel, DialogImport, DialogImportHead, DialogImportSheetName,  DialogImportConfigList, DialogImportConfigList2
from models.read_write.transport_in_BD import TransportModel
from models.read_write.manipulate_json import read_json
from models.manipulations_in_DB import ServiseModel
from models.manipul_string_relations import siblins_soft_for_one_rec
from models.other_class_func import DialogAskCorr
import app_logger
logger = app_logger.get_logger(__name__)

#Класс для хранения данных о всех столбцах таблицы, в которых есть даты. Если разукрашивать не надо, последние три параметра - не заполняются
@dataclass(frozen = True)
class DateColums:
    less_then_element: QDate = None
    more_then_element: QDate = None
    color_less: str = None
    color_between: str = None
    color_more: str = None

#Класс для хранения данных для ярлыков поля фильтрации:
@dataclass(frozen = True)
class Lables:
    text: str               #Текст
    font_size: int          #Размер шрифта
    row: int                #Номер строки в сетке для размещения ярлка
    col: int                #Номер столбца в сетке для размещения ярлка
    nrow: int               #Количество строк для размещения ярлка
    ncol: int               #Количество столбцов для размещения ярлка

#Класс для хранения данных для поля типа Edit из блока фильтрации
@dataclass(frozen = True)
class Edits:
    table_column: int       #Индекс колонки, к которой привязано поле фильтрации
    def_text: int           #Подстановочный текст
    row: int                #Номер строки в сетке для размещения поля
    col: int                #Номер столбца в сетке для размещения поля
    nrow: int               #Количество строк для размещения поля
    ncol: int               #Количество столбцов для размещения поля
    dict: dict              #Словарь для хранения объекта поля

#Класс для хранения данных для выпадающих списков типа Combos из блока фильтрации
@dataclass(frozen = True)
class Combos:
    table_column: int       #Индекс колонки, к которой привязано поле фильтрации
    def_text: int           #Подстановочный текст
    table_for_combo: str         #Название таблицы, из которой надо считать список для комбобокса
    column_for_combo: int        #Индекс столбца, из которого надо считать список для комбобокса
    def_list: list          #Список значений для выпадающего списка, применяется если не удалось считать список из БД
    row: int                #Номер строки в сетке для размещения поля
    col: int                #Номер столбца в сетке для размещения поля
    nrow: int               #Количество строк для размещения поля
    ncol: int               #Количество столбцов для размещения поля
    dict: dict              #Словарь для хранения объекта поля

#Класс для хранения данных для выпадающих списков типа Dates из блока фильтрации
@dataclass(frozen = True)
class Dates:
    table_column: int       #Индекс колонки, к которой привязано поле фильтрации
    border: int             #0 - флаг левой границы даты, 1 - флаг правой границы даты,
    offset: list            #Смещение относительно текущейдаты вмесяцах
    row: int                #Номер строки в сетке для размещения поля
    col: int                #Номер столбца в сетке для размещения поля
    nrow: int               #Количество строк для размещения поля
    ncol: int               #Количество столбцов для размещения поля
    dict: dict              #Словарь для хранения объекта поля

class MainWinModel(ServiseModel):
    def __init__(self, mainmodels: dict, window, db, table_name: str, headers: list, prymarykey: str, prymaryidx: int):
        self.__mainmodels = mainmodels
        self.window = window
        self.db = db
        self.table_name = table_name
        self.headers = headers
        self.prymarykey = prymarykey
        self.prymaryidx = prymaryidx
        self.map_list = self.window.map_list
        logger.debug(f"Создана модель манипуляции для основного окна первичной таблицы {self.table_name}")

    @property
    def data_model(self):
        return self.__mainmodels["data"]

    @data_model.setter
    def data_model(self, input_model):
        if type(input_model) == CustomSqlModel:
            self.__mainmodels["data"] = input_model
        else:
            raise TypeError
    @property
    def sel_model(self):
        return self.__mainmodels["sel"]

    @sel_model.setter
    def sel_model(self, input_model):
        if type(input_model) == QItemSelectionModel:
            self.__mainmodels["sel"] = input_model
        else:
            raise TypeError
    @property
    def proxy_model(self):
        return self.__mainmodels["proxy"]

    @proxy_model.setter
    def proxy_model(self, input_model):
        if type(input_model) == CustomProxyModel:
            self.__mainmodels["proxy"] = input_model
        else:
            raise TypeError

    def generate_args(func):
        def wraper(*args, **kwargs):
            #window = args[1]
            #print(args)
            window = kwargs['window']
            self = window.current_main
            arg_dict = {}
            kwargs = {**arg_dict, **kwargs}
            change_func = func(self, **kwargs)
            return change_func
        return wraper

    #Метод, который определяет id для новой записи (на 1 больше максимального из существующих)
    def generate_new_id(self, data_model: QSqlRelationalTableModel, id_index) -> int:
        #id_index = self.prymaryidx
        if data_model.query().first():
            ids = [data_model.query().value(id_index)]
            while data_model.query().next():
                ids.append(data_model.query().value(id_index))
            new_id = max(ids) + 1
        else:
            new_id = 1
        logger.info(f"Сгенерирован pr.key для новой записи в таблице {data_model.tableName()}, равный {new_id}")
        return new_id


    #Метод, который добавдяет новую заись в БД и возвращает ее id
    def new_rec_id(self, window, **kwargs) -> int:
        #Создаем сервисную модель со всеми записями, которые содержаться в БД для активной таблицы
        servise_model = self.create_servise_model()
        #Генерируем индекс (значение prymary key для новой записи)
        new_id = self.generate_new_id(servise_model, self.prymaryidx)
        servise_model.query().finish()
        logger.info(f"Создана и добавлена в таблицу БД ({self.table_name}) новая запись с pr.key, равным {new_id}")
        return new_id

    #Метод, который удаляет выбранную запись из БД
    @generate_args
    def del_rec(self, window, **kwargs):
        final_delete = True
        """
        Чтобы удалить запись из таблицы главного окна, надо:
        - понять, какая таблица для него является основной
        - понять, связан выбранный ключ из основной таблицы с записями из других таблиц
          способами многие-ко-многим или многие к одному нашему ключу
        - если есть связи многие-ко-многим, то предварительно нужно удалить записи из общей таблицы
        - если есть связи многие к одному нашему ключу, то нужно обнулить внешние ключи в связанных таблицах
        - после всех манипуляций можно удалить запись.
        """
        #Считываем имя основной таблицы
        main_table = self.table_name
        #Считываем основной ключ удаляемой записи в основной таблице
        choose_id, row = self.find_choose_row()
        #Создаем таб-окно(карточку) для удаляемой записи
        if choose_id:
            #Активируем основное таб-окно
            tab_window = window.open_tab_window(self.window.inital_window, window = self.window, choose_id=choose_id, is_new_record=False)
            #Отрабатываем связи многие-ко-многим
            # Считываем модель общей таблицы и ее название
            for prom_table, prom_model in tab_window.prom_dict.items():
                final_delete = True
                #Считываем данные из бд в модель
                prom_model.select()
                #Составляем список записей из общей таблицы, в которых есть ссылка на главный ключ нашей основной таблицы
                rows_for_del = [row for row in range(0, prom_model.rowCount()) if prom_model.record(row).value(0) == choose_id]
                #Удаляем связанные записи из общей таблицы
                #Вызываем метод удаления записей из под вкладки-карточки, созданной для основной таблицы.
                #Но так как удалять записи мы будем из общей таблицы передаем в метод модель общей таблицы и ее название
                delete = tab_window.current_tab.remoove_rec(rows_for_del, prom_model, prom_table)
                if delete:
                    print(f"Записи из строк {rows_for_del} общей таблицы {prom_table} успешно удалены")
                else:
                    print(f"Запись из строки {rows_for_del} общей таблицы {prom_table} не удалены")
                    final_delete = False

            #Отрабатываем связи одна-ко-многим (когда ссылка на удаляему запись есть в други таблица)
            print(tab_window.link_dict)
            #Для каждой таблицы, которая может быть связана с основной по внешнему ключу
            for link_table, link_keys in tab_window.link_dict.items():
                link_model = self.create_servise_model(link_table, link_keys[0])
                rows_for_del = [row for row in range(0, link_model.rowCount()) if link_model.record(row).value(link_keys[1]) == choose_id]
                delete = tab_window.current_tab.remoove_rec(rows_for_del, link_model, link_table)
                if delete:
                    print(f"Записи из строк {rows_for_del} связанной таблицы {link_table} успешно удалены")
                else:
                    print(f"Запись из строки {rows_for_del} связанной таблицы {link_table} не удалены")
                    final_delete = False
            #Если все связанные данные из общей таблицы удалены можно удалить запись из основной таблицы
            if final_delete:
                #ПОКА НЕ РАБОТАЕТ
                main_model = self.create_servise_model(main_table, 'id', choose_id)
                delete = self.remoove_rec(main_model, main_table, [0])
                print("результат удаления записи", delete)

            return final_delete

            """
            Чтобы удалить запись из таблицы главного окна, надо:
            - понять, какая таблица для него является основной
            - понять, связан выбранный ключ из основной таблицы с записями из других таблиц 
              способами многие-ко-многим или многие к одному нашему ключу
            - если есть связи многие-ко-многим, то предварительно нужно удалить записи из общей таблицы
            - если есть связи многие к одному нашему ключу, то нужно обнулить внешние ключи в связанных таблицах
            - после всех манипуляций можно удалить запись.
            """
            print(type(tab_window), tab_window.current_tab.rel.type)
            #print(tab_window.rel.type, tab_window.entity_id)
            """
            if tab_window.rel.type == "ManyTab-ManyBag":
                # Считываем модель общей таблицы
                prom_model = tab_window.prom_dict[tab_window.rel.table_prom_tab]
                logger.debug("Тип связи для активной таблицы - {ManyTab-ManyBag}, для удаления записи вызван метод del_MT_MB")
                rez = tab_window.del_MT_MB(tab_window.db, tab_window.entity_id, prom_model, row, id1)
            else:  # rel.type == "ManyTab-OneBag":
                logger.debug("Тип связи для активной таблицы - {ManyTab-OneBag}, для удаления записи вызван метод remoove_rec")
                rez = tab_window.remoove_rec(row)
            if rez:
                Log_str = f'Запись (строка: {row + 1}, ID: {id1}) из таблицы {tab_window.rel.table_tab} успешно удалена'
                logger.info(Log_str)
                TabModels.update_all_windows(tab_window.inital_window)
                # Применяем фильтр с учетом новой записи
                id_list = tab_window.filter_id
                id_list.remove(id1)
                tab_window.update_filter(tab_window.db, tab_window.entity_id)
            else:
                Log_str = f'Запись (строка: {row + 1}, ID: {id1}) из таблицы {tab_window.rel.table_tab} не удалена. Проблемы с методами del_MT_MB и(или) remoove_rec'
                logger.info(Log_str)

            
            if tab_window.remoove_rec(0, servise_model):
                Log_str = f'Запись (строка: {row + 1}, ID: {choose_id}) из таблицы {tab_window.table_name} успешно удалена'
                logger.info(Log_str)
                MainWinModel.update_all_windows(window.inital_window)
            servise_model.query().finish()
        else:
            Inf_str = f'Перед удалением нажмите в таблице на интересующий объект'
            dialog = QMessageBox.information(window, "Уведомление", Inf_str)
        """

    #Метод создает модель, в которой только одна строка (с id = choose_id) если choose_id задан, иначе - все строки
    def create_servise_model(self, table_name = "", prymarykey = "", choose_id: int = None) -> QSqlRelationalTableModel:
        if not table_name and not prymarykey:
            table_name = self.table_name
            prymarykey = self.prymarykey
        servise_model = QSqlRelationalTableModel(db = self.db)
        servise_model.setEditStrategy(2)
        servise_model.setTable(table_name)
        if choose_id:
            filtr_str = f'{prymarykey} = {choose_id}'
            servise_model.setFilter(filtr_str)
        try:
            servise_model.select()
            logger.debug(f"Создана сервисная модель данных для таблицы {table_name}")
        except:
            logger.warning(f"Не удалось создать валидную сервисная модель данных для таблицы {table_name}")
        return servise_model

    #Метод, который считывает данные из первичной таблицы основного окна и записывает в модель для экспорта
    def read_data_for_export(self) -> list:
        if self.data_model.query().first():
            data_header = list(self.headers)
            data_table =  []
            rec = [self.data_model.query().value(idx) for idx in range(0, self.data_model.columnCount())]
            data_table.append(rec)
            while self.data_model.query().next():
                rec =  [self.data_model.query().value(idx) for idx in range(0, self.data_model.columnCount())]
                data_table.append(rec)
            export_sets = [TransportModel(self.table_name, data_header, data_table),]
            logger.debug(f"Создан список объектов типа TransportModel с упакованными данными таблицы {self.table_name} для их дальнейшего экспорта")
            return export_sets

    #Метод, который запускает экспорт данных из таблицы основного окна в файл, определяемый значением  where
    @generate_args
    def start_export(self, window, where: str, **kwargs):
        export_sets = self.read_data_for_export()
        if not export_sets:
            pass
        else:
            _ = [export_set.add_number_of_row() for export_set in export_sets]
            #Модель экспорта
            file_name = f'report-{self.table_name} - {QDate.currentDate().toString("dd.MM.yyyy")}'
            export_model = ExportModel(window, export_sets, where, file_name, "report_objs")
            #Согласовываем полный путь для файла с пользователем
            Inf_str = f'Задайте имя файла для сохранения данных'
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            if export_model.choose_file_name():
                #Активируем экспорт
                logger.debug(f"Создан объект модели экспорта (ExportModel) для реализации экспорта данных из таблицы {self.table_name}. Активирован экспорт")
                export_model.export()
            else:
                pass

    #Метод, который активирует считывание данных из файла и их запись в БД.
    @generate_args
    def start_import(self, window, where: str, what: str, **kwargs):
        #Проверяем, есть у таблицы метка импорта с корреляцией
        corr_import = [map_field.corr_import for map_field in self.window.map_list]
        if "corr_edit" in corr_import:
            #Импорт с корреляцией
            self.start_import_with_corr()
        else:
            #Импорт без корреляции
            self.start_import_no_corr(window, where, what)

    #Метод, который активирует импорт без корреляции.
    #@generate_args
    def start_import_no_corr(self, window, where: str, what: str, **kwargs):
        FILE_command = {"add": self.add_import, "update": self.update_import}
        #Подготавливаем модель для импорта
        import_model = self.prepare_import_model(where, what)
        if import_model == None or import_model.stop == True:
            pass
        else:
            #Считываем данные из файла
            import_data = import_model.read_data_for_import()
            if import_data == None:
                pass
            else:
                #Запускаем данные в БД (дописываем, обновляем или подъменяем)
                if FILE_command[what](import_data, import_model):
                    import_model.save(self.window, self.table_name)
                    Inf_str = f"Процесс обновления таблицы {self.table_name} с параметром {what} завершен."
                    logger.info(Inf_str)
                    dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)

    #Метод, который сопоставляет столбцы БД и импортируемого файла, формирует и заполняет модель импорта
    def prepare_import_model(self, where: str, what: str) -> ImportModel:
        #Создаем пустую модель импорта
        import_model = ImportModel(self.window, where, f'report-{self.table_name}', "report_objs")
        Inf_str = "Внимание! Убедитесь, что открыто окно с таблицей, в которую планируется импорт. Выбирите файл, из которого необходимо считать импортируемые данные "
        dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
        if not import_model.choose_file_name():
            Inf_str = "Файл с данными не выбран. Импорт отстановлен"
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.warning(Inf_str)
            import_model.stop = True
        else:
            #Выбираем вкладку, из которой планируется импорта
            logger.debug("Запущен метод choose_sheet для определения вкладки источника импортируемых данных")
            import_model.sheet = self.choose_sheet(import_model)
            #Коггда вкладка выбрана. Выбираем строку, в которой храняться заголовки таблицы
            logger.debug("Запущен метод choose_first_row для считывания строки - заголовок из файла - источника импортируемых данных")
            import_model.first_row = self.choose_first_row(where)
            #Считываем заголовки столбцов из импортируемого файла
            logger.debug("Запущен метод read_head для считывания названий столбцоы в файле-источнике")
            import_head = import_model.read_head()
            if import_head == None:
                import_model.stop = True
                Inf_str = "Строка с названиями столбцов выбрана неверно. Не удалось считать данные для импорта. Импорт остановлен"
                dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                logger.warning(Inf_str)
            else:
                choose_head = ["Нет в файле"] + import_head
                #Считываем параметры таблицы БД
                db_param_turpl = self.read_bd_params()
                logger.debug("Методом read_bd_params считаны параметры модели данных первичной таблицы, в которую импортируются данные")
                #Записываем все параметры в модель
                (import_model.bd_head, import_model.combo_col, import_model.calc_col, import_model.prymary_col) = db_param_turpl
                #Опрашиваем пользователяи формируем списки разного рода столбцов и соответсвия между нимми
                import_params = self.prepare_import_params(import_model, choose_head, what)
                if not import_params:
                    Inf_str = "Не удалось подготовить параметры импорта. Импорт отстановлен"
                    dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                    import_model.stop = True
                    logger.warning(Inf_str)
                else:
                    #Записываем все параметры в модель
                    ((import_model.uniq_db_col, import_model.uniq_file_col), import_model.not_import_col, import_model.etalon_dict) = import_params
                    logger.debug("Методом prepare_import_params считаны подготовлены параметры импорта ")
        return import_model

    #Метод, который считывает данные о таблице БД, которую планируется обновлять:
    def read_bd_params(self) -> tuple:
        #Считываем заголовок таблицы из конфиг данных, закрепленных за первой вкладкой
        head = [mapfield.lable for mapfield in self.window.map_list]
        #Считываем и записываем в модель импорта номера столбцов, в которых храняться (combo) и calc столбцы
        combo_colums = [position for position,_ in enumerate(head) if self.window.map_list[position].type in ("combo", "calc")]
        #Считываем номера столбцов, в которых храняться колмплексные поля (full_name)
        calc_colums = [position for position,_ in enumerate(head) if self.window.map_list[position].type == "calc"]
        #Индекс столбца с prymarykey
        prymaryidx = self.prymaryidx
        return (head, combo_colums, calc_colums, prymaryidx)

    #Метод, который определяет соответствие между уникальными столбцами в БД и файле,
    #список столбцов, которые не надо импортировать и формирует словарь соответствия:
    #{индекс столбца в БД: (индекс столбца в файле, формат даты или None)}
    def prepare_import_params(self, import_model: ImportModel, choose_head: list, what: str) -> tuple:
        dialog = DialogImport(import_model.bd_head, import_model.calc_col, choose_head, what)
        if dialog.exec_():
            #Формируем список номеров колонок, которые не надо записывать в БД (нумерация актуальна для столбцов БД, НЕ столбцов файла)
            import_col = [idx  for idx, position in enumerate(dialog.edit_dict.values()) if position.currentIndex() > -1]
            not_import_col = [pos for pos in range(0, len(choose_head)) if pos not in import_col]
            # На основании выбора пользователя Формируем словарь соответсвия (номер столбца с БД: номер столбца в файле)
            alignment_dict = self.read_alignment_cols(dialog)
            logger.debug("Методом read_alignment_cols сформирован словарь соответсвия между столбцами в Бд и в файле")
            #Определяем индексы уникальных и связанных друг с другом столбцов
            if what == "update":
                uniqs = self.read_uniq_cols(dialog)
                if uniqs:
                    #Расчитываем применяемый в импортируемом массиве индекс уникального столбца из файла
                    uniq_pos_in_file = dialog.edit_dict[uniqs[0]].currentIndex()
                    index_in_import_list_for_uniq_file_pos = import_col.index(uniq_pos_in_file)
                    # Пересчитываем индекс уникального столбца для файла с учетом того, что часть столбцов из него "выкидывается"
                    inv_alignment_dict = {value[0]: key for key, value in alignment_dict.items()}
                    uniq_file = inv_alignment_dict[index_in_import_list_for_uniq_file_pos]
                    uniq_db = uniqs[0]
                    logger.debug(f"Расчитаны индексы связанных уникальных столбцов (uniq_db, uniq_file) = ({uniq_db}, {uniq_file}). Будьте бдительны индекс уникального столбца может поменяться если не все столбцы из файла были выбраны для импорта")
                else:
                    return None
            else:
                (uniq_db, uniq_file) = (-1, -1)
        else:
            Inf_str = "Параметры импорта не заданы. Импорт отстановлен"
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.warning(Inf_str)
            return None
        return ((uniq_db, uniq_file), not_import_col, alignment_dict)

    #Метод, который определяет соответствие между уникальными столбцами в БД и файле,
    def read_uniq_cols(self, dialog: import_in_BD.DialogImport) -> tuple:
        #Считываем номер указанного пользователем уникального столбца в БД
        uniq_db = dialog.uniq_db.currentIndex()
        if uniq_db == -1:
            Inf_str = "Не выбран столбец, который не должен меняться при обновлении БД данными из файла. Обновление отменено"
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.warning(Inf_str)
            return None
        else:
            pass
        #Считываем номер указанного пользователем уникального столбца в файле
        uniq_file = dialog.uniq_file.currentIndex()
        if uniq_file == -1:
            Inf_str = "Не выбран столбец, который необходимо соотнести со столбцом БД, который не должен меняться при обновлении БД данными из файла. Обновление отменено"
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.warning(Inf_str)
            return None
        else:
            pass
        return (uniq_db, uniq_file)

    # Метод формирует словарь соответсвия для столбцов с датами (номер столбца в БД: (номер столбца в файле, формат даты)),
    #для столбцов без дат (номер столбца в БД: (номер столбца в файле, None)
    def read_alignment_cols(self, dialog: import_in_BD.DialogImport) -> dict:
        alignment_dict = {}
        for position in dialog.edit_dict.keys():
            if dialog.check_dict[position].checkState() == 2:
                alignment_dict[position] = (dialog.edit_dict[position].currentIndex(), dialog.date_dict[position].currentText())
            else:
                alignment_dict[position] = (dialog.edit_dict[position].currentIndex(), None)
        return alignment_dict

    #Только для exell.  Метод, который определяет вкладку файла, с которой необходимо брать данные для импорта
    def choose_sheet(self, import_model: ImportModel) -> str:
        #Считываем названия вкладок из файла и ищем среди них название таблицы, в которую планируется импорт
        try:
            sheets = import_model.read_sheets()
        except:
            Inf_str = "Не удалось считать название книг из файла exell. Импорт остановлен."
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.warning(Inf_str)
            return None
        if self.table_name not in sheets:
            #Спрашиваем у пользователя, из какой вкладки считывать данные
            dialog_sheet = DialogImportSheetName(sheets)
            if dialog_sheet.exec_():
                sheet = dialog_sheet.sheet_edit.currentText()
            else:
                Inf_str = "Вкладка не выбрана. Импорт отстановлен"
                dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                logger.warning(Inf_str)
                return None
        else:
            sheet = self.table_name
        return sheet

    #Только для exell.  Метод, который определяет номер строки вкладки, в которой
    #хранится заголовок таблицы в файле
    def choose_first_row(self, where: str) -> int:
        if where == "exell":
            #Коггда вкладка выбрана. Выбираем строку, в которой храняться заголовки таблицы
            dialog = DialogImportHead()
            if dialog.exec_():
                try:
                    first_row = int(dialog.first_obj.text())
                except:
                    Inf_str = "Строка с названиями столбцов указана неверно (ожидается целое число). Импорт отстановлен"
                    dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                    logger.warning(Inf_str)
                    return None
            else:
                Inf_str = "Строка с названиями столбцов не выбрана. Импорт отстановлен"
                dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                logger.warning(Inf_str)
                return None
        else:
            first_row = 1
        return first_row

    #Метод, для добавления при импорте новых строк
    def add_import(self, import_data: TransportModel, import_model: ImportModel, *args) -> bool:
        self.import_servise_model = self.create_servise_model()
        new_id = self.generate_new_id(self.import_servise_model, self.prymaryidx)
        if len(import_data.data_table) > import_model.row_in_pack:
            logger.debug(f"Так как размер импортируемых данных выше заданного для безпакетной обработки для добавления записей в таблицу запущен метод import_or_update_with_progress")
            (done_count, fail_count, drop_count, _) = self.import_or_update_with_progress("add", import_model, import_data.data_table, new_id = new_id)
        else:
            logger.debug(f"Так как размер импортируемых данных ниже заданного для безпакетной обработки для добавления записей в таблицу запущен метод import_no_progress")
            (done_count, fail_count, drop_count, _) = self.import_no_progress(import_model, import_data.data_table, new_id)
        #self.import_servise_model.query().finish()
        if done_count > 0 and drop_count == 0:
            logger.info(f"Добавление записей в таблицу завершено. Успешно добавлено {done_count} записей. Возникли проблемы с добавлением {fail_count} записей. Запущен метод update_all_windows (для обновления моделей данных всех окон)")
            self.save_changes_report(import_model)
            MainWinModel.update_all_windows(self.window.inital_window)
            return True
        elif done_count > 0 and drop_count == 1:
            logger.info(f"Добавление записей в таблицу завершен пользователем (прерван). Успешно добавлено {done_count} записей. Возникли проблемы с добавлением {fail_count} записей. Запущен метод update_all_windows (для обновления моделей данных всех окон)")
            self.save_changes_report(import_model)
            MainWinModel.update_all_windows(self.window.inital_window)
            return True
        #return True

    def import_or_update_with_progress(self, what: str, import_model: ImportModel, import_pack: list, **kwargs) -> bool:
        #Варианты используемых функций, в зависимости от выбранного действия (обновление,добавление)
        FILE_import_command = {"add": MainWinModel.import_no_progress, "update": MainWinModel.update_no_progress}
        #Показываем строку прогресса и задаем нач. значение
        begin = 0
        self.window.progress.setVisible(True)
        self.window.progress.setValue(begin)
        #Определяем на какое кол-во пакетов будут разбиты импортируемые данные
        number_packs = len(import_pack)//import_model.row_in_pack + 1
        sum_done_count, sum_fail_count, sum_drop_count = (0,0,0)
        for index in range(number_packs):
            #Вызываем импорт/обновление для пачки записей
            (done_count, fail_count, drop_count, new_id) = FILE_import_command[what](self, import_model, import_pack[begin:begin + import_model.row_in_pack], **kwargs)
            sum_done_count, sum_fail_count, sum_drop_count = (sum_done_count + done_count, sum_fail_count + fail_count, sum_drop_count + drop_count)
            #Если в процессе добавления появились дубликаты и пользователь решил прервать процесс
            if drop_count == 1:
                Log_str = f'Пользователь прервал процесс после выявления дубликатов. До приостановки было добавлено(обновлено) {done_count} записей'
                logger.info(Log_str)
                break
            kwargs['new_id'] = new_id
            begin = begin + import_model.row_in_pack
            self.window.progress.setValue(index*100//number_packs)
        self.window.progress.setVisible(False)
        return (sum_done_count, sum_fail_count, sum_drop_count, new_id)

    def import_no_progress(self, import_model, import_pack, new_id, **kwargs) -> bool:
        (done_count, fail_count, drop_count) = (0, 0, 0)
        for record in import_pack:
            insert_rez = self.insert_add_import_rec(import_model, record, new_id)
            if insert_rez == 'DONE':
                new_id = new_id + 1
                done_count = done_count + 1
            elif insert_rez == 'DROP':
                drop_count = 1
                break
            elif insert_rez == 'FAIL':
                fail_count = fail_count + 1
        return (done_count, fail_count, drop_count, new_id)


    #Метод, для добавления одной строки при импорте
    def insert_add_import_rec(self, import_model: ImportModel, import_record: list, new_id: int) -> bool:
        record = self.import_servise_model.record()
        record.setGenerated(self.prymaryidx, True)
        _pos_list = [pos for pos in range(0, len(import_model.etalon_dict)) if pos != self.prymaryidx]
        #Считаем, что массив в import_data иммет такой же формат (те же колонки, в том же порядке), как таблица, в которую мы импортируем
        for position in _pos_list:
            if position in import_model.calc_col:
                record = self.fill_calc_col(import_record, record, position)
            elif position in import_model.combo_col:
                record = self.fill_combo_col(import_record, record, position)
            else:
                record.setValue(position, import_record[position])
        record.setValue(self.prymaryidx, new_id)
        insert_rez = self.insert_rec(self.window, record, self.import_servise_model)
        if insert_rez == "DONE":
            Log_str = f'Новая запись с primary key:{self.prymarykey} = {new_id} в таблицу {self.table_name} добавлена. '
            logger.info(Log_str)
            return "DONE"
        elif insert_rez == "DROP":
            Log_str = f'Пользователь прервал процесс после выявления дубликатов, запись не добавлена в БД'
            logger.info(Log_str)
            return "DROP"
        elif insert_rez == "FAIL":
            Err_str = f'При добавлении записи произошла ошибка, запись не добавлена в БД'
            logger.debug(Err_str)
            return "FAIL"
        elif insert_rez == "PASS":
            Log_str = f'В записи найдены дубликаты. Пользователь отказался от нее импорта в БД'
            logger.debug(Log_str)
            return "PASS"
        else:
            Err_str = f'В модуле insert_rec произошла ошибка, запись не добавлена в БД'
            logger.debug(Err_str)
            return 'FAIL'

    #Метод, создает модель данных обновляемой таблицы и активирует для нее импорт или обновление (со строкой прогресса или без нее)
    def update_import(self, import_data: TransportModel, import_model: ImportModel, *args) -> bool:
        #Если столбцы для связи между таблицами в БД и файле выбраны
        if import_model.uniq_db_col > -1 and import_model.uniq_file_col > -1:
            self.import_servise_model = self.create_servise_model()
            if len(import_data.data_table) > import_model.row_in_pack:
                logger.debug(f"Так как размер импортируемых данных выше заданного для безпакетной обработки для обновления таблицы запущен метод import_or_update_with_progress")
                (done_count, fail_count, drop_count, _) = self.import_or_update_with_progress("update", import_model, import_data.data_table)
            else:
                logger.debug(f"Так как размер импортируемых данных ниже заданного для безпакетной обработки для обновления таблицы  запущен метод update_no_progress")
                (done_count, fail_count, drop_count, _) = self.update_no_progress(import_model, import_data.data_table)
            if done_count > 0 and drop_count == 0:
                logger.info(f"бновление таблицы завершено. Успешно обновлено {done_count} записей. Возникли проблемы с обновлением {fail_count} записей. Запущен метод update_all_windows (для обновления моделей данных всех окон)")
                self.save_changes_report(import_model)
                MainWinModel.update_all_windows(self.window.inital_window)
                return True
            elif done_count > 0 and drop_count == 1:
                logger.info(f"Обновление таблицы завершено пользователем (прервано). Успешно обновлено {done_count} записей. Возникли проблемы с обновлением {fail_count} записей. Запущен метод update_all_windows (для обновления моделей данных всех окон)")
                self.save_changes_report(import_model)
                MainWinModel.update_all_windows(self.window.inital_window)
                return True

        else:
            Inf_str = "Не выбран столбец, который не должен меняться при обновлении БД данными из файла. Обновление отменено"
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.warning(Inf_str)
            return False

    def update_no_progress(self, import_model: ImportModel, import_pack: list, **kwargs) -> bool:
        (done_count, fail_count, drop_count) = (0,0,0)
        for record in import_pack:
            insert_rez = self.insert_update_import_rec(record, import_model)
            if insert_rez == 'DONE':
                done_count = done_count + 1
            elif insert_rez == 'DROP':
                drop_count = 1
                break
            elif insert_rez == 'FAIL':
                fail_count = fail_count + 1
        return (done_count, fail_count, drop_count, 0)

    #Метод, для обновления данных одной строки при импорте
    def insert_update_import_rec(self, import_record: list, import_model: ImportModel) -> bool:
        #Устанавливаем флаг отсутвия импортируемой записи в моделями
        _not_in_BD = True
        import_rez = 'PASS'
        for row_number in range(0, self.import_servise_model.rowCount()):
            #Считываем одну запись из БД
            record = self.import_servise_model.record(row_number)
            new_record = self.import_servise_model.record(row_number)
            if str(record.value(import_model.uniq_db_col)).strip() == str(import_record[import_model.uniq_file_col]).strip():
                #Импортируемая запись найдена в БД. Снимаем для нее флаг
                _not_in_BD = False
                #Переписываем в запись данные из импортируемой записи
                new_record = self.set_value_in_record(import_model, new_record, import_record)
                #Переносим запись в БД
                if self.set_value_in_BD(self.import_servise_model, row_number, new_record):
                    #Записываем данные об изменениях в таблицу изменений
                    logger.debug("Методом set_value_in_BD в строке БД данные заменены на импортируемые данные. Вызван метод find_update_changes для фиксации изменений в отчетной таблице")
                    self.find_update_changes(import_model, record, new_record, import_record)
                    import_rez = 'DONE'
            else:
                #Если уникальные значения столбцов для импортируемой записи и записи в БД не совпали
                pass
        #После проверки всех записей в модели, если импортируемая запись не была найдена (_not_in_BD = True)
        if _not_in_BD == True:
            #Определяем следующий по порядку за уже существующими в БД prymary key, он потребуется, если прийдеться добавлять записи в БД
            new_id = self.generate_new_id(self.import_servise_model, self.prymaryidx)
            #Запускаем добавление записи
            insert_rez = self.insert_add_import_rec(import_model, import_record, new_id)
            if insert_rez == 'DONE':
                logger.debug("Импортируемая запись не обнаружена в БД. Методом  _add_import_rec в БД добавлена новая запись.  Вызван метод find_update_changes для фиксации изменений в отчетной таблице")
                self.find_update_changes(import_model, record, new_record, import_record)
                return 'DONE'
            elif insert_rez == 'DROP':
                Log_str = f'Пользователь прервал процесс после выявления дубликатов, запись не добавлена в БД'
                logger.info(Log_str)
                return 'DROP'
        return import_rez

    #Метод, для заполнения записи БД импортируемыми значениями
    def set_value_in_record(self, import_model: ImportModel, record: QSqlRecord, import_record: list) -> QSqlRecord:
        for position, item in enumerate(import_record):
            #Если это вычислияемый столбец
            if position in import_model.calc_col:
                record = self.fill_calc_col(import_record, record, position)
                logger.debug(f"Для заполнения записи БД импортируемыми значениями в вычисляемом столбце {position} запущен метод fill_calc_col")
            #Если это столбец с prymary key или столбец, который не надо импортировать (кроме вычисляемого). Оставляем значение таким, каким оно записано в БД
            elif position in import_model.combo_col:
                record = self.fill_combo_col(import_record, record, position)
                logger.debug(f"Для заполнения записи БД импортируемыми значениями в комбо-столбце {position} запущен метод fill_combo_col")
            #Если это не столбец с prymary key и не столбец, который не надо импортировать (нет в файле, содержит внешние включи, вычислияемый столбец)
            elif position != import_model.prymary_col and position not in import_model.not_import_col:
                record.setValue(position, import_record[position])
            else:
                pass
        return record

    #Метод, для записи записи из модели данных в БД
    def set_value_in_BD(self, data_model: QSqlRelationalTableModel, row_number: int, record: QSqlRecord) -> bool:
        #data_model.removeRows(row_number, 1)
        old_record = data_model.record(row_number)
        print(row_number, record.value(1), old_record.value(1))
        if data_model.setRecord(row_number, record):
            if data_model.submitAll():
                Log_str = f'Запись с primary key:{self.prymarykey} = {record.value(self.prymaryidx)} в таблице {self.table_name} обновлена. '
                logger.info(Log_str)
                return True
            else:
                Error_str = f'Запись с primary key:{self.prymarykey} = {record.value(self.prymaryidx)} в таблице {self.table_name} не обновлена. Ошибка {data_model.lastError().text()}'
                logger.warning(Error_str)
                #Откатываем изменения модели данных назад
                data_model.revertAll()
        else:
            Error_str = f'Запись с primary key:{self.prymarykey} = {record.value(self.prymaryidx)} в таблице {self.table_name} не обновлена. Ошибка {data_model.lastError().text()}'
            logger.warning(Error_str)

    #Метод который сравнивает данные в БД до и после обновления. Формирует отчетную таблицу со столбцами:
    #- столбец, через который связываются записи в БД и файле (название),
    #- значение уникального столбца для изменненой записи
    #- столбец, в котором произошли изменения (название)
    #- значение, которое было в столбце
    #- значение, которое должно быловставиться
    #- значение, которое в итоге оказалось в БД
    def find_update_changes(self, import_model: ImportModel, bd_record: QSqlRecord, new_bd_record: QSqlRecord, import_record: list):
        check_col = [mapfield.index_map for mapfield in self.window.map_list if mapfield.check == "yes"]
        combo_col = import_model.combo_col
        for pos in check_col:
            if pos in combo_col:
                #Если значение ячейки в импортируемой записи не совпадает со значением в БД
                if str(import_record[pos]) != self.find_combo_value(bd_record.value(pos), pos):
                    #Формируем запись для отчетной таблицы
                    check_record = [import_model.bd_head[import_model.uniq_db_col], import_record[import_model.uniq_db_col], import_model.bd_head[pos], self.find_combo_value(bd_record.value(pos), pos), import_record[pos], self.find_combo_value(new_bd_record.value(pos), pos)]
                    check_record = [item if item != None else "Пустое значение" for item in check_record]
                    #Если значение в контролируемом столбце изменилось. Записываем запись в отчетную таблицу
                    if check_record[3] != check_record[5]:
                        import_model.check_table.append(check_record)
            else:
                if str(import_record[pos]) != bd_record.value(pos):
                    check_record = [import_model.bd_head[import_model.uniq_db_col], import_record[import_model.uniq_db_col], import_model.bd_head[pos], bd_record.value(pos), import_record[pos], new_bd_record.value(pos)]
                    check_record = [item if item != None else "Пустое значение" for item in check_record]
                    #Если значение в контролируемом столбце изменилось. Записываем запись в отчетную таблицу
                    if check_record[3] != check_record[5]:
                        import_model.check_table.append(check_record)


    #Метод, который определяет значение, которую надо вставить в строку в доп модели, в которой хранится значение, соответствующее
    #значению, которое хранится в combo-столбце основной таблицы
    def find_combo_value(self, prymary_volue: str, import_colum_index: int) -> str:
        (prymary_colum_index, combo_colum_index, combo_model) = self.create_combo_model(import_colum_index)
        if combo_colum_index:
            #Формируем словарь, где для каждой строки в комбо-модели:  { значение prymory key: значение элемента в ссылочном столбце}
            combo_table_dict = {combo_model.record(row).value(prymary_colum_index): combo_model.record(row).value(combo_colum_index) for row in range(0, combo_model.rowCount())}
            logger.debug("Методом find_combo_value определен словарь для расчета значение ячейки в подстановочной комбо-таблице, связанной со значением, хранящимся в комбо-столбце первичной таблицы.")
        else:
            combo_table_dict = {}
            logger.debug("Методом find_combo_value не удалось определить словарь для расчета значение ячейки в подстановочной комбо-таблице, связанной со значением, хранящимся в комбо-столбце первичной таблицы. Создан пустой словарь.")
        #Ищем значение prymory key для импортируемого значения, считанного из файла
        combo_value = combo_table_dict.get(prymary_volue, None)
        return combo_value

    #Метод, который создает модель доп. таблицы, на которую ссылаются combo-столбцы,
    #определяет индекс столбцов с импортируемыми значениями в этой таблице
    def create_combo_model(self, import_colum_index: int) -> tuple:
        #Определяем название таблицы, на которую ссылается импортируемый столбец
        combo_table = self.window.map_list[import_colum_index].table
        #Определяем название столбца, на который ссылается импортируемый столбец (ссылочный столбец)
        combo_colum = self.window.map_list[import_colum_index].column
        #Определяем prymory key в таблице, на которую ссылается импортируемый столбец
        prymary_colum_index = self.window.map_list[import_colum_index].pkey_idx
        #Формируем модель таблицы, на которую ссылается импортируемый столбец
        combo_model = QSqlRelationalTableModel(db = self.db)
        combo_model.setEditStrategy(2)
        combo_model.setTable(combo_table)
        try:
            combo_model.select()
            logger.debug(f"Создана сервисная модель данных для подстановочной комбо-таблицы {combo_table}")
            #Определяем индекс ссылочного столбца
            combo_colum_index = combo_model.fieldIndex(combo_colum)
        except:
            logger.warning(f"Не удалось создать валидную сервисная модель данных для подстановочной комбо-таблицы {combo_table}")
            combo_colum_index = None
        return (prymary_colum_index, combo_colum_index, combo_model)

    #Метод, для заполнения записи БД значениями вычисляемых столбцов
    def fill_calc_col(self, import_record: list, record: QSqlRecord, position: int) -> QSqlRecord:
        map_dict = {mapperfield.column: mapperfield.index_map for mapperfield in self.window.map_list}
        name = import_record[map_dict.get("name", "")]
        begin = import_record[map_dict.get("begin", "")]
        begin = QDate.fromString(begin, "yyyy-MM-dd").toString("dd.MM.yyyy")
        numb = import_record[map_dict.get("numb", "")]
        full_name_str = f'{name} от {begin} № {numb}'
        record.setValue(position, full_name_str)
        logger.debug(f"Сформирована строка формата 'name от begin № numb'. Строка записана в вычисляемое поле, столбец: {position}.")
        return record

    #Метод, для заполнения записи БД значениями комбо-столбцов
    def fill_combo_col(self, import_record: list, record: QSqlRecord, position: int) -> QSqlRecord:
        combo_index = self.find_combo_index(position, import_record[position])
        if combo_index != None:
            logger.debug("Методом find_combo_index определен индекс в связанной таблице, соответсвующий записываемому в комбо-столбец первичной таблицы значению. Индекс записан в подстановочную таблицу")
            record.setValue(position, combo_index)
        else:
            logger.debug("Методом find_combo_index не удалось определить индекс в связанной таблице, соответсвующий записываемому в комбо-столбец первичной таблицы значению. Запись постановочной таблицы не изменена")
        return record

    #Метод, который определяет номер строки в доп модели, в которой хранится значение, которое в комбо-столбце записано в импортируемом файле
    def find_combo_index(self, import_colum_index: int, import_value: str) -> int:
        (prymary_colum_index, combo_colum_index, combo_model) = self.create_combo_model(import_colum_index)
        #Формируем словарь, где для каждой строки в комбо-модели:  {значение элемента в ссылочном столбце: значение prymory key}
        try:
            combo_table_dict = {combo_model.record(row).value(combo_colum_index): combo_model.record(row).value(prymary_colum_index) for row in range(0, combo_model.rowCount())}
        except:
            logger.warning("В процессе формирования словаря {значение элемента в ссылочном столбце: значение prymory key} произошла ошибка. Создан пустой словарь")
            combo_table_dict = {}
        #Ищем значение prymory key для импортируемого значения, считанного из файла
        combo_index = combo_table_dict.get(str(import_value), None)
        return combo_index

    #Метод, который активирует автоматическое обновление таблиц БД (на основании ранее созданных моделей импорта)
    @generate_args
    def start_auto_update(self, window, **kwargs):
        #Сколько файлов обновляем
        dialog = DialogImportConfigList()
        if dialog.exec_():
            number = dialog.edit.currentText()
            if number == "Таблицы текущего(активного) окна":
                Wrn_str = f'Внимание, убедитесь, что вызываете импорт из того окна, таблицу которого хотите обновить!'
                dialog = QMessageBox.warning(self.window, "Внимание", Wrn_str)
                logger.debug("Выбран параметр 'Таблицы текущего(активного) окна', вызван метод prepare_update_one_file")
                update = self.prepare_update_one_file()
            else:
                logger.debug("Выбран параметр 'Других таблиц', вызван метод prepare_update_few_file")
                update = self.prepare_update_few_file()
            if update:
                Inf_str = "Автообновление данных в БД завершено успешно"
                dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
        else:
            Inf_str = "Параметры обновления не выбраны. Импорт отстановлен"
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            return None

    #Метод, который определяет файл, где хранятся параметры импорта и запускает автообновление одного файла
    def prepare_update_one_file(self) -> bool:
        #Создаем модель импорта для считвания параметров модели импорта
        subimport_model = ImportModel(self.window, "txt", "import_model", "import_models")
        subimport_model.choose_file_name()
        file_with_params = subimport_model.file_name
        if not file_with_params:
            Inf_str = f'Не выбран файл, в котором хранятся параметры импорта (import_model). Обновление остановлено'
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.debug(Inf_str)
            return False
        else:
            logger.debug(f"Для автоматического обновления данных из файла {file_with_params} считаны параметры модели импорта (ImportModel). Вызван метод auto_update.")
            upd = self.auto_update(file_with_params)
            return upd

    #Метод, создает модель импорта на основаниипараметров ранее использованной модели и с помощью нее проводит импорт данных
    def auto_update(self, file_with_params: str) -> bool:
        #Создаем пустую модель импорта
        import_model = ImportModel(self.window, "", "", "")
        try:
            import_model.load(file_with_params)
            #Cчитываем данные для импорта
            import_data = import_model.read_data_for_import()
        except:
            logger.warning(f"Не удалось подготовить валидную модель импорта на основании файла {file_with_params}. Импорт будет завершен")
            import_data = None
        if import_data == None:
            upd = False
        else:
            #Запускаем данные в БД (дописываем, обновляем или подъменяем)
            logger.debug(f"Для автоматического обновления данных на основании файла {file_with_params} создана модели импорта (ImportModel). Вызван метод update_import")
            upd = self.update_import(import_data, import_model)
        return upd

    #Метод, который определяет названия таблиц для обновления и файлы, где хранятся
    #параметры импорта и запускает последовательное автообновление файлов
    def prepare_update_few_file(self) -> bool:
        #Считываем словарь mapper_листов из конфига
        try:
            from models.configs.config_mapperfields import mapper_lists
            logger.debug(f"Список с параметрами таблиц (mapper_lists) импортирован из  models.configs.config_mapperfields. Используется для построения списка таблиц в процессе автоматичнского импорта")
        except:
            logger.debug(f"Не удалось импортировать список с параметрами таблиц (mapper_lists) импортирован из  models.configs.config_mapperfields. Список заменен на условно пустой")
            mapper_lists = {self.table_name: None}
        #Формируем список названий таблиц (которые являются ключами в этом словаре)
        tables = [table for table in mapper_lists.keys()]
        tables_sort = tables
        tables_sort.sort()
        dialog = DialogImportConfigList2(tables_sort)
        if not dialog.exec_():
            Inf_str = f'Не выбраны названия таблиц и файлы с моделями импорта. Автообновление отменено'
            dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
            logger.debug(Inf_str)
        else:
            flag_update = False
            for idx, edit in dialog.edit_dict.items():
                if edit.text() != "" and dialog.combo_dict[idx].currentIndex() != -1:
                    logger.debug(f"В процессе автоматического импорта для пары таблица - модель импорта ({dialog.combo_dict[idx].currentText()} - {edit.text()}) запущен метод open_window_for_update ")
                    window_model_for_update = self.open_window_for_update(dialog.combo_dict[idx].currentText())
                    logger.debug(f"В процессе автоматического импорта для пары таблица - модель импорта ({dialog.combo_dict[idx].currentText()} - {edit.text()}) запущен метод auto_update ")
                    upd = window_model_for_update.auto_update(edit.text())
                    if upd == False:
                        Inf_str = f'Автообновление в таблице {dialog.combo_dict[idx].currentText()} завершилось с ошибкой'
                        dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                        logger.debug(Inf_str)
                        return False
                    else:
                        flag_update = True
            if flag_update == False:
                Inf_str = f'Не задано ни одной корректной пары: название таблицы, подлежащей обновлению - файл с параметрами импорта (модель импорта). Автообновление не выполнено'
                dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
                logger.debug(Inf_str)
            else:
                return True

    #Метод, который открывет основное окно (привязанное к таблице, которую планируется обновить)
    # и формирует для него модель манипуляции
    def open_window_for_update(self, table_name: str):
        #Создаем окно, в котором планируется обновление
        module_name = table_name
        window_for_update = self.window.inital_window.open_main_window(config_module_name = module_name, max_width = self.window.inital_window.max_width)
        window_model_for_update = window_for_update.current_main
        logger.debug(f"Для автоматического обновления данных в таблице {table_name} созданы модель основного окна (MainWindow) и модель для манипуляции (MainWinModel)")
        return window_model_for_update

    #Метод который сохраняет отчет с результатами сравнения данных в БД до и после обновления
    def save_changes_report(self, import_model: ImportModel):
        export_sets = [TransportModel(self.table_name, import_model.check_table[0], import_model.check_table[1:]),]
        logger.debug(f"Создан список объектов типа TransportModel с отчетом о результатах обновления таблицы {self.table_name}")
        #Создаем каталог для сохранения отчетов
        file_name = f'report-update-{self.table_name}-{QDate.currentDate().toString("dd.MM.yyyy")}'
        export_model = ExportModel(self.window, export_sets, "exell", file_name, "report_updates")
        Inf_str = f'Задайте имя файла для сохранения отчета об изменении "контролируемых" столбцов'
        dialog = QMessageBox.information(self.window, "Уведомление", Inf_str)
        if export_model.choose_file_name():
            logger.debug(f"Создан объект модели экспорта (ExportModel) для реализации экспорта отчета о результатах обновления таблицы {self.table_name}. Активирован экспорт")
            #Активируем экспорт
            export_model.export()

    def read_data(self, model):
        data_table =  []
        if model.query().first():
            rec = [model.query().value(idx) for idx in range(0, model.columnCount())]
            data_table.append(rec)
            while model.query().next():
                rec =  [model.query().value(idx) for idx in range(0, model.columnCount())]
                data_table.append(rec)

        return data_table


    #Для всех колонок, в которых есть возможность загрузки с рассчетом схожести
    #с эталонными значениями предполагается наличие такой конфигурации:
    #- in_model - модель таблицы в которую данные загружаются только на время обработки и расчета схожести
    #- out_model - модель таблицы в которую данные загружаются после обработки и расчета схожести (на хранение)
    #- combo_model - модель таблицы, в которой храняться эталонные значения параметра, к одному из которых в конечном итоге должна быть привязана каждая запись в out_model
    #!!!Должен запускаться из таблицы хранения

    #Импортируем в таблицу записи, испозьзуя механизмы корреляции
    def start_import_with_corr(self):
        #Считываем индексы стобцов таблицы хранения
        #Название таблицы
        out_table = self.table_name
        #Название столбца с prk
        out_prk_name = self.prymarykey
        #индекс столбца с prk
        out_prk_idx = self.prymaryidx
        #Индекс столбца с обрабатываемым параметром
        out_value_idx = [map_field.index_map for map_field in self.window.map_list if map_field.corr_import == "corr_edit"][0]
        #Индекс столбца с которым через корреляцию должен быть связан обрабатываемый параметр
        combo_idx = [map_field.index_map for map_field in self.window.map_list if map_field.corr_import == "corr_combo"][0]
        #Индекс столбца, в котором храниться показатель корреляции
        corr_idx = [map_field.index_map for map_field in self.window.map_list if map_field.corr_import == "corr_corr"][0]
        #Название таблицы загрузки
        in_table = [map_field.corr_table for map_field in self.window.map_list if map_field.corr_import == "corr_edit"][0]
        #Проверяем,что конфигурации таблицы хранения и таблицы загрузки совпадают
        #!!!!!!!!assert
        in_prk_name = out_prk_name
        in_prk_idx = out_prk_idx
        in_value_idx = out_value_idx
        #загружаем новые данные стандартным порядком в таблицу загрузки
        #Создаем объект окна для таблицы загрузки. Далее все манипуляции проводим на нем
        in_win_model = self.open_window_for_update(in_table)
        in_win_model.start_import_no_corr(window = in_win_model.window, where = "exell", what = "add")
        #Формируем модель таблицы-загрузки
        in_model = in_win_model.create_servise_model(in_table, in_prk_name)
        #Формируем модель таблицы-хранения
        out_model = in_win_model.create_servise_model(out_table, out_prk_name)
        #Формируем комбо-модель (связную с таблицей хранения по компбо столбцу)
        (combo_prk_idx, combo_value_idx, combo_model) = in_win_model.create_combo_model(combo_idx)
        #Считываем все записи из таблицы-хранения
        out_datas = in_win_model.read_data(out_model)
        #Считываем все записи из комбо-таблицы
        combo_datas = in_win_model.read_data(combo_model)
        #Импортируем записи, у которых название совпадаетсназванием однойиззаписей в комбо-таблице.
        loaded = in_win_model.import_by_BD(out_datas, combo_datas, in_model, in_value_idx, combo_idx, combo_prk_idx, combo_value_idx, out_model, out_prk_idx)
        print(f"На первом этапе на основании ранее импортируемых записей загружено записей: {loaded}")
        #Импортируем записи на основании корреляции (corr > 0.55)
        (loaded, siblings) = in_win_model.import_by_corr(corr_idx, combo_datas, in_model, in_value_idx, combo_idx, combo_prk_idx, combo_value_idx, out_model, out_prk_idx, combo_model)
        print(f"На втором этапе на основании показателей корреляции загружено записей: {loaded}")
        #Импортируем записи наосновании выбора пользователя (подбирает под загруженный параметр параметр из комбо-таблицы)
        loaded = in_win_model.import_by_choose(corr_idx, combo_datas, siblings, in_model, in_value_idx, combo_idx, out_model, out_prk_idx, combo_model, combo_value_idx, combo_prk_idx)
        print(f"На третьем этапе на основании выбора пользователя загружено записей: {loaded}")
        MainWinModel.update_all_windows(self.window.inital_window)
        #Закрываем окно загрузки
        in_win_model.window.close()

    #Определяет есть ли в основной таблице параметра запись о таком названии.
    #Если есть - переносит записи в основную таблицу и удаляет из промежуточной
    #Конфигурация обоих таблиц должна быть одинаковой
    def import_by_BD(self, out_datas, combo_datas, in_model, in_value_idx, combo_idx, combo_prk_idx, combo_value_idx, out_model, out_prk_idx):
        loaded = 0
        row_for_del = []
        #Составляем словарь {"загрузочное" значение параметра: значение сопоставленного с ним значения из комбо-таблицы
        out_dict = {out_data[in_value_idx]: out_data[combo_idx] for out_data in out_datas}
        combo_dict = {combo_data[combo_value_idx]: combo_data[combo_prk_idx] for combo_data in combo_datas}
        #Для каждой заoписи в таблице загрузки
        for row_numb in range(in_model.rowCount()):
            in_record = in_model.record(row_numb)
            #Если аналогичному расчетному параметру ранее уже было сопоставлено значение в таблице хранения
            #Prkey для связанной созначением комбо-записи
            out_value = out_dict.get(in_record.value(in_value_idx))
            if out_value:
                #Заполняем запись сопоставленным значением
                in_record.setValue(combo_idx, out_value)
                #Записываем запись в таблицу хранения
                if self.corr_insert_record(out_model, in_record, out_prk_idx):
                    loaded = loaded + 1
                    #Создаем список на удаление из загрузочной таблицы
                    row_for_del.append(row_numb)
        if self.remoove_rec(row_for_del, in_model, in_model.tableName()):
            logger.info(f'Записи {row_for_del} перенесены в основную таблицу и удалена иззагрузочной')
        else:
            logger.info(f'Записи {row_for_del} перенесена в основную таблицу, но не удалена из загрузочной')
        return loaded

    #Для всех оставшися записей в таблице загрузки рассчитывает коэффициент корреляции между параметром из загруженной записи и
    #всеми возможнымизначениями параметров из компбо-таблицы, записывает в столбец corr наилучщий показатель.
    #Если corr больше 0.55, записываем запись в таблицу хранения. Если нет, оставляем втаблице загрузки
    def import_by_corr(self, corr_idx, combo_datas, in_model, in_value_idx, combo_idx, combo_prk_idx, combo_value_idx, out_model, out_prk_idx, combo_model):
        loaded = 0
        row_for_del = []
        #Составляем словарь {"загрузочное" значение параметра: prkey сопоставленного с ним значения из комбо-таблицы
        combo_dict = {combo_data[combo_value_idx]: combo_data[combo_prk_idx] for combo_data in combo_datas}
        #Считываем по одной записи из таблицы загрузки и подбираем для каждой запись из комбо-таблицы
        sibling_values = []
        for row_number in range(0, in_model.rowCount()):
            record = in_model.record(row_number)
            in_value = record.value(in_value_idx)
            if in_value:
                (best_row, rvalue, siblings) = siblins_soft_for_one_rec(in_value, combo_datas, combo_value_idx)
                #Из индексов наиболее близких по корреляции строк высчитываем значение параметра в комбо-таблице
                sibling_list = [combo_datas[sibling][combo_value_idx] for sibling in siblings]
                #Записываем значение параметров в список
                sibling_values.extend(sibling_list)
                #Если наилучший коэффициент связности меньше 0.2 считаем что запись подобрать не удалось
                if rvalue < 0.15:
                    record.setValue(combo_idx, None)
                    record.setValue(corr_idx, str(rvalue))
                else:
                    combo_value =  combo_datas[best_row][combo_value_idx]
                    combo_prk_for_value = combo_dict.get(combo_value)
                    record.setValue(combo_idx, combo_prk_for_value)
                    record.setValue(corr_idx, str(rvalue))
                #Записываем измененную запись в таблицу загрузки
                self.set_value_in_BD(in_model, row_number, record)
                #Если п\корреляция более 55 % добавляем запись в таблицу хранения
                if rvalue > 0.55:
                    #Копируем запись чтобы не ломать основну
                    record_for_out = record
                    #Записываем запись в таблицу хранения
                    if self.corr_insert_record(out_model, record_for_out, out_prk_idx):
                        loaded = loaded + 1
                        #Создаем список на удаление из загрузочной таблицы
                        row_for_del.append(row_number)
        if self.remoove_rec(row_for_del, in_model, in_model.tableName()):
            logger.debug(f"Запись о ПО высокой корреляцией перенесена в основную и удалена из ромежуточной таблицы")
        #Возвращаем кол-во загруженных записей и отсортированный по алфовиту с выкинутыми повторениями список ближайших значений для всех проанализированнызх через корреляцию записей
        sibling_values.append("не определено")
        return (loaded, sorted(list(set(sibling_values))))

    #На основании составленной пользователем таблицы определяет:
    #какие загруженные записи связаны с араметрами, которые уже есть в комбо-таблице, такие записи записываеются в таблицу сохранения
    #для каких загруженных записей в БД нет подходящего параметра, для таких записей создаетсязапись в комбо-таблице и запись втаблице хранения
    def import_by_choose(self, corr_idx, combo_datas, siblings, in_model, in_value_idx, combo_idx, out_model, out_prk_idx, combo_model, combo_value_idx, combo_prk_idx):
        #Формируем список пар (номер строки в таблице загрузки, значение втаблице загрузки, подобранное покорреляции значение из комбо-таблицы)
        all_pair_values = self.calc_pairs(in_model, in_value_idx, combo_idx, combo_datas, combo_prk_idx, combo_value_idx)
        if all_pair_values == []:
            return 0
        #Просим пользователя подобрать к плохо рассчитанным по корреляции значениям параметра значения из комбо-таблицы
        all_choose_values = self.calc_choose(all_pair_values, siblings)
        #Заполнняем записи в таблице загрузке и копируем их в таблицу хранения. Формируем список записей из таблицы загрузки на удаление
        (loaded, row_for_del) = self.fill_records(all_pair_values, all_choose_values, in_model, combo_datas, combo_model, combo_idx, combo_value_idx, combo_prk_idx, out_model, out_prk_idx)
        #Удаляем записи из таблицы загрузки
        self.remoove_rec(row_for_del, in_model, in_model.tableName())
        return loaded

    #Формирует список пар (номер строки в таблице загрузки, значение втаблице загрузки, подобранное покорреляции значение из комбо-таблицы)
    def calc_pairs(self, in_model, in_value_idx, combo_idx, combo_datas, combo_prk_idx, combo_value_idx):
        all_pair_values = []
        combo_dict_value_by_prk = {combo_data[combo_prk_idx]: combo_data[combo_value_idx] for combo_data in combo_datas}
        #Для каждой записи втаблице загрузки расчитываем пару загрузочное значение - подобранное на основании корреляции значение
        for row_number in range(0, in_model.rowCount()):
            record = in_model.record(row_number)
            in_value = record.value(in_value_idx)
            #Вычисляем значение связанной записи из комбо таблицы
            combo_prk_for_value = record.value(combo_idx)
            combo_value = combo_dict_value_by_prk.get(combo_prk_for_value)
            all_pair_values.append((row_number, in_value, combo_value))
        return all_pair_values

    #На основе выбора пользователя расчитывает значения из комбо-таблицы, с которми надо связать параметр из таблицы хранения
    def calc_choose(self, all_pair_values, siblings):
        #Считываем все записанные в комбо-таблицу значения параметра
        #Разбиваем на пакеты по 15 записей, чтобы они поместились на экран
        row_in_pack = 15
        begin = 0
        number_packs = len(all_pair_values)//row_in_pack + 1
        all_choose_values = []
        for index in range(number_packs):
            #Расчитываем подобранные пользователем значения для каждой группы пар
            choose_values = self.choose_one_group(all_pair_values[begin:begin + row_in_pack], siblings)
            all_choose_values.extend(choose_values)
            begin = begin + row_in_pack
        return all_choose_values

    #Заполнняет записи в таблице загрузке и копирует их в таблицу хранения. Формирует список записей из таблицы загрузки на удаление
    def fill_records(self, all_pair_values, all_choose_values, in_model, combo_datas, combo_model, combo_idx, combo_value_idx, combo_prk_idx, out_model, out_prk_idx):
        loaded = 0
        row_for_del = []
        combo_dict_prk_by_value = {combo_data[combo_value_idx]: combo_data[combo_prk_idx] for combo_data in combo_datas}
        for number, choose_value in enumerate(all_choose_values):
            #Соответствующее выбранному значению значение prkey в связной таблице
            combo_prk_for_value = combo_dict_prk_by_value.get(choose_value)
            #Запись из таблицы загрузки, с которой сейчас работаем
            record = in_model.record(all_pair_values[number][0])
            #Если для загруженного значения пользователем подобрано подходщее значение
            if combo_prk_for_value:
                #Устанавливаем найденный индекс в запись таблицы загрузки (из-за особенностей работы qt с комбостолбцами, это не индекс,а само значение)
                record.setValue(combo_idx, combo_prk_for_value)
            else:
                #Записываем в комбо таблицу новую запись с новым ПО для которого ничего не удалось подобрать
                new_record = combo_model.record()
                new_record.setValue(combo_value_idx, all_pair_values[number][1])
                new_id = self.corr_insert_record(combo_model, new_record, combo_prk_idx)
                #Устанавливаем вновь созданный индекс в запись таблицы загрузки (из-за особенностей работы qt с комбостолбцами, это не индекс,а само значение)
                record.setValue(combo_idx, new_id)
            #Дабавляем запись в таблицу загрузки
            if self.set_value_in_BD(in_model, all_pair_values[number][0], record):
                #Записываем запись в таблицу хранения
                #Копируем запись чтобы ее не ломать
                record_for_bd = record
                if self.corr_insert_record(out_model, record_for_bd, out_prk_idx):
                    loaded = loaded + 1
                    #Создаем список на удаление из загрузочной таблицы
                    row_for_del.append(all_pair_values[number][0])
        return (loaded, row_for_del)

    #Расчитываем подобранные пользователем значения для одной группы пар
    def choose_one_group(self, all_pair_values, combo_values):
        choose_pair_values = []
        dialog = DialogAskCorr(all_pair_values, combo_values)
        if dialog.exec_():
            #Для каждого кортежа в списке подбираем под выбранное пользователем значение prkey в комбо таблице
            for number, ask_combo in enumerate(dialog.out_dict.values()):
                #Выбранное пользователем значение
                choose_value = ask_combo.currentText()
                #Формируем итоговый список
                choose_pair_values.append(choose_value)
        return choose_pair_values

    #Записывает запись в БД, определяет нужный номер строки и нужное значение prk
    def corr_insert_record(self, model, record, pr_key_index):
        #Вычисляем номер последней строки в модели, в которую будем вставлять значение
        last_row = model.rowCount()
        #Вычисляем доступное значение для pr_key
        new_id = self.generate_new_id(model, pr_key_index)
        #формируем запись
        record.setValue(pr_key_index, new_id)
        self.insert_rec(self.window, record, model, model.tableName())
        return new_id
