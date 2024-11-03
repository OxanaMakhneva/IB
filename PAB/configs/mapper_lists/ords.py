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
[(0, 30), (1, 100), (2, 150), (3, 250), (4, 100), (5, 100), (6, 100), (7, 100),
(8, 100), (9, 100),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Тип ОРД", "Категория события", "Название ОРД", "Номер ОРД", "Дата ОРД, от",
"Дата ОРД, до", "Инвентарный", "Пометка", "Тип объекта", "Название объекта")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                ORDs.id, OTypes.type, DDTypes.type,
                ORDs.name, ORDs.numb, ORDs.begin, ORDs.end, ORDs.inv, Secrets.type,
                GROUP_CONCAT(ATypes.type, ', '),
                GROUP_CONCAT(Assets.name, ', ')
                FROM ORDs
                LEFT JOIN OTypes ON OTypes.id = ORDs.type_id
                LEFT JOIN DDTypes ON DDTypes.id = ORDs.typeD_id
                LEFT JOIN Secrets ON Secrets.id = ORDs.secret_id
                LEFT JOIN asset_ords ON asset_ords.id_ord = ORDs.id
                LEFT JOIN  Assets ON Assets.id = asset_ords.id_asset
                LEFT JOIN ATypes ON Assets.type_id = ATypes.id
                WHERE  ORDs.id > 0
                GROUP BY ORDs.id
            """

QUERY_STR['QPSQL7'] = """ 
                SELECT DISTINCT
                ords.id, otypes.type, ddtypes.type,
                ords.name, ords.numb, ords.begin, ords.end, ords.inv, secrets.type,
				string_agg(atypes.type, ', '),
				string_agg(assets.name, ', ')
                FROM ords
                LEFT JOIN otypes ON otypes.id = ords.type_id
                LEFT JOIN ddtypes ON ddtypes.id = ords.typed_id
                LEFT JOIN secrets ON secrets.id = ords.secret_id
                LEFT JOIN asset_ords ON asset_ords.id_ord = ords.id
                LEFT JOIN  assets ON assets.id = asset_ords.id_asset
                LEFT JOIN atypes ON assets.type_id = atypes.id
                WHERE  ords.id > 0
                GROUP BY ords.id, otypes.type, ddtypes.type, secrets.type
            """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (3, 10)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              5:  DateColums(),
              6:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta", None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип ОРД...", 9, 2, 0, 1, 1),
    Lables("Категория события ...", 9, 2, 2, 1, 1),
    Lables("Тип объекта ... ", 9, 2, 4, 1, 1),
    Lables("Название ОРД ...", 9, 3, 0, 1, 1),
    Lables("Номер ОРД ...", 9, 3, 2, 1, 1),
    Lables("Инвентарный ...", 9, 3, 4, 1, 1),
    Lables("ОРД от, с ...", 9, 4, 0, 1, 1),
    Lables("ОРД от, по ...", 9, 4, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(3, "Название ОРД ...", 3, 1, 1, 1, dict = {}),
        Edits(4, "Номер ОРД ...", 3, 3, 1, 1, dict = {} ),
        Edits(7, "Инвентарный ...", 3, 5, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (типы)
types = ("", "Приказ о вводе", "Приказ об аттестации", "Приказ о классификации",
"Приказ о выводе", "Распоряжение об ответсвенных", "Распоряжение об изменении матрицы",)
atypes = ("", "ИСПДн", "ГИС", "КИИ")
kats = ("", "Периодика", "Аттестация", "Текущие процессы")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(1, "Тип ОРД...", "OTypes", 1,  types, 2, 1, 1, 1, dict = {}),
        Combos(2, "Категория события ...", "DDTypes", 1, kats, 2, 3, 1, 1, dict = {}),
        Combos(7, "Тип объекта ... ", "ATypes", 1, atypes, 2, 5, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(5, 0, -20, 4, 1, 1, 1, dict = {}),
        Dates(5, 1, 0, 4, 3, 1, 1, dict = {}),
        )

TABLE_ATTR = TabTableAttr("ОРД", "ОРД", "ords", "full_name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"ords":       RelField(type = "OneTab-NoBag", table_tab = "ords", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "ords", pkey_bag = "id", pkey_bag_idx = 0),
"assets":     RelField(type = "ManyTab-ManyBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "ords", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_ords", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_ord", pfkey_bag_idx = 1),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["ords"], table_name = "ords", tab_name = "ОРД", map_list = mapper_lists["ords"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объекты", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {"asset_ords": ""}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }