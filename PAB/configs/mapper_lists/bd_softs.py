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
[(0, 100), (1, 450), (2, 120), (3, 250), (4, 100), (5, 100), (6, 100), (7, 200)])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Название", "Тип", "Категория", "Легальность", "Производитель", "Лицензия", "Списочные отделы")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                BD_Softs.id, BD_Softs.name, BD_Softs.type,
                SoftCats.catigory, BD_Softs.legality,
                BD_Softs.developer, BD_Softs.license, 
                GROUP_CONCAT(Otdels.numb, ', ')
                FROM BD_Softs
                LEFT JOIN SoftCats ON SoftCats.id = BD_Softs.catigory_id
                LEFT JOIN soft_otdels ON soft_otdels.id_soft = BD_softs.id
                LEFT JOIN Otdels ON soft_otdels.id_otdel = Otdels.id
                WHERE BD_Softs.id > 0
                GROUP BY BD_Softs.id
            """
QUERY_STR['QPSQL7'] = """ 
     SELECT DISTINCT
                bd_softs.id, bd_softs.name, bd_softs.type,
                softcats.catigory, bd_softs.legality,
                bd_softs.developer, bd_softs.license
                FROM bd_softs
                LEFT JOIN softcats ON softcats.id = bd_softs.catigory_id
                LEFT JOIN soft_otdels ON soft_otdels.id_soft = bd_softs.id
                LEFT JOIN otdels ON soft_otdels.id_otdel = otdels.id
                WHERE BD_softs.id > 0
                GROUP BY BD_softs.id, softcats.catigory
                """


#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (1, 4)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип ПО...", 9, 2, 0, 1, 1),
    Lables("Название ПО ...", 9, 2, 2, 1, 1),
    Lables("Категория ПО ... ", 9, 2, 4, 1, 1),
    Lables("Легальность ...", 9, 3, 0, 1, 1),
    Lables("Производитель ...", 9, 3, 2, 1, 1),
    Lables("Лицензия ...", 9, 3, 4, 1, 1),
            )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(2, "Тип ПО ...", 2, 1, 1, 1, dict = {}),
        Edits(1, "Название ПО ...", 2, 3, 1, 1, dict = {} ),
        Edits(3, "Категория ТС ...", 2, 5, 1, 1, dict = {} ),
        Edits(4, "Легальность ...", 3, 1, 1, 1, dict = {} ),
        Edits(5, "Производитель ...", 3, 3, 1, 1, dict = {} ),
        Edits(6, "Лицензия ...", 3, 5, 1, 1, dict = {} ),
                )

#Список значений для выпадающего списка (типы)
types = ("", "Системный блок",)

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (

        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (

        )

TABLE_ATTR = TabTableAttr("Программное обеспечение", "ПО", "bd_softs", "name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"bd_softs":    RelField(type = "OneTab-NoBag", table_tab = "bd_softs", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "bd_softs", pkey_bag = "id", pkey_bag_idx = 0),
"pc_softs":    RelField(type = "ManyTab-OneBag", table_tab = "pc_softs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "soft_id", fkey_bag_idx = 4, table_bag = "bd_softs", pkey_bag = "id", pkey_bag_idx = 0),
"otdels":      RelField(type = "ManyTab-ManyBag", table_tab = "otdels", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "bd_softs", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "soft_otdels", pfkey_tab = "id_otdel", pfkey_tab_idx = 1,  pfkey_bag = "id_soft", pfkey_bag_idx = 0),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["bd_softs"], table_name = "bd_softs", tab_name = "ПО БД", map_list = mapper_lists["bd_softs"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["pc_softs"], table_name = "pc_softs", tab_name = "ПО ПК", map_list = mapper_lists["pc_softs"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["otdels"], table_name = "otdels", tab_name = "Разрешенноые отделы", map_list = mapper_lists["otdels"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
)

#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {
"soft_otdels": "",
}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }