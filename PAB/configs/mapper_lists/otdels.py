from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 50), (1, 150), (2, 450), (3, 450), (4, 150),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Отдел, номер", "Отдел, название", "ФИО руководителя", "Служба, номер",)

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                 Otdels.id,  Otdels.numb,
                 Otdels.name, Peoples.fio,
                 Servises.numb
                 FROM Otdels
                 LEFT JOIN Peoples ON Peoples.id = Otdels.lboss_id
                 LEFT JOIN Servises ON Servises.id = Otdels.servise_id
                 WHERE Otdels.id > 0
            """
QUERY_STR['QPSQL7'] = """ SELECT
                 otdels.id,  otdels.numb,
                 otdels.name, peoples.fio,
                 servises.numb
                 FROM otdels
                 LEFT JOIN peoples ON peoples.id = otdels.lboss_id
                 LEFT JOIN servises ON servises.id = otdels.servise_id
                 WHERE otdels.id > 0
            """

#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (2, )
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {}
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 6),
Lables("Отдел, номер...", 9, 2, 0, 1, 1),
Lables("Начальник... ", 9, 2, 2, 1, 1),
Lables("Служба ... ", 9, 2, 4, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Отдел, номер ...", 2, 1, 1, 1, dict = {}),
        Edits(2, "Начальник ...", 2, 3, 1, 1, dict = {} ),
        Edits(3, "Служба ...", 2, 5, 1, 1, dict = {} ),
        )
#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = ()
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = ()
TABLE_ATTR = TabTableAttr("Отделы", "отделы с ID: ", "otdels", "id", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"otdels":        RelField(type = "OneTab-NoBag", table_tab = "otdels", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "otdels", pkey_bag = "id", pkey_bag_idx = 0),
"bd_softs":      RelField(type = "ManyTab-ManyBag", table_tab = "bd_softs", pkey_tab = "id", pkey_tab_idx = 0, table_bag = "otdels", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "soft_otdels", pfkey_tab = "id_soft", pfkey_tab_idx = 0,  pfkey_bag = "id_otdel", pfkey_bag_idx = 1),
}
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["otdels"], table_name = "otdels", tab_name = "Отделы", map_list = mapper_lists["otdels"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["bd_softs"], table_name = "bd_softs", tab_name = "ПО", map_list = mapper_lists["bd_softs"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {
"soft_otdels": "",
}
DOP_TABLE_WIDTHS = dict([(0, 50), (1, 200), (2, 200), (3, 400),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }