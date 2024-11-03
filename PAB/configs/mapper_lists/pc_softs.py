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
[(0, 30), (1, 150), (2, 120), (3, 250), (4, 100), (5, 100), (6, 100),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
 "ст-т", "ID", "Легальность", "Название (ПК)", "Версия (ПК)", "Название", "Тип", "Категория", "Производитель", "Лицензия", "ПК", "Отдел")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                CASE 
                    WHEN BD_Softs.legality LIKE '%' || "Разрешено" || '%' THEN 0
                    WHEN BD_Softs.legality LIKE '%' || "Не определено" || '%' THEN 1
                    WHEN (BD_Softs.legality LIKE '%' || "Ситуационно" || '%') AND (soft_otdels.id_otdel = Otdels.id) THEN 0
                    ELSE 2
                    END PCLegalityP,
                PC_Softs.id, 
                CASE 
                    WHEN BD_Softs.legality LIKE '%' || "Разрешено" || '%' THEN "Разрешено"
                    WHEN BD_Softs.legality LIKE '%' || "Не определено" || '%' THEN "Не определено"
                    WHEN (BD_Softs.legality LIKE '%' || "Ситуационно" || '%') AND (soft_otdels.id_otdel = Otdels.id) THEN "Разрешено (список)"
                    ELSE "Запрещено"
                    END PCLegality,
             
                      
                PC_Softs.name, PC_Softs.version,
                BD_Softs.name, BD_Softs.type,
                SoftCats.catigory,
                BD_Softs.developer, BD_Softs.license, BD_Softs.site,
                BD_Softs.wiki_page, ARMs.name, Otdels.numb
                FROM PC_Softs
                LEFT JOIN BD_Softs ON BD_Softs.id = PC_Softs.soft_id
                LEFT JOIN SoftCats ON SoftCats.id = BD_Softs.catigory_id
                LEFT JOIN ARMs ON ARMs.id = PC_Softs.arm_id
                LEFT JOIN Otdels ON Otdels.id = ARMs.otdel_id
                LEFT JOIN soft_otdels ON soft_otdels.id_soft = BD_softs.id
                WHERE PC_Softs.id > 0
                GROUP BY PC_Softs.id
            """

QUERY_STR['QPSQL7'] = """ 
                SELECT DISTINCT
CASE 
     WHEN bd_softs.legality LIKE '%Разрешено%' THEN 0
     WHEN BD_Softs.legality LIKE '%Не определено%' THEN 1
     WHEN (bd_softs.legality LIKE '%Ситуационно%') AND (soft_otdels.id_otdel = otdels.id) THEN 0
     ELSE 2
     END pc_legality_p,
     pc_softs.id, 
CASE 
     WHEN bd_softs.legality LIKE '%Разрешено%' THEN 'Разрешено'
     WHEN bd_softs.legality LIKE '%Не определено%' THEN 'Не определено'
     WHEN (bd_softs.legality LIKE '%Ситуационно%') AND (soft_otdels.id_otdel = otdels.id) THEN 'Разрешено (список)'
     ELSE 'Запрещено'
     END pc_legality,

pc_softs.name, pc_softs.version,
bd_softs.name, bd_softs.type,
softcats.catigory,
bd_softs.developer, bd_softs.license, arms.name, otdels.numb
FROM pc_softs
LEFT JOIN bd_softs ON bd_softs.id = pc_softs.soft_id
LEFT JOIN softcats ON softcats.id = bd_softs.catigory_id
LEFT JOIN arms ON arms.id = pc_softs.arm_id
LEFT JOIN otdels ON otdels.id = arms.otdel_id
LEFT JOIN soft_otdels ON soft_otdels.id_soft = bd_softs.id
WHERE pc_softs.id > 0
GROUP BY pc_softs.id, bd_softs.legality, soft_otdels.id_otdel, 
otdels.id, bd_softs.name, bd_softs.type, softcats.catigory,
bd_softs.developer, bd_softs.license,  arms.name
            """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = ()
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = (0, )
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип ПО...", 9, 2, 0, 1, 1),
    Lables("Название ПО ...", 9, 2, 2, 1, 1),
    Lables("Категория ПО ... ", 9, 2, 4, 1, 1),
    Lables("Производитель ...", 9, 3, 0, 1, 1),
    Lables("Лицензия ...", 9, 3, 2, 1, 1),
            )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(4, "Тип ПО ...", 2, 1, 1, 1, dict = {}),
        Edits(3, "Название ПО ...", 2, 3, 1, 1, dict = {} ),
        Edits(5, "Категория ТС ...", 2, 5, 1, 1, dict = {} ),
        Edits(6, "Производитель ...", 3, 1, 1, 1, dict = {} ),
        Edits(7, "Лицензия ...", 3, 3, 1, 1, dict = {} ),
                )

#Список значений для выпадающего списка (типы)
types = ("", "Системный блок",)

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (

        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (

        )

TABLE_ATTR = TabTableAttr("Программное обеспечение c ПК", "ПО с ПК", "pc_softs", "name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"pc_softs":    RelField(type = "OneTab-NoBag", table_tab = "pc_softs", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "pc_softs", pkey_bag = "id", pkey_bag_idx = 0),
"bd_softs":    RelField(type = "OneTab-ManyBag", table_tab = "bd_softs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "pc_softs", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "soft_id", fkey_tab_idx = 3),
"arms":        RelField(type = "OneTab-ManyBag", table_tab = "arms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "pc_softs", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "arm_id", fkey_tab_idx = 4),
"otdels":      RelField(type = "OneTab-ManyBt-OneBt-ManyBag",  table_tab = "otdels",  pkey_tab = "id", pkey_tab_idx = 0, table_bag = "pc_softs", fkey_bt_bag = "arm_id", fkey_bt_bag_idx = 5, pkey_bag = "id", pkey_bag_idx = 0, table_bt = "arms", fkey_tab = "otdel_id", fkey_tab_idx = 3, pkey_bt = "id", pkey_bt_idx = 0),
"assets":      RelField(type = "OneTab-ManyBt-OneBt-ManyBag",  table_tab = "assets",  pkey_tab = "id", pkey_tab_idx = 0, table_bag = "pc_softs", fkey_bt_bag = "arm_id", fkey_bt_bag_idx = 5, pkey_bag = "id", pkey_bag_idx = 0, table_bt = "arms", fkey_tab = "asset_id", fkey_tab_idx = 4, pkey_bt = "id", pkey_bt_idx = 0),

            }

#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["pc_softs"], table_name = "pc_softs", tab_name = "ПО c ПК", map_list = mapper_lists["pc_softs"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["bd_softs"], table_name = "bd_softs", tab_name = "ПО БД", map_list = mapper_lists["bd_softs"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["arms"], table_name = "arms", tab_name = "АРМ", map_list = mapper_lists["arms"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["otdels"], table_name = "otdels", tab_name = "otdels", map_list = mapper_lists["otdels"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "assets", map_list = mapper_lists["assets"], permissions = ("r", "w"), filter_str = "", filter_id = []),
)

#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }