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
[(0, 30), (1, 200), (2, 130), (3, 180), (4, 80),
(5, 80), (6, 60), (7, 80),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Наименование", "Тип ответственного", "ФИО", "Вн. тел", "Табельный", "Форма",
 "Отдел", "Труд. статус", "Объекты", "ОРД, основание")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                 Responsibles.id, Responsibles.name, RTypes.type,
                 Peoples.fio,  Peoples.tel, Peoples.card, Forms.type,
                 Otdels.numb, Truds.type,
                 GROUP_CONCAT(Assets.name, ', '),
                 ORDs.full_name
                 FROM Responsibles
                 LEFT JOIN RTypes ON RTypes.id = Responsibles.type_id
                 LEFT JOIN Peoples ON Peoples.id = Responsibles.people_id
                 LEFT JOIN Otdels ON Otdels.id = Peoples.otd_id
                 LEFT JOIN Truds ON Truds.id = Peoples.trud_id
                 LEFT JOIN Forms ON Forms.id = Peoples.form_id
                 LEFT JOIN asset_responsibles ON asset_responsibles.id_responsible = Responsibles.id
                 LEFT JOIN  Assets ON Assets.id = asset_responsibles.id_asset
                 LEFT JOIN asset_ords ON asset_ords.id_asset = Assets.id
                 LEFT JOIN  ORDs ON ORDs.id = asset_ords.id_ord
                 WHERE Responsibles.id > 0
                 GROUP BY  Responsibles.id
                 """

QUERY_STR['QPSQL7'] = """ 
                 SELECT DISTINCT
                 responsibles.id, responsibles.name, rtypes.type,
                 peoples.fio,  peoples.tel, peoples.card, forms.type,
                 otdels.numb, truds.type,
                 string_agg(assets.name, ','),
                 ords.full_name
                 FROM responsibles
                 LEFT JOIN rtypes ON rtypes.id = responsibles.type_id
                 LEFT JOIN peoples ON peoples.id = responsibles.people_id
                 LEFT JOIN otdels ON otdels.id = peoples.otd_id
                 LEFT JOIN truds ON truds.id = peoples.trud_id
                 LEFT JOIN forms ON forms.id = peoples.form_id
                 LEFT JOIN asset_responsibles ON asset_responsibles.id_responsible = responsibles.id
                 LEFT JOIN  assets ON assets.id = asset_responsibles.id_asset
                 LEFT JOIN asset_ords ON asset_ords.id_asset = assets.id
                 LEFT JOIN  ords ON ords.id = asset_ords.id_ord
                 WHERE responsibles.id > 0
                 GROUP BY  responsibles.id, rtypes.type, peoples.fio, peoples.tel, 
				 peoples.card, forms.type, otdels.numb, truds.type, ords.full_name
                 """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (1, )
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {}
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
Lables("Номер отдела...", 9, 3, 4, 1, 1),
Lables("Объект... ", 9, 2, 0, 1, 1),
Lables("Тип ответственного ... ", 9, 2, 2, 1, 1),
Lables("Фамилия ...", 9, 2, 4, 1, 1),
Lables("Номер ОРД ...", 9, 3, 0, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(9, "Объект ...", 2, 1, 1, 1, dict = {}),
        Edits(7, "Номер отдела ...", 3, 5, 1, 1, dict = {} ),
        Edits(3, "Фамилия ...", 2, 5, 1, 1, dict = {} ),
        Edits(10, "Номер ОРД ...", 3, 1, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (категории)
types = ("", "Администратор", "Администратор ИБ", "Администратор АС",
              "Ответсвенный по защите", "Секретарь","Оператор")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(2, "Тип ответственного...", "rtypes", 1, types, 2, 3, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = ()
TABLE_ATTR = TabTableAttr("Ответственные", "ответсвенного с ID: ", "responsibles", "id", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"responsibles":   RelField(type = "OneTab-NoBag", table_tab = "responsibles", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "responsibles", pkey_bag = "id", pkey_bag_idx = 0),
#"Assets":         RelField(type = "ManyTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Responsibles", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_responsibles", pfkey_tab = "id_responsible", pfkey_tab_idx = 1, pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"peoples":        RelField(type = "OneTab-ManyBag", table_tab = "peoples", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "responsibles", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "people_id", fkey_tab_idx = 3),
"ords":           RelField(type = "OneTab-ManyBag", table_tab = "ords", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "responsibles", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4),
}
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {},  relfield = RELS_DICT["responsibles"], table_name = "responsibles", tab_name = "Ответственные", map_list = mapper_lists["responsibles"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {},  relfield = RELS_DICT["peoples"], table_name = "peoples", tab_name = "Сотрудники", map_list = mapper_lists["peoples"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
TabModels(models = {},  relfield = RELS_DICT["ords"], table_name = "ords", tab_name = "ОРД", map_list = mapper_lists["ords"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {"asset_responsibles": ""}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }