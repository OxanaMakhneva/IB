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
[(0, 30), (1, 150), (2, 150), (3, 250), (4, 100), (5, 100), (6, 100),
(7, 80), (8, 100),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Тип документа", "Категория события", "Название документа", "Номер", "Дата, от",
"Инвентарный", "Пометка", "Тип объекта", "Название объекта")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                Attdocs.id, DTypes.type, DDTypes.type,
                Attdocs.name, Attdocs.numb, Attdocs.begin, Attdocs.inv, Secrets.type,
                ATypes.type,
                GROUP_CONCAT(Assets.name, ', ')
                FROM Attdocs
                LEFT JOIN Secrets ON Secrets.id = Attdocs.secret_id
                LEFT JOIN DTypes ON DTypes.id = Attdocs.type_id
                LEFT JOIN DDTypes ON DDTypes.id = Attdocs.typeD_id
                LEFT JOIN asset_attdocs ON asset_attdocs.id_attdoc = Attdocs.id
                LEFT JOIN  Assets ON Assets.id = asset_attdocs.id_asset
                LEFT JOIN ATypes ON ATypes.id = Assets.type_id
                WHERE Attdocs.id > 0
                GROUP BY  Attdocs.id
            """
QUERY_STR['QPSQL7'] ="""
                SELECT 
                attdocs.id, dtypes.type, ddtypes.type,
                attdocs.name, attdocs.numb, attdocs.begin, attdocs.inv, secrets.type,
                atypes.type,
				string_agg(DISTINCT assets.name,',')
                FROM attdocs
                LEFT JOIN secrets ON secrets.id = attdocs.secret_id
                LEFT JOIN dtypes ON dtypes.id = attdocs.type_id
                LEFT JOIN ddtypes ON ddtypes.id = attdocs.typed_id
                LEFT JOIN asset_attdocs ON asset_attdocs.id_attdoc = attdocs.id
                LEFT JOIN  assets ON assets.id = asset_attdocs.id_asset
                LEFT JOIN aTypes ON atypes.id = assets.type_id
                WHERE attdocs.id > 0
                GROUP BY  attdocs.id, dtypes.type, ddtypes.type, secrets.type,
				atypes.type
                """

#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (3,)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              5:  DateColums(None, None, None, None, None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип документа...", 9, 2, 0, 1, 1),
    Lables("Категория события ...", 9, 2, 2, 1, 1),
    Lables("Тип объекта ... ", 9, 2, 4, 1, 1),
    Lables("Название документа ...", 9, 3, 0, 1, 1),
    Lables("Номер документа ...", 9, 3, 2, 1, 1),
    Lables("Инвентарный ...", 9, 3, 4, 1, 1),
    Lables("Документ от, с ...", 9, 4, 0, 1, 1),
    Lables("Документ от, по ...", 9, 4, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(3, "Название документа ...", 3, 1, 1, 1, dict = {}),
        Edits(4, "Номер документа ...", 3, 3, 1, 1, dict = {} ),
        Edits(6, "Инвентарный ...", 3, 5, 1, 1, dict = {} ),
        )

#Список значений для выпадающего списка (типы)
types = ("",)
atypes = ("", )
kats = ("", "Периодика", "Аттестация", "Текущие процессы")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(1, "Тип документа...", "dtypes", 1, types, 2, 1, 1, 1, dict = {}),
        Combos(2, "Категория события ...", "ddtypes", 1, kats, 2, 3, 1, 1, dict = {}),
        Combos(8, "Тип объекта ... ", "atypes", 1, atypes, 2, 5, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(5, 0, -20, 4, 1, 1, 1, dict = {}),
        Dates(5, 1, 0, 4, 3, 1, 1, dict = {}),
        )

TABLE_ATTR = TabTableAttr("Документы", "документа", "attdocs", "full_name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"attdocs":    RelField(type = "OneTab-NoBag", table_tab = "attdocs", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "attdocs", pkey_bag = "id", pkey_bag_idx = 0),
"assets":     RelField(type = "ManyTab-ManyBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "attdocs", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_attdocs", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_attdoc", pfkey_bag_idx = 1),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["attdocs"], table_name = "attdocs", tab_name = "Документы", map_list = mapper_lists["attdocs"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объект", map_list = mapper_lists["assets"], permissions = ("r", "w"), filter_str = "", filter_id = []),
)

#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {
            "asset_attdocs": "",
            }
DOP_TABLE_WIDTHS = dict([(0, 30), (1, 120), (2, 120), (3, 250), (4, 250), (5, 120), (6, 120), (7, 120)])
