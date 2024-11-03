from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 30), (1, 300), (2, 100), (3, 150), (4, 300)])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Имя АРМ", "Тип", "Отдел", "Объект", "Тип объекта")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                ARMs.id, ARMs.name, ARMs.type,
                Otdels.numb,
                GROUP_CONCAT( Assets.name || " ("  || Assets.year || ")", "; "),
                ATypes.type
                FROM ARMs
                LEFT JOIN Otdels ON ARMs.otdel_id = Otdels.id
                LEFT JOIN  Assets ON ARMs.asset_id = Assets.id
                LEFT JOIN  ATypes ON Assets.type_id = ATypes.id
                WHERE  ARMs.id > 0
                GROUP BY  ARMs.id
            """
QUERY_STR['QPSQL7'] = """ 
                SELECT
                arms.id, arms.name, arms.type,
                otdels.numb,
                string_agg(CONCAT(assets.name,' (', assets.year, ') '), ','),
                atypes.type
                FROM arms
                LEFT JOIN otdels ON arms.otdel_id = otdels.id
                LEFT JOIN  assets ON arms.asset_id = assets.id
                LEFT JOIN  atypes ON assets.type_id = atypes.id
                WHERE  arms.id > 0
                GROUP BY  arms.id, otdels.numb, atypes.type
"""
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (1,)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ( )
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
        Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
        Lables("Имя АРМ...", 9, 2, 0, 1, 1),
        Lables("Тип АРМ ...", 9, 2, 2, 1, 1),
        Lables("Отдел.. ", 9, 2, 4, 1, 1),
        Lables("Объект ...", 9, 3, 0, 1, 1),
        Lables("Тип объекта ...", 9, 3, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Имя АРМ ...", 2, 1, 1, 1, dict = {}),
        Edits(2, "Тип АРМ ...", 2, 3, 1, 1, dict = {} ),
        Edits(3, "Отдел ...", 2, 5, 1, 1, dict = {} ),
        Edits(4, "Объект ...", 3, 1, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (типы объектов)
types = ("", "ИСПДн", "ГИС", "КИИ")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(5, "Тип объекта...", "atypes", 1, types, 3, 3, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        )
TABLE_ATTR = TabTableAttr("АРМы", "АРМа №", "arms", "name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"arms":           RelField(type = "OneTab-NoBag", table_tab = "arms", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "arms", pkey_bag = "id", pkey_bag_idx = 0),
"assets":         RelField(type = "OneTab-ManyBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "arms", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "asset_id", fkey_tab_idx = 4),
"pc_softs":       RelField(type = "ManyTab-OneBag", table_tab = "pc_softs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "arm_id", fkey_bag_idx = 5, table_bag = "arms", pkey_bag = "id", pkey_bag_idx = 0),
"tehnos":         RelField(type = "ManyTab-OneBag", table_tab = "tehnos", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "arm_id", fkey_bag_idx = 7, table_bag = "arms", pkey_bag = "id", pkey_bag_idx = 0),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["arms"], table_name = "arms", tab_name = "АРМ", map_list = mapper_lists["arms"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объект", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["pc_softs"], table_name = "pc_softs", tab_name = "ПО ПК", map_list = mapper_lists["pc_softs"], permissions = ("r"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["tehnos"], table_name = "tehnos", tab_name = "ТС", map_list = mapper_lists["tehnos"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}

#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }

DOP_TABLE_WIDTHS = dict([(0, 50)])
