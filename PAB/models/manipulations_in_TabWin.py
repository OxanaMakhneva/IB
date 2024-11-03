from PyQt5.QtCore import QRegExp, QDate, QItemSelectionModel, QSortFilterProxyModel
from PyQt5.QtWidgets import QMenu, QTableView, QDataWidgetMapper, QFormLayout, QMessageBox, QLineEdit, QSpinBox, QComboBox, QDateEdit, QCompleter
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtSql import QSqlRelationalTableModel
from models.other_class_func import CustomDialog
from models.table_model_qt import CustomTableView, CustomQSortFilterProxyModel
from models.relations_in_BD_qt import find_item_row_MM
from models.read_write.export_in_BD import ExportModel
from models.read_write.transport_in_BD import TransportModel
from models.manipulations_in_DB import ServiseModel

import app_logger
logger = app_logger.get_logger(__name__)

#Метод, который формирует и записывает в словарь модели данных общих таблиц
def prom_model(db, prom_dict = {}):
    for key in prom_dict.keys():
        model = QSqlRelationalTableModel(db = db)
        model.setEditStrategy(2)
        #Назначаем для модели основную таблицу, имя считываем:
        model.setTable(key)
        prom_dict[key] = model

#Класс, хранящий данные о структуре таблиц  в БД, которые также используются
#для формирования и управления полями мэппера на вкладках таб-окна
#column_map - служебное имя столбца таблицы вкладки (далее - ТВ) , к которому привязано поле мэппера
#index_map - индекс столбца ТВ, к которому привязано поле мэппера
#lable - текст ярлыка поля (пользовательское название столбца)
#table - имя связанной таблицы (далее - СТ), из которой изымается информация для поля
#pkey - имя столбца, в котором содержится primary key СТ
#pkey_idx - индекс столбца, в котором содержится primary key СТ
#column - служебное имя столбца СТ, из которого изымается информация для отображения в поле (если у данного поля нет делегирования - это столбец ПТ и он =  column_m, если есть делегирование - это имя столбца ВТ, изкоторого изымаются подстановочные данные)
#type - тип поля (spin - для primary key, combo - для подстановочных полей, date - для полей ввода/вывода даты, edit - для остальных полей)
#wid - cловарь, в который будет записываться объект поля
class MapperField():
    def __init__(self, column_map: str, index_map: int, lable: str, table: str, pkey: str, pkey_idx: int, column: str, type: str, check: str,  wid: dict, corr_import = "", corr_table = ""):
        self.column_map = column_map
        self.index_map = index_map
        self.lable = lable
        self.table =  table
        self.pkey = pkey
        self.pkey_idx = pkey_idx
        self.index_map = index_map
        self.column = column
        self.type =  type
        self.check = check
        self.wid = wid.get("obj")
        self.corr_import = corr_import
        self.corr_table = corr_table

    def __str__(self):
        return f'Объект данных {self.__class__.__name__} для столбца {self.column_map} таблицы {self.table} мэппера '

    def __repr__(self):
        return (f'{self.__class__.__name__}'
         f' (column_map: {self.column_map}, index_map: {self.index_map},'
         f' lable: {self.lable}, table: {self.table}, pkey: {self.pkey},'
         f' pkey_idx: {self.pkey_idx}, index_map: {self.index_map},'
         f' column: {self.column}, type: {self.type}, объет поля: {self.wid})')

    #Метод, который создает поля для ввода/вывода информации и записываем их объекты в значения словаря <wid>
    #1. -  <IVALIDATOR> - словарь с параметрами для настройки численного валидатора
    #2. -  <SVALIDATOR> - словарь с параметрами для настройки строкового валидатора
    #3. -  <MASK> - словарь с параметрами для настройки маски
    def create_mapper_widgets(self, IVALIDATOR = {}, SVALIDATOR = {}, MASK = {}):
        assert self.type in ("spin", "edit", "date", "combo", "calc"), (f'Задайте тип поля ввода для поля {self.column}, таблица {self.table}. Получен тип {self.type}')
        if self.type == "spin":
            widget = QSpinBox()
            widget.setDisabled(True)
            widget.setMaximum(9999)
        elif self.type in ("edit", "calc"):
            widget = QLineEdit()
            if self.column in IVALIDATOR.keys():
                validator = QIntValidator(IVALIDATOR[self.column][0], IVALIDATOR[self.column][1])
                widget.setValidator(validator)
                widget.setPlaceholderText(IVALIDATOR[self.column][2])
            elif self.column in SVALIDATOR.keys():
                #Любое количество слов, разделенных одним пробелом
                rx = QRegExp(SVALIDATOR[self.column][0])
                validator = QRegExpValidator(rx)
                widget.setValidator(validator)
                widget.setPlaceholderText(SVALIDATOR[self.column][1])
            elif self.column in MASK.keys():
                widget.setInputMask(MASK[self.column][0])
                widget.setPlaceholderText(MASK[self.column][0])
        elif self.type == "date":
            widget = QDateEdit()
            widget.setDisplayFormat('dd.MM.yyyy')
        else:
            #"combo"
            widget = QComboBox()
            widget.setPlaceholderText(f'...')
            #Устанавливаем режим редактирования (чтобы стал доступен комплитер)
            widget.setEditable(True)
            widget.completer().setCompletionMode(QCompleter.PopupCompletion)
            widget.completer().setModelSorting(QCompleter.CaseSensitivelySortedModel)
            widget.setInsertPolicy(QComboBox.NoInsert)

            if self.column == "id":
                widget.setDisabled(True)
        #Записываем объект поля в словарь объекта wid_inf в заись с ключом "obj"
        self.wid = widget
        #Конец метода <create_mapper_widgets>

    #Метод, который обновляет внешний вид полей mappera после добавления новой записи в ТВ
    def update_mapper_field(self, current_tab):
        if (self.column_map != current_tab.rel.fkey_bag) and (self.type == "combo"):
            self.wid.setPlaceholderText(f'...')
            self.wid.setCurrentIndex(-1)
        elif self.type == "date":
            self.wid.setDate(QDate(1999, 9, 9))

    #Метод, который обновляет внешний вид полей mappera после добавления новой записи в ТВ
    def fix_id_field(self, current_tab):
        if (self.column_map == current_tab.rel.fkey_bag) and (self.type == "combo"):
            self.wid.setCurrentIndex(self.wid.findText(self.wid.currentText()))

#Класс, хранящий данные о таблице вкладки для управления записями в модели данных и БД
#<filter_id> - списком prymary ключей ТВ, связанных с выбранной в основном окне записью первичной таблицы (ПТ), для которой открыто таб-окно (карточка)
#<filter_str> - строка для фльтрации модели данных ТВ по выбранной записи ПТ
#<map_list> - список объектов типа <MapperField> с данными о ТВ и о полях ввода/вывода мэппера
#<table_name> - имя ТВ
#<tab_name> - имя вкладки
# <__models> - словарь, в котором храняться объекты моделей (доступ через сеттеры и геттеры):
# <__models["data"]>(self.data_model) - объект модели данных для таблицы вкладки
# <__model["sel"]>(self.sel_model) - объект модели выбора для таблицы вкладки
# <__models["mapper"]>(self.mapper_model) - объект модели мэппера для вкладки
# <__models["form"]>(self.form_model)
# -объект модели формы для вкладки
class TabModels(ServiseModel):
    def __init__(self, models: dict, relfield, filter_id: list, map_list: list, table_name: str, tab_name: str, permissions: tuple, filter_str: str):
        self.__models = models
        self.rel = relfield
        self.filter_id = filter_id
        self.map_list = map_list
        self.table_name =  table_name
        self.tab_name = tab_name
        self.permissions = permissions
        self.filter_str = filter_str
        logger.debug(f"Создана модель манипуляции для таб-окна первичной таблицы {self.table_name}")

    def __str__(self):
        return f'Объект данных {self.__class__.__name__} для моделей таблицы {self.table_name} вкладки {self.tab_name} '

    def __repr__(self):
        return (f'{self.__class__.__name__}'
        f' (tab_name: {self.tab_name}, table_name: {self.table_name},'
        f' (permissions: rwe - {self.permissions},'
        f' filter_str: {self.filter_str}, filter_id: {self.filter_id},'
        f' map_list: {self.map_list}, models: {self.__models},')

    @property
    def data_model(self):
        return self.__models["data"]

    @data_model.setter
    def data_model(self, input_model):
        if type(input_model) == QSqlRelationalTableModel:
            self.__models["data"] = input_model
        else:
            raise TypeError

    @property
    def sel_model(self):
        return self.__models["sel"]

    @sel_model.setter
    def sel_model(self, input_model):
        if type(input_model) == QItemSelectionModel:
            self.__models["sel"] = input_model
        else:
            raise TypeError

    @property
    def table_model(self):
        return self.__models["table"]

    @table_model.setter
    def table_model(self, input_model):
        if type(input_model) in (CustomTableView, QTableView):
            self.__models["table"] = input_model
        else:
            raise TypeError

    @property
    def mapper_model(self):
        return self.__models["mapper"]

    @mapper_model.setter
    def mapper_model(self, input_model):
        if type(input_model) == QDataWidgetMapper:
            self.__models["mapper"] = input_model
        else:
            raise TypeError

    @property
    def form_model(self):
        return self.__models["form"]

    @form_model.setter
    def form_model(self, input_model):
        if type(input_model) == QFormLayout:
            self.__models["form"] = input_model
        else:
            raise TypeError

    @property
    def proxy_model(self):
        return self.__models["proxy"]

    @proxy_model.setter
    def proxy_model(self, input_model):
        if type(input_model) in (QSortFilterProxyModel, CustomQSortFilterProxyModel):
            self.__models["proxy"] = input_model
        else:
            raise TypeError

    @property
    def context_menu_model(self):
        return self.__models["context_menu_model"]

    @context_menu_model.setter
    def context_menu_model(self, input_model):
        if type(input_model) == QMenu:
            self.__models["context_menu_model"] = input_model
        else:
            raise TypeError

    #Декоратор, который принимает от объекта таб-окна обязательные аргументы:
    #объект класса <TabModels> (current_tab), и объект класса <TabWindow> (tab_window), а также
    #необязательные аргументы: словарь с пром. моделями (prom_dict), тип файла для экспорта таблиц (where), тип экспорта (what), список млделей вкладок (tabs_list)
    #(2) пепедает в декарируемую функцию словарь с аргументами и возвращает функцию ее
    def generate_args(func):
        def wraper(*args, **kwargs):
            self = kwargs["current_tab"]
            tab_window = kwargs["tab_window"]
            arg_dict = {}
            kwargs = {**arg_dict, **kwargs}
            change_func = func(self, **kwargs)
            #print("обновление модели")
            #tab_window.inital_window.main_windows[tab_window.tab_table_attr.inital_table_name].update_data_model()
            return change_func
        return wraper

    #Метод для перемещения мэппера на запись, выбранную в таблице отображения информации на вкладке
    #1. <id> - индекс модели данных (номер строки в модели, на которую надо переключиться)
    def goto(self, id: int):
        try:
            id = int(id)
            self.mapper_model.setCurrentIndex(id)
        except:
            logger.warning("Не удалось установить новый индекс для модели мэппера")
            pass


    #Метод, который определяет id для новой записи (на 1 больше максимального из существующих)
    def generate_new_id(self, table_name, id_index, db) -> int:
        servise_model = QSqlRelationalTableModel(db = db)
        servise_model.setEditStrategy(2)
        servise_model.setTable(table_name)
        servise_model.select()
        if servise_model.query().first():
            ids = [servise_model.query().value(id_index)]
            while servise_model.query().next():
                ids.append(servise_model.query().value(id_index))
            new_id = max(ids) + 1
        else:
            print("бяда в generate_new_id")
            new_id = None
        servise_model.query().finish()
        logger.info(f"Сгенерирован pr.key для новой записи в таблице {servise_model.tableName()}, равный {new_id}")
        return new_id


    #Метод для сохранения изменений в БД, выполненных на вкладке, при нажатии кнопки Сохранить
    @generate_args
    def submit_model(self, tab_window,  **kwargs):
        #Завершаем запрос чтобы освободить БД

        try:
            print("закрываем запрос в submit_model")
            for main_window in tab_window.inital_window.main_windows.values():
                main_window.current_main.data_model.query().finish()
        except:
            pass

        #Чтобы не сбросилось значение для комбосписка мэппера фиксируем его
        for widget in self.map_list:
            widget.fix_id_field(self)
        self.mapper_model.submit()
        map_dict_type = {mapperfield.type: mapperfield.index_map for mapperfield in self.map_list}
        #Определяем номер выбранной строки (в которой происходят изменения)
        if self.sel_model.currentIndex().isValid():
            row = self.proxy_model.mapToSource(self.sel_model.currentIndex()).row()
        else: #Если ни одна запись не выбрана
            row = -1
        #Считываем текущий индекс мэппера
        index = self.mapper_model.currentIndex()
        if self.data_model.submitAll():
            if "calc" in map_dict_type.keys():
                #Заполняем full_name поля
                logger.debug("Изменения для таблицы с вычисляемым столбцом внесены в БД. Вызван метод fill_full_name дзаполнения вычисляемого столбца")
                self.fill_full_name(row)
            Inf_str = f'Изменения для таблицы {self.table_name} на вкладке "{self.tab_name}" успешно внесены в БД.'
            dialog = QMessageBox.information(tab_window, "Уведомление", Inf_str)
            logger.info(Inf_str)
            #Устанавливаем новый индекс мэппера
            self.mapper_model.setCurrentIndex(index)
            #Обновляем модели данных всех окон
            logger.debug("Изменения для таблицы внесены в БД. Вызван метод update_all_windows для обновления моделей данных во всехоткрытых окнах")
            TabModels.update_all_windows(tab_window.inital_window)
        else:
            Inf_str = f'Изменения для таблицы {self.table_name} на вкладке "{self.tab_name}" не внесены в БД. При сохранении произошла ошибка: {self.data_model.lastError().text()}'
            dialog = QMessageBox.information(tab_window, "Уведомление", Inf_str)


    #Метод для заполнения столбцов ТВ в которых храниться комплексная строка с именем документа (имя док. от дата № номер)
    def fill_full_name(self, change_row: int):
        #Если запись в таблице была выбрана
        if change_row > -1:
            map_dict = {mapperfield.column: mapperfield.index_map for mapperfield in self.map_list}
            #Определяем значения полей, которые надо внести в full_name
            name = self.data_model.record(change_row).value(map_dict.get("name", ""))
            begin = self.data_model.record(change_row).value(map_dict.get("begin", ""))
            print(begin, "begin")
            try:
                begin = str(QDate.fromString(begin, "yyyy-MM-dd").toString("dd.MM.yyyy"))
            except:
                begin = begin.toString("dd.MM.yyyy")
                print(begin, "begin")
                logger.warning("Не удалось привести формат даты к виду dd.MM.yyyy, будет использован исходный формат")
            numb = self.data_model.record(change_row).value(map_dict.get("numb", ""))
            full_name_str = f'{name} от {begin} № {numb}'
            change_record = self.data_model.record(change_row)
            change_record.setValue(map_dict["full_name"], full_name_str)
            if not self.data_model.setRecord(change_row, change_record):
                logger.warning(f"Не удалось установить значение вычисляемого столбца равным вычисленному значению {full_name_str}")
            else:
                if not self.data_model.submitAll():
                    logger.warning(f"Не удалось применить изменения, связанные с заполнением вычисляемого столбца в модель данных, к БД")
                else:
                    self.data_model.select()
                    logger.info(f"Значение вычисляемого столбца ({full_name_str}) расчитано и внесено в БД")
    """
    #Метод для отмены изменений, выполненных на вкладке при нажатии кнопки Отменить
    def revert_model(self, **kwargs):
        if self.data_model.revertAll():
            print(f'Все изменения для таблицы {self.table_name} на вкладке "{self.tab_name}" успешно отменены')
            id = self.mapper_model.currentIndex()
            self.mapper_model.toFirst()
            self.mapper_model.setCurrentIndex(id)
        else:
            print(f'Изменения для таблицы {self.table_name} на вкладке "{self.tab_name}" не отменены. При отмене произошла ошибка: {self.data_model.lastError().text()}')
    """

    #Метод для отмены фильтра по выбранной записи ПТ (entity_id)
    @generate_args
    def del_filtr(self, tab_window, **kwargs):
        filter_str = self.rel.find_str_out_null(tab_window.db)
        self.data_model.setFilter(filter_str)
        self.data_model.select()
        Inf_str = f'Фильтр успешно отключен'
        dialog = QMessageBox.information(tab_window, "Уведомление", Inf_str)
        logger.debug(Inf_str)

    #Метод для возврата фильтра по выбранной записи ПТ (entity_id)
    @generate_args
    def add_filtr(self, tab_window, **kwargs):
        self.data_model.setFilter(self.filter_str)
        self.data_model.select()
        Inf_str = f'Фильтр для таблицы успешно включен'
        dialog = QMessageBox.information(tab_window, "Уведомление", Inf_str)
        logger.debug(Inf_str)

    #Метод, который пересчитывает фильтр при изменении списка prymary key ТВ, связанных с  prymary key ПТ и перезаписывает его данные в хранилище
    def update_filter(self, db, choose_id):
        id_list = self.rel.find_id_level1(db, choose_id)
        filtr_str = self.rel.find_str_level(id_list, db)
        self.data_model.setFilter(filtr_str)
        self.data_model.select()
        logger.debug(f"В процессе обновления фильтра модели данных установлено выражение {filtr_str}")
        #Обновляем данные о фильтре в словаре
        self.filter_id = id_list
        self.filter_str = filtr_str
        self.mapper_model.toLast()

    #Метод для проверки типа связи между ПТ и ТВ и получения согласия на сохранение изменений в БД перед выполнением заппрошенной операции
    def check_type(self, tab_window):
        if self.rel.type not in ("ManyTab-ManyBag", "ManyTab-OneBag"):
            Inf_str = f'Добавление записей в этом типе вкладки (связь: {self.rel.type}) программно не предусмотрен. Откройте таблицу в индивидуальном окне'
            dialog = QMessageBox.information(tab_window, "Предупреждение", Inf_str)
            logger.info(Inf_str)
            return False
        else:
            Que_str = f'Перед выполнением запрошенной операции все изменения в таблице {self.rel.table_tab} будут сохранены в БД. Вы уверены, что хотите запустить операцию ?'
            dialog = QMessageBox.question(tab_window, "Подтверждение операции", Que_str)
            if dialog == QMessageBox.Yes:
                return True
            else:
                return False

    #Метод, который добавляет новую пустую строку в модель данных и  БД (ТВ)
    @generate_args
    def new_rec(self, tab_window, **kwargs):
        if self.check_type(tab_window):
            if self.rel.type == "ManyTab-ManyBag":
                #Считываем модель общей таблицы
                prom_model = tab_window.prom_dict[self.rel.table_prom_tab]
                logger.debug("Тип связи для активной таблицы - {ManyTab-ManyBag}, для добавления записи вызван метод new_rec_MT_MB")
                rez = self.new_rec_MT_MB(tab_window, tab_window.db, prom_model, tab_window.entity_id)
            else: #rel.type == "ManyTab-OneBag":
                logger.debug("Тип связи для активной таблицы - {ManyTab-OneBag}, для добавления записи вызван метод new_rec_MT_OB")
                rez = self.new_rec_MT_OB(tab_window, tab_window.db, tab_window.entity_id)
            if rez:
                return True
            else:
                return False

    #Подметод для случая нулевой вкладки
    def new_rec_OT_NB(self, tab_window, new_id):
        map_dict_index = {mapperfield.index_map: mapperfield.type for mapperfield in self.map_list}
        if self.rel.type == "OneTab-NoBag":
            record = self.data_model.record()
            record.setGenerated(self.rel.pkey_tab_idx, True)
            _idx_list = [idx for idx in range(0, record.count()) if idx != self.rel.pkey_tab_idx]
            for idx in _idx_list:
                #!!!!!раньше был ""
                if map_dict_index.get(idx, None) == "combo":
                    record.setValue(idx, None)
                else:
                    record.setValue(idx, None)
            record.setValue(self.rel.pkey_tab_idx, new_id)
            if not self.insert_rec(tab_window, record):
                Log_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {new_id} не доавлена в модель данных таблицы {self.rel.table_tab}. '
                logger.error(Log_str)
                return False
            else:
                Log_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {new_id} в таблицу {self.rel.table_tab} добавлена. '
                logger.info(Log_str)
                return True

    #"Подметод" методов <new_rec> и <copy_rec> для связей типа "ManyTab-OneBag" (много записей из ТВ к одной записи из ПТ)
    #1. <copy_record> - запись из копируемой строки, задается только в методе <copy_rec>
    def new_rec_MT_OB(self, tab_window, db, choose_id, copy_record = None):
        map_dict_index = {mapperfield.index_map: mapperfield.type for mapperfield in self.map_list}
        #Создаем новую запись
        record = self.data_model.record()
        #Заполнякм запись данными
        record.setGenerated(self.rel.pkey_tab_idx, True)
        # Определяем id для новой записи
        new_id = self.generate_new_id(self.table_name, self.rel.pkey_tab_idx, tab_window.db)
        # Устанавливаем расчитанное значение на место id
        record.setValue(self.rel.pkey_tab_idx, new_id)
        # Устанавливаем значение choose_id на место внешнего ключа
        record.setValue(self.rel.fkey_bag_idx, choose_id)
        #Формируе список остальных индексов столбцов
        _idx_list = [idx for idx in range(0, record.count()) if idx not in (self.rel.pkey_tab_idx,  self.rel.fkey_bag_idx)]
        if copy_record != None:
            for idx in _idx_list:
                record.setValue(idx, copy_record.value(idx))
        else:
            for idx in _idx_list:
                #!!!!РАньше было 0, ""
                if map_dict_index[idx] == "combo":
                    record.setValue(idx, None)
                elif map_dict_index[idx] == "calc":
                    record.setValue(idx, None)
                else:
                    record.setValue(idx, None)
        #Если запись успешно добавлена в модель
        if not self.insert_rec(tab_window, record):
            Log_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {choose_id} не добавлена в модель данных таблицы {self.rel.table_tab}.'
            logger.error(Log_str)
            return False
        else:
            Log_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {choose_id} в таблицу {self.rel.table_tab} добавлена. Внешний ключ, равный {choose_id} в таблице {self.rel.table_tab} сопоставлен с внешним ключом основной таблицы = {choose_id}. Вызваны методы update_filter, update_mapper_field, update_all_windows'
            logger.info(Log_str)
            self.update_filter(db, choose_id)
            for widget in self.map_list:
                widget.update_mapper_field(tab_window.current_tab)
            TabModels.update_all_windows(tab_window.inital_window)
        return True

    #"Подметод" методов <new_rec> и <copy_rec> для связей типа "ManyTab-ManyBag" (много записей из ТВ к многим записям из ПТ)
    #1. <copy_record> - запись из копируемой строки, задается только в методе <copy_rec>
    def new_rec_MT_MB(self, tab_window, db, prom_model, choose_id, copy_record = None):
        map_dict_index = {mapperfield.index_map: mapperfield.type for mapperfield in self.map_list}
        #Создаем новую запись
        record = self.data_model.record()
        record.setGenerated(self.rel.pkey_tab_idx, True)
        # Определяем id для новой записи
        new_id = self.generate_new_id(self.table_name, self.rel.pkey_tab_idx, tab_window.db)
        # Устанавливаем расчитанное значение на место id
        record.setValue(self.rel.pkey_tab_idx, new_id)
        # Формируе список остальных индексов столбцов
        _idx_list = [idx for idx in range(0, record.count()) if idx != self.rel.pkey_tab_idx]
        if copy_record != None:
            for idx in _idx_list:
                record.setValue(idx, copy_record.value(idx))
        else:
            for idx in _idx_list:
                #!!!! ранеьше было 0, ""
                if map_dict_index[idx] == "combo":
                    record.setValue(idx, None)
                elif map_dict_index[idx] == "calc":
                    record.setValue(idx, None)
                else:
                    record.setValue(idx, None)
        #Если запись не успешно добавлена в модель
        if not self.insert_rec(tab_window, record):
            logger.error(f"Не удалось добавить в модель данных запись с primary key:{self.rel.pkey_tab} = {new_id} ")
            return False
        else:
            #Если запись не добавлена в общую таблицу
            if not self.new_prom(choose_id, new_id, prom_model):
                logger.error(f"Не удалось добавить в модель данных общей таблицы {self.rel.table_prom_tab} запись с primary key:{self.rel.pkey_tab}")
                return False
            else:
                self.update_filter(db, choose_id)
                Log_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {new_id} в таблицу {self.rel.table_tab} добавлена. Внешний ключ, равный {new_id} в таблице {self.rel.table_prom_tab} сопоставлен с внешним ключом основной таблицы = {choose_id}. Вызван метод для обновления моделей данных всех окон'
                logger.info(Log_str)
                TabModels.update_all_windows(tab_window.inital_window)
                return True

    #"Подметод" методов <new_rec> и <copy_rec> для связей типа "ManyTab-ManyBag".
    #Создает "связывающую" запись в общей таблице
    #1.<new_item_id> - значение primary key для записи, добавленной в таблицу вкладки
    #2.<prom_model> - объект модели данных общей таблицы
    def new_prom(self, choose_id, new_item_id, prom_model):
        #Создаем и записываем новую запись в модель данных общей таблицы (id объекта = id сущности)
        ct_record = prom_model.record()
        ct_record.setGenerated(self.rel.pfkey_tab_idx, True)
        ct_record.setGenerated(self.rel.pfkey_bag_idx, True)
        ct_record.setValue(self.rel.pfkey_tab_idx, new_item_id )
        ct_record.setValue(self.rel.pfkey_bag_idx, choose_id)
        if not prom_model.insertRecord(-1, ct_record):
            Error_str = f'Не удалось записать новую строку в модель данных общей таблицы {self.rel.table_prom_tab}. Ошибка {prom_model.lastError().text()}'
            logger.error(Error_str)
            return False
        else:
            #Добавляем запись в БД
            rez = prom_model.submitAll()
            if rez:
                Log_str = f'Запись ({self.rel.pfkey_tab}: {new_item_id} - {self.rel.pfkey_bag}: {choose_id}) успешно добавлена в БД таблицы {self.rel.table_prom_tab}'
                logger.info(Log_str)
            else:
                Log_str = f'Запись ({self.rel.pfkey_tab}: {new_item_id} - {self.rel.pfkey_bag}: {choose_id}) не добавлена в БД таблицы {self.rel.table_prom_tab}. Проблемы с применением изменений модели данных в БД'
                logger.error(Log_str)
            return rez

    #Метод, который удаляет выбранную строку из модели данных вкладки и из ее таблицы в БД
    @generate_args
    def del_rec(self, tab_window, **kwargs):
        if self.check_type(tab_window):
            if self.data_model.filter() == "":
                Inf_str = f'Удаление записей c отключенным фильтром не предусмотрено. Включите фильтр'
                dialog = QMessageBox.information(tab_window, "Предупреждение", Inf_str)
                logger.warning(Inf_str)
            elif self.sel_model.currentIndex().isValid():
                row = self.proxy_model.mapToSource(self.sel_model.currentIndex()).row()
                #Определяем id прикреаляемой строки
                id1 = self.data_model.record(row).value(self.rel.pkey_tab_idx)
                if self.rel.type == "ManyTab-ManyBag":
                    #Считываем модель общей таблицы
                    prom_model = tab_window.prom_dict[self.rel.table_prom_tab]
                    logger.debug("Тип связи для активной таблицы - {ManyTab-ManyBag}, для удаления записи вызван метод del_MT_MB")
                    rez = self.del_MT_MB(tab_window.db, tab_window.entity_id, prom_model, row, id1)
                else: # rel.type == "ManyTab-OneBag":
                    logger.debug("Тип связи для активной таблицы - {ManyTab-OneBag}, для удаления записи вызван метод remoove_rec")
                    rez = self.remoove_rec(row)
                if rez:
                    Log_str = f'Запись (строка: {row + 1}, ID: {id1}) из таблицы {self.rel.table_tab} успешно удалена'
                    logger.info(Log_str)
                    TabModels.update_all_windows(tab_window.inital_window)
                    #Применяем фильтр с учетом новой записи
                    id_list = self.filter_id
                    id_list.remove(id1)
                    self.update_filter(tab_window.db, tab_window.entity_id)
                else:
                    Log_str = f'Запись (строка: {row + 1}, ID: {id1}) из таблицы {self.rel.table_tab} не удалена. Проблемы с методами del_MT_MB и(или) remoove_rec'
                    logger.info(Log_str)


    #"Подметод" метода <del_rec> для связей типа "ManyTab-ManyBag"
    #1. <row> - номер выбранной в модели данных строки
    def del_MT_MB(self, db, choose_id, prom_model, row, id1):
        prom_model.select()
        #Ищем строки в общей таблице, в которых id удоляемой записи сопоставлено id выбранного объекта
        list_row_prom = find_item_row_MM(db, self.rel.table_prom_tab, self.rel.pfkey_bag, choose_id, self.rel.pfkey_tab, id1)
        logger.debug(f"Методом find_item_row_MM cформирован список строк в общей таблице {self.rel.table_prom_tab}, , в которых id удоляемой записи сопоставлено id выбранного объекта")
        delete = self.del_prom(choose_id, id1, prom_model, list_row_prom)
        #Если не все записи успешно удалены из общей таблицы
        if delete == True:
            logger.info(f"Методом del_prom из общей таблице {self.rel.table_prom_tab} удалены строки, в которых id удоляемой записи сопоставлено id выбранного объекта. Вызывается метод remoove_rec для удаления записи из активной таблицы")
            #Удаляем выбранную запись из таблицы вкладки
            self.remoove_rec(row)
        return delete

    #"Подметод" методов <del_rec> и <unjoin_rec> для связей типа "ManyTab-ManyBag".
    #Удаляет "связывающую" запись в общей таблице
    #1.<id1> - значение primary key для удаляемой (открепляемой) из таблицы вкладки записи
    #2.<prom_model> - объект модели данных общей таблицы
    #3.<list_row_prom> - список номеров строк из общей модели, требующих удаления
    def del_prom(self, choose_id, id1, prom_model, list_row_prom):
        delete = True
        if len(list_row_prom) > 0:
            #Последовательно удаляем записи из общей таблицы
            for del_row in list_row_prom:
                if not self.remoove_rec(del_row, prom_model, self.rel.table_prom_tab):
                    delete = False
                    Inf_str = f'Запись (строка: {del_row + 1}, {self.rel.pfkey_tab}: {id1} - {self.rel.pfkey_bag}: {choose_id}) не удалена из БД таблицы {self.rel.table_prom_tab}. Проблемы с методом remoove_rec'
                    logger.warning(Inf_str)
                    return delete
                else:
                    Log_str = f'Запись (строка: {del_row + 1}, {self.rel.pfkey_tab}: {id1} - {self.rel.pfkey_bag}: {choose_id}) успешно удалена из БД таблицы {self.rel.table_prom_tab}'
                    logger.info(Log_str)
        elif list_row_prom == None:
            #Если не удалось получить инф. из общей таблицы
            Error_str = f'Не удалось проверить связанные записи в общей таблице {self.rel.table_prom_tab}.'
            logger.error(Error_str)
            delete = False
        return delete

    #Метод для создания связи между выбранной строкой в модели данных (таблице вкладки) и основным объектом
    #аргументы идентичны методу <new_rec>
    @generate_args
    def join_rec(self, tab_window, **kwargs):
        if self.check_type(tab_window):
            if self.sel_model.currentIndex().isValid():
                row = self.proxy_model.mapToSource(self.sel_model.currentIndex()).row()
                #Определяем id прикреаляемой строки
                id1 = self.data_model.record(row).value(self.rel.pkey_tab_idx)

                if self.rel.type == "ManyTab-ManyBag":
                    #Считываем модель общей таблицы
                    prom_model = tab_window.prom_dict[self.rel.table_prom_tab]
                    logger.debug("Тип связи для активной таблицы - {ManyTab-ManyBag}, для прикрепления записи вызван метод join_rec_MT_MB")
                    rez = self.join_rec_MT_MB(tab_window, tab_window.db, tab_window.entity_id, prom_model, row, id1)
                else: #rel.type == "ManyTab-OneBag":
                    logger.debug("Тип связи для активной таблицы - {ManyTab-OneBag}, для прикрепления записи вызван метод join_rec_MT_OB")
                    rez = self.join_rec_MT_OB(tab_window, tab_window.entity_id, tab_window.entity_volue, row, id1)
                if rez:
                    #Применяем фильтр с учетом новой записи
                    logger.debug("Запись успешно прикреплена. Вызваны методы update_filter и  update_all_windows для обновления фильта по объекту и моделей данных всех открытых окон")
                    id_list = self.filter_id
                    id_list.append(id1)
                    self.update_filter(tab_window.db, tab_window.entity_id)
                    TabModels.update_all_windows(tab_window.inital_window)

    #"Подметод" метода <join_rec> для связей типа "ManyTab-ManyBag"
    #1. <row> - номер выбранной в модели данных строки
    #2. <id1> - значение primary key прикрепляемой строки в таблице вкладки
    def join_rec_MT_MB(self, tab_window, db, choose_id, prom_model, row, id1):
        #Проверяем, есть ли в таблице строка, содержащая запись (id объекта - id прикрепляемой сущности)
        row_list = find_item_row_MM(db, self.rel.table_prom_tab, self.rel.pfkey_bag, choose_id, self.rel.pfkey_tab, id1)
        if row_list == None:
            Error_str = f'Произошла ошибка при проверке текущих связей, закрепленных в таблице {self.rel.table_prom}'
            logger.error(Error_str)
            return False
        elif row_list != []:
            Inf_str = f'Запрашиваемая связь уже существует (строка: {row_list}) в таблице {self.rel.table_prom_tab}'
            dialog = QMessageBox.information(tab_window, "Предупреждение", Inf_str)
            logger.warning(Inf_str)
            return False
        else:
            if self.new_prom(choose_id, id1, prom_model):
                Log_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {id1} в таблицу {self.rel.table_tab} добавлена. Внешний ключ, равный {id1} в таблице {self.rel.table_prom_tab} сопоставлен с внешним ключом основной таблицы = {choose_id}'
                logger.info(Log_str)
                return True
            else:
                Inf_str = f'Новая запись с primary key:{self.rel.pkey_tab} = {id1} в таблицу {self.rel.table_tab} не добавлена. Не удалось создать сопоставляющую запись в общей таблице {self.rel.table_prom_tab}'
                logger.warning(Inf_str)
                return False

    #"Подметод" метода <join_rec> для связей типа "ManyTab-OneBag"
    #1. <row> - номер выбранной в модели данных строки
    #2. <id1> - значение primary key прикрепляемой строки в таблице вкладки
    def join_rec_MT_OB(self, tab_window, choose_id, name, row, id1):
        #Считываем строку
        join_record = self.data_model.record(row)
        #Проверяем, что связь еще не установлена:
        if self.data_model.record(row).value(self.rel.fkey_bag_idx) == name:
            Inf_str = f'Запрашиваемая связь уже существует (запись: {row + 1}, столбец с индексом: {self.rel.fkey_bag_idx}) в таблице {self.rel.table_tab}'
            dialog = QMessageBox.information(tab_window, "Предупреждение", Inf_str)
            logger.warning(Inf_str)
            return False
        else:
            #Заменяем в строке foreygn key объекта на значение primary key (id) выбранного объекта (объекта окна)
            join_record.setValue(self.rel.fkey_bag_idx, choose_id)
            self.data_model.setRecord(row, join_record)
            if self.data_model.submitAll():
                Log_str = f'Запись в таблице {self.rel.table_tab}  (primary key = {id1}) привязана к объекту (primary key = {choose_id}) '
                logger.info(Log_str)
                return True
            else:
                Log_str = f'Запись в таблице {self.rel.table_tab}  (primary key = {id1}) не привязана к объекту (primary key = {choose_id}). Не удалось применить изменения в модели данных к БД '
                logger.warning(Log_str)
                return False


    #Метод для удаления связи между выбранной строкой в модели данных (таблице вкладки) и основным объектом
    #аргументы идентичны методу <new_rec>
    @generate_args
    def unjoin_rec(self, tab_window, **kwargs):
        if self.check_type(tab_window):
            if self.sel_model.currentIndex().isValid():
                #Определяем id открепляемой строки
                row = self.proxy_model.mapToSource(self.sel_model.currentIndex()).row()
                id1 = self.data_model.record(row).value(self.rel.pkey_tab_idx)
                if self.rel.type == "ManyTab-ManyBag":
                    #Считываем модель общей таблицы
                    prom_model = tab_window.prom_dict[self.rel.table_prom_tab]
                    logger.debug("Тип связи для активной таблицы - {ManyTab-ManyBag}, для открепления записи вызван метод unjoin_rec_MT_MB")
                    rez = self.unjoin_rec_MT_MB(tab_window, tab_window.db, tab_window.entity_id, prom_model, row, id1)
                else: #rel.type == "ManyTab-OneBag":
                    logger.debug("Тип связи для активной таблицы - {ManyTab-OneBag}, для открепления записи вызван метод unjoin_rec_MT_OB")
                    rez = self.unjoin_rec_MT_OB(tab_window, tab_window.entity_id, tab_window.entity_volue, row, id1)
                if rez:
                    #Применяем фильтр с учетом новой записи
                    logger.debug("Запись успешно откреплена. Вызваны методы update_filter и  update_all_windows для обновления фильта по оъекту и моделей данных всех открытых окон")
                    id_list = self.filter_id
                    id_list.remove(id1)
                    self.update_filter(tab_window.db, tab_window.entity_id)
                    TabModels.update_all_windows(tab_window.inital_window)

    #"Подметод" метода <unjoin_rec> для связей типа "ManyTab-ManyBag"
    #1. <row> - номер выбранной в модели данных строки
    #2. <id1> - значение primary key открепляемой строки в таблице вкладки
    def unjoin_rec_MT_MB(self, tab_window, db, choose_id, prom_model, row, id1):
        #Проверяем, есть ли в таблице строка, содержащая запись (id объекта - id прикрепляемой сущности). Находим ее номер
        row_list = find_item_row_MM(db, self.rel.table_prom_tab, self.rel.pfkey_bag, choose_id, self.rel.pfkey_tab, id1)
        delete = self.del_prom(choose_id, id1, prom_model, row_list)
        if delete:
            Log_str = f'Связь записи ({row + 1}, ID: {id1}) с объектом разорвана. Запись: {row_list[0] + 1}: "{self.rel.pfkey_bag} = {choose_id} - {self.rel.pfkey_tab} = {id1}" из модели таблицы {self.rel.table_prom_tab} удалена'
            logger.info(Log_str)
            return True
        else:
            Log_str = f'Не удалось разорвать вязь записи ({row + 1}, ID: {id1}) с объектом. Запись: {row_list[0] + 1}: "{self.rel.pfkey_bag} = {choose_id} - {self.rel.pfkey_tab} = {id1}" из модели таблицы {self.rel.table_prom_tab} не удалена'
            logger.warning(Log_str)
            return False

    #"Подметод" метода <unjoin_rec> для связей типа "ManyTab-OneBag"
    #1. <row> - номер выбранной в модели данных строки
    #2. <id1> - значение primary key открепляемой строки в таблице вкладки
    #остальные аргументы идентичны основному методу
    def unjoin_rec_MT_OB(self, tab_window, choose_id, name, row, id1):
        #Считываем строку
        unjoin_record = self.data_model.record(row)
        #Проверяем, что связь существует:
        if self.data_model.record(row).value(self.rel.fkey_bag_idx) != name:
            Error_str = f'Запрашиваемая связь не существует, запись {row + 1} в таблице {self.rel.table_tab} прикреплена к объекту с именем: {self.data_model.record(row).value(self.rel.fkey_bag)}'
            logger.error(Error_str)
            return False
        else:
            #Заменяем в строке foreygn key объекта на значение primary key (id) выбранного объекта (в основной таблице)
            unjoin_record.setValue(self.rel.fkey_bag_idx, None)
            #Удаляем старую запись из модели данных таблицы вкладки
            self.data_model.select()
            if not self.data_model.removeRows(row, 1):
                Error_str = f'Запись {row + 1} с текущей связью не может быть удалена из модели БД. Ошибка: {self.data_model.lastError().text()}'
                logger.error(Error_str)
            else:
                if self.insert_rec(tab_window, unjoin_record):
                    Log_str = f'Запись {row + 1} в таблице {self.rel.table_tab}  (primary key = {self.rel.pkey_tab}) откреплена от объекта (primary key = {choose_id}) '
                    logger.info(Log_str)
                    return True
                else:
                    return False
    #Метод для копирования выбранной строки в модели данных (таблице вкладки)
    #аргументы идентичны методу <new_rec>
    @generate_args
    def copy_rec(self, tab_window, **kwargs):
        if self.check_type(tab_window):
            if self.sel_model.currentIndex().isValid():
                row = self.proxy_model.mapToSource(self.sel_model.currentIndex()).row()
                #Определяем id прикреаляемой строки
                #id1 = self.data_model.record(row).value(self.rel.pkey_tab_idx)
                if self.rel.type == "ManyTab-ManyBag":
                    #Считываем модель общей таблицы
                    prom_model = tab_window.prom_dict[self.rel.table_prom_tab]
                    logger.debug("Тип связи для активной таблицы - {ManyTab-ManyBag}, для копирования записи вызван метод copy_rec_MT_MB")
                    rez = self.copy_rec_MT_MB(tab_window, tab_window.db, tab_window.entity_id, prom_model, row)
                else: # rel.type == "ManyTab-OneBag":
                    logger.debug("Тип связи для активной таблицы - {ManyTab-OneBag}, для копирования записи вызван метод copy_rec_MT_OB")
                    rez = self.copy_rec_MT_OB(tab_window, tab_window.db, tab_window.entity_id, row)
                if rez:
                    logger.debug("Копирование завершено успешно. Вызван метод update_all_windows для обновления моделей данных всех окон")
                    TabModels.update_all_windows(tab_window.inital_window)
                else:
                    logger.error("Копирование не выполнено. Проблемы с методами copy_rec_MT_OB, copy_rec_MT_MB")


    #"Подметод" метода <copy_rec> для связей типа "ManyTab-OneBag"
    #1. <row> - номер выбранной в модели данных строки
    def copy_rec_MT_OB(self, tab_window, db, choose_id: int, row: int):
        if not row:
            logger.warning(f"Некорректное значение номера копируемой строки ({row}). Копирование остановлено")
        else:
            #Считываем строку
            copy_record = self.data_model.record(row)
            #Генерируем новую запись:
            return self.new_rec_MT_OB(tab_window, db, choose_id, copy_record)


    #"Подметод" метода <copy_rec> для связей типа "ManyTab-ManyBag"
    #1. <row> - номер выбранной в модели данных строки
    def copy_rec_MT_MB(self, tab_window, db, choose_id: int, prom_model, row: int):
        if not row:
            logger.warning(f"Некорректное значение номера копируемой строки ({row}). Копирование остановлено")
        else:
            #Создаем новую запись
            copy_record = self.data_model.record(row)
            #Генерируем новую запись:
            return self.new_rec_MT_MB(tab_window, db, prom_model, choose_id, copy_record)


    #Метод, который пдготавливает все для экспорта (данные, имя файла) и запускает экспорт
    #@staticmethod
    @generate_args
    def start_export(self, tab_window, where: str, what: str, **kwargs):
        export_sets = TabModels.read_data_for_export(tab_window.tabs_list, what)
        if not export_sets:
            logger.warning("Методом read_data_for_export не удалось сформировать массивы данных для экспорта")
            pass
        else:
            logger.info("Для добавления столбца с номерами пунктов в экспортируемые таблицы вызван метод add_number_of_row")
            _ = [export_set.add_number_of_row() for export_set in export_sets]
            #Формируем имя файла
            begin_default_name = f'card ID-{tab_window.entity_id} - {what} - {QDate.currentDate().toString("dd.MM.yyyy")}'
            export_model = ExportModel(tab_window, export_sets,  where, begin_default_name, "report_cards")
            if export_model.choose_file_name():
                logger.info("Создана модель экспорта ExportModel. Запущен метод export")
                #Активируем экспорт
                export_model.export()
            else:
                pass

    #Метод, который формирует массив данных, состоящий из трех списков:
    #список с названиями вкладок для книги эксел, список со списков заголовков таблиц,
    #список со списком данных для экспортируемых таблиц
    @staticmethod
    def read_data_for_export(tabs: list, what: str):
        check_dict = {}
        #если выбран пункт меню <act_exp_all>, считываем данные из всех таблиц вкладок и записываем в <all_data>
        if what == "all":
            logger.debug("В процессе экспорта выбран пункт меню 'all'. В цикле для всех вкладок запущены методы read_header_for_export, read_table_for_export")
            export_sets = [TransportModel(tab.tab_name, tab.read_header_for_export(), tab.read_table_for_export()) for tab in tabs]
        #если выбран пункт меню <act_exp_list>, опрашиваем пользователя и считываем данные из выбранных им  таблицы вкладок и записываем в <all_data>
        elif what == "list":
            logger.debug("В процессе экспорта выбран пункт меню 'list'. Активирован CustomDialog для опроса пользователя о требующих экспорта вкладках")
            dialog = CustomDialog(tabs, check_dict)
            if dialog.exec_():
                export_sets = [TransportModel(tab.tab_name, tab.read_header_for_export(), tab.read_table_for_export()) for tab in tabs if check_dict[tab.tab_name].checkState() == 2]
            else:
                return None
        return export_sets

    #Метод, который подготавливает список с данными для заголовка таблицы
    def read_header_for_export(self):
        data_header = [wid.lable for wid in self.map_list]
        return data_header

    #Метод, который подготавливает список с данными для заголовка таблицы
    def read_column_name_for_export(self):
        column_name = [mapfield.column_map for mapfield in self.map_list]
        return column_name

    #Метод который считывает из БД данные,ткоторые надо экспортировать
    def read_table_for_export(self):
        def change_value(column, value, date_colums):
            if column in date_colums:
                try:
                    value_qdate = QDate.fromString(str(value), "yyyy-MM-dd")
                    value = value_qdate.toString("dd.MM.yyyy")
                except:
                    logger.warning("Не удалось привести формат даты к виду dd.MM.yyyy, будет использован исходный формат")
                    value = value
            return value
        date_colums = [mapfield.index_map for mapfield in self.map_list if mapfield.type == "date"]
        data_table =  []
        for row in range(0, self.data_model.rowCount()):
            record = self.data_model.record(row)
            change_data_row = [change_value(column, record.value(column), date_colums) for column in range(0, self.data_model.columnCount())]
            data_table.append(change_data_row)
        return data_table
