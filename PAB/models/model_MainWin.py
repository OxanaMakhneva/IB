 # Модуль, который будет создавать основные  окно, в которых аккумулирована информация о сущностях конкретного типа
from dataclasses import dataclass
from PyQt5.QtCore import QSize, QDate, Qt
from PyQt5.QtWidgets import QProgressBar, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QToolBar, QAction, QStatusBar, QMessageBox,  QMenu, QLineEdit, QFormLayout, QDataWidgetMapper, QComboBox, QDateEdit, QGridLayout, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate, QSqlQuery
from models.table_model_qt import CustomTableView, CustomQSortFilterProxyModel
from models.sql_model_qt import CustomSqlModel, CustomProxyModel
from models.manipulations_in_MainWin import MainWinModel
from models.relations_in_BD_qt import  find_choose_name
from models.manipulations_in_TabWin import TabModels, prom_model
from models.other_class_func import Color
from models.init_set.config_prepare import prepare
import app_logger
logger = app_logger.get_logger(__name__)

# Созданный  на основе класса QMainWindow подкласс для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self, DB_TYPE, DB_NAME, QACTIONS, LABLES, edits, combos, dates, HEADERS,
                 table_widths, QUERY_STR, NAME_COLUMS, NODISPLAY_COLUMS, DATE_COLUMS, TABLE_ATTR, map_list, **kwargs):
        super().__init__()

        #!!!!!!!!!!!!!!!!!!исправить, чтобы модно было снять
        DB_TYPE = 'QPSQL7'
        #Максимальновозможный размер окна. Будет заменен при создании окна на параметр, переданный из QAction
        self.max_width = 640
        #Ссылка на объект окна инициализации.
        self.inital_window = None
        #Флаг состояния окна ("OPEN","CLOSE")
        self.__state_window = "OPEN"
        #Словарь для хваненения объектов открытых основных окон
        self.main_windows = {}
        #Словарь для хваненения объектов открытых таб-окон
        self.tab_windows = {}
        #Список параметров мэппера первичной таблицы окна
        self.map_list = map_list
        #Список параметров для подготовки полей фильтрации типа edits,combos,dates
        self.edits = edits
        self.combos = combos
        self.dates = dates
        #Строка для запроса к БД
        self.query_str = QUERY_STR.get(DB_TYPE)
        #Словарь со значениями ширины столбцов таблицы
        self.table_widths = table_widths
        #Имя основной таблицы окна
        self.table_name = TABLE_ATTR.inital_table_name
        self.headers = HEADERS
        #Заголовок окна
        title_text = f'Основное окно - "{TABLE_ATTR.entity_lable}"'
        self.setWindowTitle(title_text)
        #Переменная для сохранения состояния нажатия кнопки фильтрации по датам
        self.dates_btn_is_ON = False
        #Cловарь для сохранения ID объектов, для которых открыты дополнительные основные окна
        self.tab_windows = {}
        #Основной слой окна
        self.layout = QVBoxLayout()

        #Подключаемся к БД
        db = QSqlDatabase(DB_TYPE)
        db.setDatabaseName(DB_NAME)

        db = QSqlDatabase('QPSQL7')
        db.setHostName('localhost')
        db.setDatabaseName('test12')
        db.setUserName('postgres')
        db.setPassword('z-123456')
        db.open()
        self.db = db
        """
        #Параметры БД
        self.db = db
        self.db_type = DB_TYPE
        self.db_name = DB_NAME
        """
        #Настраивам меню файл и панель инстументов
        menu = self.create_file_menu(QACTIONS)
        toolbar = self.create_toolbar(QACTIONS)
        self.addToolBar(toolbar)
        #Настраиваем контексное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.context_menu = self.create_context_menu(QACTIONS)
        self.customContextMenuRequested.connect(self.raise_context_menu)
        #Создаем модель для обработки данных
        self.data_model = CustomSqlModel(NAME_COLUMS, NODISPLAY_COLUMS, DATE_COLUMS)
        #Выбираем данные для основной таблицы
        self.main_query(self.query_str)
        #Создаем модель для отображения данных и назначаем ей модель для обработки данных
        self.table_model = CustomTableView(self, self.table_widths)
        self.table_model.setModel(self.data_model)
        #Заполняем заголовки основной таблицы и настраиваем шрифт
        self.table_model.add_headers(self.data_model, self.headers)
        self.table_model.set_table_style(table_font = 10)
        self.table_model.dynamic_column_resize()
        #Создаем модель для фильтрации, назначаем ей таблицу для отображения данных
        #и источник данных
        proxy_model = CustomProxyModel(self.table_model)
        proxy_model.setSourceModel(self.data_model)
        self.table_model.setModel(proxy_model)
        self.table_model.setSortingEnabled(True)
        self.proxy_model = proxy_model
        #Создаем панель фильтрации и добавляем ее на основной слой (методом box_filter)
        self.add_box_filter(LABLES, DATE_COLUMS)
        #Создаем ярлык таблицы. Добавляем его и таблицу на основной слой (методом result_label)
        self.add_result_table(self.table_model, TABLE_ATTR.entity_lable)
        #Создаем виджет для отображения слоев
        box = QWidget()
        box.setLayout(self.layout)
        self.setCentralWidget(box)
        #Создаем модель выбора
        self.sel_model = self.table_model.selectionModel()
        #Формируем модель для манипулирования БД в главном окне
        self.current_main = MainWinModel(mainmodels = {}, window = self, db = self.db, table_name =  TABLE_ATTR.inital_table_name, headers = HEADERS, prymarykey = TABLE_ATTR.inital_prymary_name, prymaryidx = TABLE_ATTR.inital_prymary_idx)
        self.current_main.data_model = self.data_model
        self.current_main.sel_model = self.sel_model
        self.current_main.proxy_model = self.proxy_model
        logger.debug(f"Создана модель основного окна для таблицы {self.table_name}")
    #Конец метода init класса MainWindow

    #Геттер и сеттер для параметра, хранящего состояние(открыто/закрто) таб-окна
    @property
    def state_window(self):
        return self.__state_window

    @state_window.setter
    def state_window(self, input_state):
        if input_state in ("OPEN", "CLOSE"):
            self.__state_window = input_state
        else:
            raise TypeError

    #Метод, который считывает из БД данные для модели данных
    def main_query(self, query_str):
        query = QSqlQuery(db = self.db)
        query.prepare(query_str)
        #Выполняем запрос
        query.exec_()
        if query.isActive():
            self.data_model.setQuery(query)
        else:
            print(f'Проблемы с поисковым запросом: {query.lastError().text()}')
    #Конец метода main_query класса MainWindow

    #Метод, который запускает обновлерие (повторное считывние) данных для модели данных
    def update_data_model(self):
        self.main_query(self.query_str)

    #Метод, который создает ярлык основной таблицы и помещает его и таблицу на основной слой
    def add_result_table(self, table_model, TABLE_NAME):
        result_label_text = f'Результаты выборки из базы данных относительно основной таблицы - "{TABLE_NAME}"'
        result_label = QLabel(result_label_text)
        font = result_label.font()
        font.setPointSize(11)
        font.setBold(True)
        result_label.setFont(font)
        #Настраиваем основной слой окна <self.layout>. Добавляем заголовок и таблицу
        self.layout.addWidget(result_label)
        self.layout.addWidget(table_model)
        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)
        self.progress.setValue(0)
        self.progress.setVisible(False)

    #Декоратор, который формирует список параметров и передает их в функцию.
    #Используется при создании панели инструментов
    def generate_args(func):
        def wraper(*args, **kwargs):
            self = kwargs.get("window", None)
            #main_qactions = kwargs.get("main_qactions", None)
            #max_width = kwargs.get("max_width", None)
            arg_dict = {}
            kwargs = {**arg_dict, **kwargs}
            change_func = func(self, **kwargs)
            return change_func
        return wraper

    #Создает основное меню
    def create_file_menu(self, qactions_file):
        menu = self.menuBar()
        file_menu = menu.addMenu("&Новое окно")
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Открыть рабочее окно, привязанное к ...")
        actions_rw = [self.create_file_action(file_submenu, qaction, qactions_file) for qaction in qactions_file if qaction.permreq == "rw" and "file" in qaction.menu_position]
        file_submenu = file_menu.addMenu("Открыть информационное окно, привязанное к ...")
        actions_r = [self.create_file_action(file_submenu, qaction, qactions_file) for qaction in qactions_file if qaction.permreq == "r" and "file" in qaction.menu_position]
        file_submenu = file_menu.addMenu("Открыть сервисное окно, привязанное к ...")
        actions_s = [self.create_file_action(file_submenu, qaction, qactions_file) for qaction in qactions_file if qaction.permreq == "s" and "file" in qaction.menu_position]
        file_menu = menu.addMenu("&Экспорт")
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Экспортировать таблицу в...")
        actions_ex = [self.create_file_action(file_submenu, qaction, qactions_file) for qaction in qactions_file if qaction.permreq == "ex" and "file" in qaction.menu_position]
        file_menu = menu.addMenu("&Импорт")
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Добавить в таблицу БД все записи из ...")
        actions_im = [self.create_file_action(file_submenu, qaction, qactions_file) for qaction in qactions_file if qaction.permreq == "im" and "file" in qaction.menu_position]
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Обновить таблицу БД данными из ...")
        actions_up = [self.create_file_action(file_submenu, qaction, qactions_file) for qaction in qactions_file if qaction.permreq == "up" and "file" in qaction.menu_position]
        logger.debug(f"Создано файл-меню")
        return menu

    #Создает "действия" для основного меню
    def create_file_action(self, file_submenu, action_params, qactions_file):
        action = QAction(QIcon(action_params.icon), action_params.name, self)
        action.setStatusTip(action_params.about)
        action.triggered.connect(lambda state_act: action_params.func_obj(window = self, main_qactions = qactions_file, max_width = self.max_width, **action_params.func_kwargs))
        file_submenu.addAction(action)
        logger.debug(f"Созданы команды для файл-меню")
        return action

    #Создает панель управления
    def create_toolbar(self, qactions_tool):
        toolbar = QToolBar("Панель инструментов")
        toolbar.setIconSize(QSize(16, 16))
        actions = [self.create_tool_action(toolbar, qaction) for qaction in qactions_tool if "tool" in qaction.menu_position]
        self.setStatusBar(QStatusBar(self))
        logger.debug(f"Создана панель управления")
        return toolbar

    #Создает "действия" для панели управления
    def create_tool_action(self, toolbar, action_params):
        action = QAction(QIcon(action_params.icon), action_params.name, self)
        action.setStatusTip(action_params.about)
        action.triggered.connect(lambda state_act: action_params.func_obj(window = self, **action_params.func_kwargs))
        action.setCheckable(action_params.chekable_status)
        action.setChecked(action_params.cheked_status)
        toolbar.addAction(action)
        logger.debug(f"Созданы команды для панели управления")
        return action

    #Создает контексное меню для основного меню
    def create_context_menu(self, qactions_tool):
        context_menu = QMenu(self)
        actions = [self.create_context_action(context_menu, qaction) for qaction in qactions_tool if "context" in qaction.menu_position]
        self.setStatusBar(QStatusBar(self))
        logger.debug(f"Создано контексное меню")
        return context_menu

    #Создает "действия" для контексного меню
    def create_context_action(self, context_menu, action_params):
        action = QAction(QIcon(action_params.icon), action_params.name, self)
        action.setStatusTip(action_params.about)
        action.triggered.connect(lambda state_act: action_params.func_obj(window = self, **action_params.func_kwargs))
        context_menu.addAction(action)
        logger.debug(f"Созданы команды для контексного меню")
        return action

    #Вызывает контесное меню
    def raise_context_menu(self, pos):
        if self.table_model.underMouse():
            self.context_menu.exec_(self.mapToGlobal(pos))

    #Метод, который создает панель фильтрации
    def add_box_filter(self, lables, DATE_COLUMS):
        # Создаем форму для поисковых полей
        layout_box_filter = QGridLayout()
        layout_box_filter.setSpacing(8)
        layout_box_filter.setContentsMargins(0,0,0,20)
        #Создаем и добавляем на слой отображения ярлыки и поля ввода информации
        self.set_filter_lables(layout_box_filter, lables)
        self.check_filter_config(DATE_COLUMS)
        self.set_filter_edits(layout_box_filter)
        self.set_filter_combos(layout_box_filter)
        self.set_filter_datas(layout_box_filter)
        #Добавляем слой отображения (сетка) на основной слой
        self.layout.addLayout(layout_box_filter)
        #Создаем и добавляем на слой отображения кнопки
        layout_box_buttons = self.add_box_buttons()
        self.layout.addLayout(layout_box_buttons)
        logger.debug(f"Создана панель фильтрации")
        #Конец метода box_filter класса MainWindow

    #Метод, который создает кнопки для панели фильтрации
    def add_box_buttons(self):
        # Создаем форму для кнопок
        layout_box_buttons = QGridLayout()
        layout_box_buttons.setSpacing(8)
        layout_box_buttons.setContentsMargins(0,0,0,20)
        #Кнопка для активации фильтрации по датам
        dates_check_btn = QPushButton("Применить фильтрацию по датам")
        dates_check_btn.setCheckable(True)
        dates_check_btn.setObjectName('dates_btn')
        qss = """ QPushButton#dates_btn:checked {background: red;}"""
        self.setStyleSheet(qss)
        self.dates_check_btn = dates_check_btn
        self.dates_check_btn.clicked.connect(lambda: self.date_filter_switch())
        #Кнопка для сброса всех введенных пользователем значений к значениям по улолчанию
        self.filtr_reset_btn = QPushButton("Отмена всех фильтров")
        self.filtr_reset_btn.setCheckable(True)
        self.filtr_reset_btn.clicked.connect(lambda: self.filtr_reset())
        #Добавляем кнопки на слой отображения
        layout_box_buttons.addWidget(self.filtr_reset_btn, 0, 0, 1, 2)
        layout_box_buttons.addWidget(self.dates_check_btn,  0, 2, 1, 2)
        logger.debug(f"Созданы кнопки для панели фильтрации")
        return layout_box_buttons

    #Метод, который управляет состоянием фильтрации по датам.
    def date_filter_switch(self):
        if self.dates_btn_is_ON == True:
            self.filtr_reset(True)
            self.dates_btn_is_ON = False
            self.dates_check_btn.setText("Применить фильтрацию по датам")
        else:
            self.dates_btn_is_ON = True
            self.start_filter()
            self.dates_check_btn.setText("Отменить фильтрацию по датам")
        self.dates_check_btn.setChecked(self.dates_btn_is_ON)

    #Метод, который проверяет корректность данных, к которым привязаны поля фильтрации
    def check_filter_config(self, date_colums):
        #Проверыем данные для фильтрации по датам
        assert {date.table_column for date in self.dates}.issubset(set(date_colums.keys())), ("Не все поля фильтра ссылаются на столбцы, содержащие даты. Откорректируйте кортеж DATES")
        borders = [date.border for date in self.dates]
        assert set(borders[::2]).issubset({0 for _ in date_colums}), ("Левая граница для поля фильтра имеет некорректное значение, ожидается int: 0. Откорректируйте кортеж DATES")
        assert set(borders[1::2]).issubset({1 for _ in date_colums}), ("Правая граница для поля фильтра имеет некорректное значение, ожидается int: 1. Откорректируйте кортеж DATES")
        #Проверяем данные для фильтрации по текстам
        edit_list = {edit.table_column for edit in self.edits}
        combo_list = {combo.table_column for combo in self.combos}
        assert {edit.table_column for edit in self.edits}.isdisjoint(date_colums.keys()), ("В списке полей фильтра по полям типа edit присутствует ссылка на столбец(цы) с датами. Откорректируйте кортеж EDITS")
        assert {combo.table_column for combo in self.combos}.isdisjoint(date_colums.keys()), ("В списке полей фильтра по полям типа combobox присутствует ссылка на столбец(цы) с датами. Откорректируйте кортеж COMBOS")

    #Метод, который создает ярлыки для панели фильтрации
    def set_filter_lables(self, layout_box_filter, lables):
        for lable in lables:
            #Создаем объект
            lbl = QLabel(f'{lable.text}')
            lbl.hasScaledContents()
            font = lbl.font()
            font.setPointSize(lable.font_size)
            #font.setBold(True)
            lbl.setFont(font)
            #Добавляем объект на слой отображения
            layout_box_filter.addWidget(lbl, lable.row, lable.col, lable.nrow, lable.ncol, Qt.Alignment(0))
            logger.debug(f"Созданы ярлыки для панели фильтрации")
    #Конец метода set_filter_lables класса MainWindow

    #Метод, который создает поля типа <QLineEdit> для панели фильтрации
    def set_filter_edits(self, layout_box_filter):
        for edit in self.edits:
            #Создаем объект
            edit_obj = QLineEdit()
            edit_obj.setPlaceholderText(f'{edit.def_text}')
            edit_obj.textChanged.connect(lambda: self.start_filter())
            #Добавляем объект на слой отображения
            layout_box_filter.addWidget(edit_obj, edit.row, edit.col, edit.nrow, edit.ncol, Qt.Alignment(0))
            #Добавляем объект в список словаря на последнюю позицию
            edit.dict["obj"] = edit_obj
            logger.debug(f"Созданы поля ввода для панели фильтрации")
    #Конец метода set_filter_edits класса MainWindow

    #Метод, который считываем наполнение сервисной таблицы для поля типа <QComboBox> для панели фильтрации
    def read_list_combos(self, table, column_idx, def_list_for_combo):
        if not table or not column_idx:
            items = def_list_for_combo
        else:
            servise_model = QSqlRelationalTableModel(db = self.db)
            servise_model.setEditStrategy(2)
            servise_model.setTable(table)
            servise_model.select()
            items = ["",]
            if servise_model.query().first():
                items.append(servise_model.query().value(column_idx))
                while servise_model.query().next():
                    items.append(servise_model.query().value(column_idx))
            else:
                items = def_list_for_combo
            servise_model.query().finish()
        return items

    #Метод, который создает поля типа <QComboBox> для панели фильтрации
    def set_filter_combos(self, layout_box_filter):
        for combo in self.combos:
            #Считываем список длякомбобокса
            list_for_combo = self.read_list_combos(combo.table_for_combo, combo.column_for_combo, combo.def_list)
            #Создаем объект
            combo_obj = QComboBox()
            combo_obj.setPlaceholderText(f'{combo.def_text}')
            combo_obj.addItems(list_for_combo)
            combo_obj.currentTextChanged.connect(lambda: self.start_filter())
            #Добавляем объект на слой отображения
            layout_box_filter.addWidget(combo_obj, combo.row, combo.col, combo.nrow, combo.ncol, Qt.Alignment(0))
            #Добавляем объект в список словаря на последнюю позицию
            combo.dict["obj"] = combo_obj
            logger.debug(f"Созданы выпадающие списки для панели фильтрации")
    #Конец метода set_filter_combos класса MainWindow

    #Метод, который создает поля типа <QDateEdit> для панели фильтрации
    def set_filter_datas(self, layout_box_filter):
        for date in self.dates:
            #Создаем объект
            date_obj = QDateEdit(QDate.currentDate().addYears(date.offset))
            date_obj.dateChanged.connect(lambda: self.start_filter())
            #Добавляем объект на слой отображения
            layout_box_filter.addWidget(date_obj, date.row, date.col, date.nrow, date.ncol, Qt.Alignment(0))
            #Добавляем объект в список словаря на последнюю позицию
            date.dict["obj"] = date_obj
            logger.debug(f"Созданы поля дат для панели фильтрации")
    #Конец метода set_filter_datas класса MainWindow

    #Метод, который передает в прокси-модель значения набранных параметров фильтрации
    #и вызывает фильтрацию
    def start_filter(self):
        if self.dates_btn_is_ON == True:
            self.proxy_model.set_texts(self.edits, self.combos)
            self.proxy_model.set_dates(self.dates)
        else:
            self.proxy_model.set_texts(self.edits, self.combos)
        self.proxy_model.invalidateFilter()

    #Метод для сброса всех введенных в полях фильтрации значений к  значениям по улолчанию
    def filtr_reset(self, old_dates_btn_is_ON = None):
        if old_dates_btn_is_ON == True:
            for date in self.dates:
                date.dict["obj"].setDate(QDate.currentDate().addYears(date.offset))
                self.proxy_model.dates = {}
                self.proxy_model.invalidateFilter()
        else:
            self.dates_btn_is_ON = False
            self.dates_check_btn.setChecked(self.dates_btn_is_ON)
            self.dates_check_btn.setText("Применить фильтрацию по датам")
            for edit in self.edits:
                edit.dict["obj"].clear()
            for combo in self.combos:
                combo.dict["obj"].setCurrentIndex (-1)
            for date in self.dates:
                date.dict["obj"].setDate(QDate.currentDate().addYears(date.offset))
            self.proxy_model.texts = {}
            self.proxy_model.dates = {}
            self.proxy_model.invalidateFilter()
            self.filtr_reset_btn.setChecked(False)
    #Конец метода filtr_reset класса MainWindow

    #Метод, который управляет процессом создания новой записи, активированным из основного окна
    @generate_args
    def new_rec_window(self, **kwargs):
        logger.debug("Вызван метод new_rec_id для определения(генерирования) pr.key для новой записи")
        new_id = self.current_main.new_rec_id(window = self)
        #Новая запись записывается в модель данных и в бд при создании окна (метод new_rec_OT_NB)
        logger.debug("Вызван метод open_tab_window для создания новой записи и открытия для нее таб-окна")
        TabWindow.open_tab_window(self.inital_window, self.current_main, new_id, is_new_record = True)

    #Метод, который открывает основное окно
    @generate_args
    def open_main_window(self, config_module_name, max_width, **kwargs):
        #Если это самое первое окно
        if not self:
            logger.debug("Создается первое основное окно. Оно фиксируется как окно инициализаци")
            new_main_window = MainWindow.create_main_window(config_module_name)
            new_main_window.inital_window = new_main_window
            new_main_window.max_width = max_width
            new_main_window.main_windows[config_module_name] = new_main_window
        else:
            #Проверяем есть ли уже такое созданное и открытое окно
            new_main_window = MainWindow.check_main_window_state(self.inital_window, config_module_name)
            #Если окно ранее не создавалось
            if not new_main_window:
                #Создаем окно
                logger.debug("Создается вторичное основное окно.")
                new_main_window = MainWindow.create_main_window(config_module_name)
                new_main_window.inital_window = self.inital_window
                new_main_window.max_width = max_width
                #Записываем объект в словарь
                self.inital_window.main_windows[config_module_name] = new_main_window
            else:
                pass
        return new_main_window

    #Метод, который открывалось ли ранее окно и окрыто ли оно сейчас
    @staticmethod
    def check_main_window_state(inital_window, table_name, **kwargs):
        #Проверяем есть ли уже такое созданное и открытое окно
        check_main_window = inital_window.main_windows.get(table_name)
        if check_main_window:
            if check_main_window.state_window == "OPEN":
                Inf_str = f'Окно для выбранного объекта открыто ранее'
                dialog = QMessageBox.information(inital_window, "Уведомление", Inf_str)
                logger.debug(Inf_str)
                check_main_window.show()
            else:
                Inf_str = f'Окно в процессе сеанса было закрыто, создаем его заново'
                dialog = QMessageBox.information(inital_window, "Уведомление", Inf_str)
                return None
                #check_main_window.state_window == "OPEN"
                #check_main_window.show()
        return check_main_window

    @staticmethod
    def create_main_window(config_module_name):
        full_GENERAL_PARAMS, full_MAIN_PARAMS, full_TAB_PARAMS = prepare(config_module_name)
        new_main_window = MainWindow(**full_GENERAL_PARAMS, **full_MAIN_PARAMS)
        new_main_window.showMaximized()
        return new_main_window

    #Метод, который открывает карточку объекта (таб-окно), запись о котором выбрана пользователем
    @generate_args
    def open_tab_window(self, choose_id = None, is_new_record = False, **kwargs):
        new_tab_window = TabWindow.open_tab_window(self.inital_window, self.current_main, choose_id, is_new_record)
        return new_tab_window

    def open_tab_window_for_del(self, choose_id = None, is_new_record = False, **kwargs):
        new_tab_window = TabWindow.open_tab_window(self.inital_window, self.current_main, choose_id, is_new_record)
        return new_tab_window

    #Метод для обработки события закрытия окна. При закрытии окна изменяем переменную
    #<self.state> чтобы родительское окно могло проверить закрыто таб-окно
    def closeEvent(self, event):
        if self == self.inital_window:
            #Присваиваем статус окна инициализации ервому окну в словаре main_windows
            self.change_inital_window()
        self.state_window = "CLOSE"
        print("Закрываем окно")
        self.current_main.data_model.query().finish()
        self.close()

    def change_inital_window(self):
        #Определяем объект нового окна инициализации.
        new_inital_win = None
        for win_name in self.main_windows.keys():
            if win_name != self.table_name:
                new_inital_win = self.main_windows[win_name]
                break
        #Нашлось окно, которое можно сделать новым первичным окном
        if new_inital_win:
            #Ссылаемся на новое окно инициализации во всех основных окнах
            for win_obj in self.main_windows.values():
                win_obj.inital_window = new_inital_win
            #Ссылаемся на новое окно инициализации во всех таб-окнах
            for win_obj in self.tab_windows.values():
                win_obj.inital_window = new_inital_win
            #Записываем в словарь нового окна инициализации объекты остальных основных и таб-окон
            new_inital_win.main_windows = self.main_windows
            new_inital_win.tab_windows = self.tab_windows
            #Затираем словарь в старом окне инициализации
            self.main_windows = {}
            self.tab_windows = {}

#Конец описания класса MainWindow
##########################################################################################################

##########################################################################################################
#Класс, хранящий инф. о первичной таблице (таблице нулевой вкладки). Используется  в
#модели таб-окна для формирования там ярлыков таблиц
@dataclass
class TabTableAttr:
    inital_lable: str           #Заголовок первичной таблицы и название нулевой вкладки
    entity_lable: str           #Заголовок(название) сущности(entity), с которой связана первичная таблица
    inital_table_name: str      #Служебное Название таблицы (название из БД)
    entity_column_name: str     #служебное Имя столбца первичной таблицы, в котором храниться entity_volue (название сущности)
    inital_prymary_name: str    #служебное Имя столбца с ключом первичной таблицы
    inital_prymary_idx: int     #Индекс столбца с ключом первичной таблицы

###Описание класса TabWindow (для моделей таб-окон)
#Класс для описания окна со вкладками с выводом информации из таблицы мэппером и таблицей
class TabWindow(QMainWindow):
    def __init__(self,  SERVISE_TABLE_PATH, DB, ENTITY_ID, is_new_record,
                 SVALIDATOR, IVALIDATOR, MASK, QACTIONS, RELS_DICT, tabs_list, prom_dict, link_dict, table_width, TAB_TABLE_ATTR, *args, **kwargs):
        super().__init__()
        #self.parent = PARENT_WINDOW         #объект основного окна, из которого вызвано таб-окно
        #Ссылка на объект окна инициализации.
        self.inital_window = None
        self.db = DB                        #идинтификатор БД
        self.entity_id = ENTITY_ID          #prymary key записи, выбранной в основном окне, для данных которой открывается таб-окно
        self.tabs_list = tabs_list
        self.prom_dict = prom_dict
        self.link_dict = link_dict
        self.table_widths = table_width
        self.svalidator = SVALIDATOR
        self.ivalidator = IVALIDATOR
        self.mask = MASK
        self.tab_table_attr = TAB_TABLE_ATTR
        self.servise_table_path = SERVISE_TABLE_PATH
        #Переменные, хранящая состояние окна
        self.__is_new_record = is_new_record        #True - окно для создаваемой записи (нет в БД), False - для ранее созданной записи (есть в БД)
        self.__state_window = "OPEN"                #OPEN - есть оккрытое окно с таким entity_id, CLOSE - окно закрыто
        #Переменная, хранящая информацио об активации автоматического обновления вкладок
        self.__state_upd = "ON"                     #ON - включено (при изменении на любой вкладке данные ересчитываются для всех вкладок, OFF - выключено)
        #Cловарь для сохранения объектов, для которых открыты дополнительные таб-окна
        self.other_tab_windows = {}
        #Заголовок окна
        title_text = f'Дополнительное окно к таблице "{self.tab_table_attr.inital_lable}"'
        self.setWindowTitle(title_text)
        #Создаем виджет для вкладок и настраиваем его
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        #Создаем модели для общих таблиц и записываем их в словарь
        prom_model(self.db, self.prom_dict)
        #Создаем вкладки
        for tab in self.tabs_list:
            self.create_tab_model(tabs, tab)
        #Настраиваем основной слой окна
        layout_all_tabs = QVBoxLayout()
        layout_all_tabs.addWidget(tabs)
        window = QWidget()
        window.setMaximumWidth(1280)
        window.setLayout(layout_all_tabs)
        self.setCentralWidget(window)
        #Настраивам меню файл
        menu = self.create_file_menu(QACTIONS)
        #Настраиваем панель инструментов. Сохраняем словарь с qactions
        (toolbar, tool_actions) = self.create_toolbar(QACTIONS)
        self.addToolBar(toolbar)
        #Создаем контексное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        (self.context_menu, context_actions) = self.create_context_menu(QACTIONS)
        self.customContextMenuRequested.connect(self.raise_context_menu)
        #Собираем словарь с объектами "действий", чтобы при переключении между вкладками блокировать те "действия", на которые нет разрешений для новой вкладки
        self.actions_dict = {**tool_actions, **context_actions}
        #При переключении вкладки передаем управление методу <change_mapper> для замены мэппера и моделей данных
        tabs.currentChanged.connect(lambda tab_idx: self.change_mapper(tab_idx, self.current_tab))
        #Переключаемся на первую вкладку
        self.change_mapper(0, self.tabs_list[0])
        logger.debug(f"Создана модель таб-окна для таблицы {self.tab_table_attr.inital_lable}")
        #Конец метода init класса <TabWindow_assets>

    #Метод, который создает объект(виджет вкладки)  для одной вкладки
    def create_tab_model(self, tabs: QTabWidget, create_tab: TabModels):
        #Создаем форму с мэппером и полями (для вкладки, у которой есть словарь). Если словаря нет, создаем для вкоадки пустой виджет
        if create_tab.map_list is None:
            tabs.addTab(Color("red"), create_tab.tab_name)
        else:
            #Cоздаем форму и записываем ее в список вкладки <tab>
            self.create_form(create_tab)
            #Считываем из списка созданную форму и мэппер
            created_form = create_tab.form_model
            created_mapper = create_tab.mapper_model
            created_sel_model = create_tab.sel_model
            #Создаем виджет, чтобы поместить в него наполнене вкладки
            tab_widget = QWidget()
            tab_widget.setLayout(created_form)
            #Создаем основной слой вкладки
            tab_btn_layot = QVBoxLayout()
            #Добавляем виджет формы на слой вкладки
            tab_btn_layot.addWidget(tab_widget)
            #Считываем из списка модель для отображения данных (таблица), настраиваем авт. подстройку ширины столбцов
            created_table_model = create_tab.table_model
            created_table_model.dynamic_column_resize()
            #Создаем заголовок (ярлык) для таблицы
            self.entity_volue = find_choose_name(self.db, self.tab_table_attr.inital_table_name, self.tab_table_attr.entity_column_name, self.tab_table_attr.inital_prymary_name, self.entity_id)
            title_lbl = QLabel(f'Все записи из категории "{create_tab.tab_name}" для выбранного {self.tab_table_attr.entity_lable} "{self.entity_volue}"')
            font = title_lbl.font()
            font.setPointSize(10)
            font.setBold(True)
            title_lbl.setFont(font)
            #Создаем виджет для навигации по мэпперу и добавляем его на слой вкладки
            goto_box = self.create_buttons_widget()
            tab_btn_layot.addWidget(goto_box)
            #Добавляем ярлык, таблицу, виджет для управления на слой вкладки
            tab_btn_layot.addWidget(title_lbl)
            tab_btn_layot.addWidget(created_table_model)
            #Создаем виджет, чтобы поместить в него итоговый слой вкладки
            tab_btn_widget = QWidget()
            tab_btn_widget.setLayout(tab_btn_layot)
            #Помещаем виджет вкладки в виджет вкладок <QTabWidget()>
            tabs.addTab(tab_btn_widget, create_tab.tab_name)
            logger.debug(f"Создана модель одной вкладки таб-окна с названием {create_tab.tab_name}")

        #Конец метода create_tab_model класса <TabWindow_assets>

    #Создает кнопки для навигации по мэпперу и сохранения изменений
    def create_buttons_widget(self):
        #Создаем слой и виджет для навигации по мэпперу
        goto_layot = QGridLayout()
        goto_layot.setSpacing(8)
        goto_layot.setContentsMargins(0,0,0,20)
        goto_box = QWidget()
        #Создаем кнопки для навигации по мэпперу
        prev_rec = QPushButton("Назад")
        prev_rec.clicked.connect(lambda: self.current_tab.mapper_model.toPrevious())
        next_rec = QPushButton("Вперед")
        next_rec.clicked.connect(lambda: self.current_tab.mapper_model.toNext())
        #Создаем кнопки для управления редактированием
        save_rec = QPushButton("Сохранить изменения на вкладке")
        save_rec.clicked.connect(lambda s: TabModels.submit_model(current_tab = self.current_tab, tab_window = self))
        revert_rec = QPushButton("Отменить изменения на вкладке")
        revert_rec.clicked.connect(lambda: self.current_tab.revert_model())
        #Добавляем кнопки на слой и виджет для навигации по мэпперу
        goto_layot.addWidget(save_rec, 0, 0, 1, 44, Qt.Alignment(0))
        goto_layot.addWidget(prev_rec, 2, 0, 1, 22, Qt.Alignment(0))
        goto_layot.addWidget(next_rec, 2, 22, 1, 22, Qt.Alignment(0))
        goto_box.setLayout(goto_layot)
        logger.debug(f"Создана панель кнопок для мэппера")
        return goto_box

    #Метод, который создает форму для вкладки с полями для ввода/вывода информации и мэппером
    def create_form(self, create_tab: TabModels):
        #Создаем форму для отображения мэппера
        create_form = QFormLayout()
        create_form.setFieldGrowthPolicy(2)
        #Создаем и настраиваем модель обработки данных
        create_data_model = QSqlRelationalTableModel(db = self.db)
        create_data_model.setEditStrategy(2) #EditStrategy { OnFieldChange, OnRowChange, OnManualSubmit }
        create_data_model.setTable(create_tab.table_name)
        create_data_model.setJoinMode(QSqlRelationalTableModel.LeftJoin)
        # Вычленяем из записей основной таблицы только те, которые соответсвуют фильтру
        create_id_list = create_tab.rel.find_id_level(self.db, self.entity_id)
        create_filtr_str = create_tab.rel.find_str_level(create_id_list, self.db)
        create_data_model.setFilter(create_filtr_str)
        #Создаем и настраиваем модель отображения данных (таблица) для отображения всех записей таблицы вкладки, связанных с выбранным объектом
        create_table_model = CustomTableView(self, self.table_widths)
        create_table_model.set_table_style(table_font = 10)
        #Вставляем заголовки в таблицу
        headers = [widget.lable for widget in create_tab.map_list]
        create_table_model.add_headers(create_data_model, headers)
        #Вставляем модель между <SQLRelationTable> и <CustomTAbleView>, чтобы
        #преобразовать отображение даты в красивый формат и сделать таблицу нередактируемой
        create_proxy_model = CustomQSortFilterProxyModel(create_table_model)
        create_proxy_model.setSourceModel(create_data_model)
        #Задаем для модели maplist чтобы знать в каких столбцах даты
        create_proxy_model.set_maplist(create_tab.map_list)
        create_table_model.setModel(create_proxy_model)
        create_table_model.setSortingEnabled(True)
        #Настраиваем модель отображения данных (мэппер)
        create_mapper = QDataWidgetMapper()
        create_mapper.setOrientation( Qt.Horizontal)
        create_mapper.setModel(create_data_model)
        create_mapper.setItemDelegate(QSqlRelationalDelegate())
        create_mapper.setSubmitPolicy(1)
        #Создаем форму отображения инф. полей. Для каждого поля в списке полей вкладки
        self.create_mapper_fields(create_tab, create_data_model, create_form, create_mapper)
        #Блокируем ввод/вывод в полях мэппера, расположенных на вкладке с запретом на запись
        self.lock_mapper_fields(create_tab)
        #При переключении вкладки передаем управление методу <change_mapper> для замены мэппера и моделей данных
        create_mapper.currentIndexChanged.connect(lambda map_idx: self.switch_mapper_fields(create_tab))
        #Создаем модель выбора
        create_sel_model = create_table_model.selectionModel()
        #Настраивам ереключение мэппера при изменении выбора строчки в таблице
        #Пересчитываем индекс прокси модели, возвращаемый моделью выбора, в индекс модели данных и передаем в метод goto значение строки, изъятое из полученного индекса
        create_sel_model.currentRowChanged.connect(lambda curent_index, curent_previos: self.current_tab.goto(self.current_tab.proxy_model.mapToSource(self.current_tab.sel_model.currentIndex()).row()))
        #Обновляем данные о фильтре в словаре
        create_tab.filter_str = create_filtr_str
        create_tab.filter_id = create_id_list
        create_data_model.select()
        #Записываем форму, модель обработки данных, мэппер и модель отображения данных (таблица)
        #в объект типа <TabModels>
        create_tab.form_model = create_form
        create_tab.data_model = create_data_model
        create_tab.mapper_model = create_mapper
        create_tab.table_model = create_table_model
        create_tab.sel_model = create_sel_model
        create_tab.proxy_model = create_proxy_model
        #Активируем запрос информации и переходим к первой записи
        create_data_model.select()
        create_mapper.toFirst()
        logger.debug(f"Создана модель формы с мэппером и табличными данными для вкладки таб-окна с названием {create_tab.tab_name}")
        #Если окно вызывается из-за создания нового объекта, иницированного в основном окне. Создам новую запись
        if self.is_new_record == True:
            logger.debug(f"Создана новая запись и пустое таб-окно {create_tab.tab_name}")
            create_tab.new_rec_OT_NB(self, self.entity_id)

    #Создает объекты для полей мэппера, параметры которых закреплены в конфиг-файле, объект MapperField
    def create_mapper_fields(self, create_tab, create_data_model, create_form, create_mapper):
        for widget in create_tab.map_list:
            #Создаем поля для ввода/вывода информации и записываем их объекты в значения словаря <widgets_dict>
            widget.create_mapper_widgets(self.ivalidator, self.svalidator, self.mask)
            #Построчно добавляем ярлык и созданное шагом ранее поле ввода/вывода (wid_inf.wid[wid_inf.column_map])
            create_form.addRow(QLabel(f'{widget.lable}'), widget.wid)
            #Добавляем в мэппер <mapper> поля ввода/вывода и ссылки на столбцы таблицы (индексы),
            create_mapper.addMapping(widget.wid, widget.index_map)
            # Если поле ввода/вывода типа <QComboBox()>, настраиваем для него подстановочную таблицу
            #и столбец в ней, откуда будет заимствоваться инф. для отображения
            if widget.type == "combo":
                #Настраиваем связи основной таблицы с зависимыми таблицами, index_map - индекс столбца основной таблицы, который надо связать с полем
                create_data_model.setRelation(widget.index_map, QSqlRelation(widget.table, widget.pkey, widget.column))
                #data_model.setRelation(widget.index_map, QSqlRelation(widget.table, widget.pkey, widget.column))
                #Создаем модель делегирования чтобы позволить основной таблице менять значение в подстановочной при изменении их в мэппере
                re_model = create_data_model.relationModel(widget.index_map)
                widget.wid.setModel(re_model)
                widget.wid.setModelColumn(re_model.fieldIndex(widget.column))
            logger.debug(f"Созданы поля мэппера для вкладки {create_tab.tab_name}")

    #Блокируем ввод/вывод в полях мэппера, расположенных на вкладке с запретом на запись (если в объекте вкладки в поле разрешений нет "w")
    def lock_mapper_fields(self, create_tab):
        if "w" not in create_tab.permissions:
            for mapfield in create_tab.map_list:
                if mapfield.type == "edit":
                    mapfield.wid.setReadOnly(True)
                else:
                    mapfield.wid.setDisabled(True)
        else:
            for mapfield in create_tab.map_list:
                if mapfield.type == "calc":
                    mapfield.wid.setReadOnly(True)
        logger.debug(f"Заблокированы ввод/вывод в полях мэппера, расположенных на вкладке с запретом на запись")

    #Метод, который при переключении вкладки считывает объект мэппера, модели и таблицы для новой вкладки и устанавливает их в окно:
    #1. - <index> - индекс новой вкладки
    #2. - <old_tab> - объект класса <TabModels> для ранее выбранной вкладки (с которой переключились)
    def change_mapper(self, index, old_tab):
    #Сохраняем изменения, внесенные в модель прошлой вкладки
    #Если в модели есть несохраненные в БД изменения
        if old_tab.data_model.isDirty():
            old_tab.data_model.submitAll()
            logger.info(f'При переключении с вкладки "{old_tab.tab_name}" все неотмененные изменения записаны в БД')
        #Обновляем списки связанных с выбранным объектом записей для каждой вкладки
        if self.state_upd == "ON":
            self.update_tabs_data()
        #Назначаем объекту окна модель обработки данных, мэппер и имя новой вкладки
        self.current_tab = self.tabs_list[index]
        #вызываем метод динамической подстройки ширины столбцов
        self.current_tab.table_model.dynamic_column_resize()
        #Блокируем поля ввода мэппера, до выбора пользоваталем какой-либо записи
        self.switch_mapper_fields(self.current_tab)
        #Настраиваем кнопки панели цправления. Отключаем те, для которых недостаточно прав
        for action, permreq in self.actions_dict.items():
            if permreq not in self.current_tab.permissions:
                action.setDisabled(True)
            else:
                action.setDisabled(False)

    #Метод блокирует поля ввода в мэпере если не выбрана запись в модели выбора.
    def switch_mapper_fields(self, current_tab):
        if "w" in current_tab.permissions:
            if current_tab.sel_model.currentIndex().isValid():
                for mapfield in current_tab.map_list:
                    mapfield.wid.setDisabled(False)
            else:
                for mapfield in current_tab.map_list:
                    mapfield.wid.setDisabled(True)

    #Создает основное меню
    def create_file_menu(self, qactions):
        menu = self.menuBar()
        file_menu = menu.addMenu("&Экспорт")
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Экспортировать данные...")
        actions = [self.create_file_action(file_submenu, qaction) for qaction in qactions if "file" in qaction.menu_position]
        return menu

    #Создает "действия" для основного меню
    def create_file_action(self, file_submenu, action_params):
        action = QAction(QIcon(action_params.icon), action_params.name, self)
        action.setStatusTip(action_params.about)
        action.triggered.connect(lambda state_act: action_params.func_obj(current_tab = self.current_tab, tab_window = self, state_act = state_act, **action_params.func_kwargs))
        file_submenu.addAction(action)
        return action

    #Метод, кторый создает панель инструментов. Возвращает объект панели и словарь
    # со всеми actions(ключи) и требованиями по правам (значения)
    def create_toolbar(self, qactions):
        toolbar = QToolBar("Панель инструментов. Подробнее об объекте")
        toolbar.setIconSize(QSize(16, 16))
        actions = {self.create_toolbar_action(toolbar, qaction): qaction.permreq for qaction in qactions if "tool" in qaction.menu_position}
        self.setStatusBar(QStatusBar(self))
        #Возвращаем словарь с объектами действий чтобы при переключении между вкладками блокировать те, на которые нет разрешений для новой вкладки
        logger.debug(f"Создана панель управления")
        return toolbar, actions

    #Метод, который создает и помещает на панель инструментов кнопки qactions на основе списка из конфига
    def create_toolbar_action(self, toolbar, action_params):
        action = QAction(QIcon(action_params.icon), action_params.name, self)
        action.setStatusTip(action_params.about)
        action.triggered.connect(lambda state_act: action_params.func_obj(current_tab = self.current_tab, tab_window = self, state_act = state_act, **action_params.func_kwargs))
        action.setCheckable(action_params.chekable_status)
        action.setChecked(action_params.cheked_status)
        toolbar.addAction(action)
        logger.debug(f"Созданы команды для панели управления")
        return action

    #Декоратор, который формирует список параметров и передает их в функцию.
    #Используется при создании панели инструментов
    def generate_args(func):
        def wraper(*args, **kwargs):
            self = kwargs["tab_window"]
            arg_dict = {}
            kwargs = {**arg_dict, **kwargs}
            change_func = func(self, **kwargs)
            return change_func
        return wraper

    #Создает контексное меню для основного меню
    def create_context_menu(self, qactions):
        context_menu = QMenu(self)
        actions = {self.create_toolbar_action(context_menu, qaction): qaction.permreq for qaction in qactions if "context" in qaction.menu_position}
        self.setStatusBar(QStatusBar(self))
        #Возвращаем словарь с объектами действий чтобы при переключении между вкладками блокировать те, на которые нет разрешений для новой вкладки
        logger.debug(f"Создано контексное меню")
        return context_menu, actions

    #Создает "действия" для контексного меню
    def create_context_action(self, context_menu, action_params):
        action = QAction(QIcon(action_params.icon), action_params.name, self)
        action.setStatusTip(action_params.about)
        action.triggered.connect(lambda state_act: action_params.func_obj(current_tab = self.current_tab, tab_window = self, state_act = state_act, **action_params.func_kwargs))
        context_menu.addAction(action)
        logger.debug(f"Созданы команды для контексного меню")
        return action

    #Вызывает контесное меню
    def raise_context_menu(self, pos):
        if self.current_tab.table_model.underMouse():
            self.context_menu.exec_(self.mapToGlobal(pos))

    #Геттер и сеттер для параметра, хранящего состояние кнопки автоматического обновления
    #(если она в состоянии ON после любого submit перерисовываются данные всех вкладок)
    @property
    def state_upd(self):
        return self.__state_upd

    @state_upd.setter
    def state_upd(self, input_state):
        if input_state in ("ON", "OFF"):
            self.__state_upd = input_state
        else:
            raise TypeError

    #Геттер и сеттер для параметра, хранящего состояние(открыто/закрто) таб-окна
    @property
    def state_window(self):
        return self.__state_window

    @state_window.setter
    def state_window(self, input_state):
        if input_state in ("OPEN", "CLOSE"):
            self.__state_window = input_state
        else:
            raise TypeError

    #Геттер и сеттер для параметра, хранящего состояние(новая запись/старая запись) таб-окна
    @property
    def is_new_record(self):
        return self.__is_new_record

    @is_new_record.setter
    def is_new_record(self, input_state):
        if input_state in ("True", "False"):
            self.__is_new_record = input_state
        else:
            raise TypeError

    #Метод, который запускает обновление вкладок
    @generate_args
    def update_tabs(self, status_act, **kwargs):
        if status_act == True:
            self.state_upd = "ON"
            self.update_tabs_data()
        else:
            self.state_upd = "OFF"

    #Метод, который пересчитывает (обновляет) данные из БД для вкладок
    def update_tabs_data(self):
        for tab in self.tabs_list:
            tab.filter_id = tab.rel.find_id_level(self.db, self.entity_id)
            tab.filter_str = tab.rel.find_str_level(tab.filter_id, self.db)
            tab.data_model.setFilter(tab.filter_str)

    #Метод для обработки события закрытия окна. При закрытии окна изменяем переменную
    #<self.state> чтобы родительское окно могло проверить закрыто таб-окно
    def closeEvent(self, event):
        self.state_window = "CLOSE"
        self.close()

    #Метод, который создает таб-окно
    @staticmethod
    def create_tab_window(config_module_name, inital_window, entity_id, is_new_record = False, **kwargs):
        #Считываем конфигурационные данные для выбранного типа основного окна и его дополнительных окон
        full_GENERAL_PARAMS, full_MAIN_PARAMS, full_TAB_PARAMS = prepare(config_module_name)
        new_tab_window = TabWindow(full_GENERAL_PARAMS["SERVISE_TABLE_PATH"], inital_window.db, entity_id, is_new_record, **full_TAB_PARAMS)
        new_tab_window.inital_window = inital_window
        #Обновляем модели данных всех окон
        inital_window.tab_windows[(config_module_name, entity_id)] = new_tab_window
        TabModels.update_all_windows(new_tab_window.inital_window)
        new_tab_window.showMaximized()
        return new_tab_window

    #Метод, который открывает таб-окно из таб-окна. Вызов в qactions
    @generate_args
    def open_window(self, current_tab, choose_id = None, is_new_record = False, **kwargs):
        TabWindow.open_tab_window(self.inital_window, self.current_tab, choose_id, is_new_record)

    #Подметод, который вызывается при вызове таб-обна из таб-окна или основного окна
    @staticmethod
    def open_tab_window(inital_window, window_model, choose_id = None, is_new_record = False, **kwargs):
        #Если открывается окно для новой записи
        if is_new_record and choose_id:
            #Создаем таб-окно для новой записи
            new_tab_window = TabWindow.create_tab_window(window_model.table_name, inital_window, choose_id, is_new_record = True)
            new_tab_window.centralWidget().setMaximumWidth(inital_window.max_width)
        else:
            choose_id, row = window_model.find_choose_row()
            #Если запись старая, а процесс определения choose_id прошел штатно
            if choose_id:
                #Проверяем есть ли уже такое созданное и открытое окно
                new_tab_window = TabWindow.check_tab_window_state(inital_window, window_model.table_name, choose_id)
                if not new_tab_window:
                    #Создаем таб-окно
                    new_tab_window = TabWindow.create_tab_window(window_model.table_name, inital_window, choose_id)
                else:
                    pass
            else:
                Inf_str = f'Перед открытием карточки нажмите в таблице на интересующий объект'
                dialog = QMessageBox.information(inital_window, "Уведомление", Inf_str)
                return None
        return new_tab_window

    #Метод, который открывалось ли ранее окно и окрыто ли оно сейчас
    @staticmethod
    def check_tab_window_state(inital_window, table_name, choose_id, **kwargs):
        #Проверяем есть ли уже такое созданное и открытое окно
        check_tab_window = inital_window.tab_windows.get((table_name, choose_id))
        if check_tab_window:
            if check_tab_window.state_window == "OPEN":
                Inf_str = f'Окно для выбранного объекта открыто ранее'
                dialog = QMessageBox.information(inital_window, "Уведомление", Inf_str)
                logger.debug(Inf_str)
            else:
                Inf_str = f'Окно для выбранного объекта закрыто в процессе работы и будет создано заново'
                dialog = QMessageBox.information(inital_window, "Уведомление", Inf_str)
                return None
                #check_tab_window.state_window == "OPEN"
                #check_tab_window.show()

        return check_tab_window
