from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Настройки для семейства окон "Аттестат"
#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 30), (1, 100), (2, 250), (3, 150), (4, 100), (5, 200), (6, 100),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Тип записи", "Имя учетной записи", "ФИО", "Номер отдела", "ОРД", "ОРД, до", "АРМ", "Название объекта")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT DISTINCT
                users.id, users.type, users.name, peoples.fio, otdels.numb,
                ords.full_name, ords.end, arms.name, assets.name
                FROM users
                LEFT JOIN ords ON ords.id = users.ord_id
                LEFT JOIN peoples ON peoples.id = users.people_id
                LEFT JOIN otdels ON otdels.id = peoples.otd_id
                LEFT JOIN arms ON arms.id = users.arm_id
                LEFT JOIN assets ON assets.id = arms.asset_id
                WHERE  users.id > 0
                GROUP BY users.id, peoples.fio, otdels.numb, ords.full_name,
				ords.end, arms.name, assets.name
            """

QUERY_STR['QPSQL7'] = """ SELECT DISTINCT
                users.id, users.type, users.name, peoples.fio, otdels.numb,
                ords.full_name, ords.end, arms.name, assets.name
                FROM users
                LEFT JOIN ords ON ords.id = users.ord_id
                LEFT JOIN peoples ON peoples.id = users.people_id
                LEFT JOIN otdels ON otdels.id = peoples.otd_id
                LEFT JOIN arms ON arms.id = users.arm_id
                LEFT JOIN assets ON assets.id = arms.asset_id
                WHERE  users.id > 0
                GROUP BY users.id, peoples.fio, otdels.numb, ords.full_name,
				ords.end, arms.name, assets.name
            """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (2)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              6:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta", None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип записи...", 9, 2, 0, 1, 1),
    Lables("Имя учетной записи ...", 9, 2, 2, 1, 1),
    Lables("ФИО ... ", 9, 2, 4, 1, 1),
    Lables("Номер отдела ...", 9, 3, 0, 1, 1),
    Lables("ОРД ...", 9, 3, 2, 1, 1),
    Lables("Объект ...", 9, 3, 4, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Тип записи ...", 2, 1, 1, 1, dict = {}),
        Edits(2, "Имя учетной записи ...", 2, 3, 1, 1, dict = {} ),
        Edits(3, "ФИО ...", 2, 5, 1, 1, dict = {} ),
        Edits(4, "Номер отдела ...", 3, 1, 1, 1, dict = {}),
        Edits(5, "ОРД ...", 3, 3, 1, 1, dict = {} ),
        Edits(7, "Объект ...", 3, 5, 1, 1, dict = {}),
        )

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = ()
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = ()

TABLE_ATTR = TabTableAttr("Учетнаые записи", "Учетной записи", "users", "name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"users":       RelField(type = "OneTab-NoBag", table_tab = "users", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "users", pkey_bag = "id", pkey_bag_idx = 0),
"peoples":     RelField(type = "OneTab-ManyBag", table_tab = "peoples", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "users", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "people_id", fkey_tab_idx = 3),
"ords":        RelField(type = "OneTab-ManyBag", table_tab = "ords", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "users", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4),
"arms":        RelField(type = "OneTab-ManyBag", table_tab = "arms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "users", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "arm_id", fkey_tab_idx = 5),
"assets":      RelField(type = "OneTab-ManyBt-OneBt-ManyBag", table_bag = "users", fkey_bt_bag = "arm_id", fkey_bt_bag_idx = 5, pkey_bag = "id", pkey_bag_idx = 0, table_bt = "arms", fkey_tab = "asset_id", fkey_tab_idx = 4,  pkey_bt = "id", pkey_bt_idx = 0),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["users"], table_name = "users", tab_name = "Учетные записи", map_list = mapper_lists["users"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["peoples"], table_name = "peoples", tab_name = "Сотрудники", map_list = mapper_lists["peoples"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["ords"], table_name = "ords", tab_name = "ОРД", map_list = mapper_lists["ords"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объекты", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["arms"], table_name = "arms", tab_name = "АРМ", map_list = mapper_lists["arms"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }