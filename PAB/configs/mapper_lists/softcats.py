from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 100), (1, 1150),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Категория ПО")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                 SoftCats.id, SoftCats.catigory
                 FROM SoftCats
                 WHERE  SoftCats.id > 0
            """
QUERY_STR['QPSQL7'] = """ SELECT
                 softcats.id, softcats.catigory
                 FROM softcats
                 WHERE  softcats.id > 0
            """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = ()
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {}
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
Lables("Категория...", 9, 2, 0, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (Edits(1, "Категория ...", 2, 1, 1, 1, dict = {}),)
#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = ()
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = ()
TABLE_ATTR = TabTableAttr("Категории объектов", "категория с ID: ", "softcats", "id", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"softcats":        RelField(type = "OneTab-NoBag", table_tab = "softcats", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "softcats", pkey_bag = "id", pkey_bag_idx = 0),
}
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["softcats"], table_name = "softcats", tab_name = "Категории ПО", map_list = mapper_lists["softcats"], permissions = ("r", "w", "s"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}
DOP_TABLE_WIDTHS = dict([(0, 50)])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }