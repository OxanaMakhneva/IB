from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 30), (1, 100), (2, 250), (3, 250), (4, 60),
(5, 80), (6, 100), (7, 100), (8, 100)])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Табельный", "Должность", "ФИО", "Вн.тел.", "Форма", "Отдел, номер", "Отдел, название", "Служба", "Труд. статус")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                 Peoples.id, Peoples.card,
                 Positions.name, Peoples.fio, Peoples.tel, Forms.type,
                 Otdels.numb, Otdels.name,  Servises.numb, Truds.type
                 FROM Peoples
                 LEFT JOIN Positions ON Positions.id = Peoples.pos_id
                 LEFT JOIN Forms ON Forms.id = Peoples.form_id
                 LEFT JOIN Otdels ON Otdels.id = Peoples.otd_id
                 LEFT JOIN Servises ON Servises.id = Otdels.servise_id
                 LEFT JOIN Truds ON Truds.id = Peoples.trud_id
                 WHERE Peoples.id > 0
                 """

QUERY_STR['QPSQL7'] = """ 
              
        SELECT
                 peoples.id, peoples.card,
        CASE 
                 WHEN positions.name IS NOT NULL THEN positions.name
                 WHEN peoples.id IN (SELECT servises.boss_id FROM servises) THEN 'руководитель службы'
                 WHEN peoples.id IN (SELECT otdels.lboss_id FROM otdels) THEN 'начальник отдела'
        END,
                 peoples.fio, peoples.tel, forms.type,
        CASE
                 WHEN otdels.numb IS NOT NULL THEN otdels.numb
                 WHEN peoples.id IN (SELECT servises.boss_id FROM servises) THEN (SELECT servises.numb FROM servises WHERE servises.boss_id = peoples.id LIMIT 1)
        END,
        CASE
                 WHEN otdels.name IS NOT NULL THEN otdels.name
                 WHEN peoples.id IN (SELECT servises.boss_id FROM servises) THEN (SELECT servises.name FROM servises WHERE servises.boss_id = peoples.id LIMIT 1)
        END,
        CASE 
                 WHEN servises.numb IS NOT NULL THEN servises.numb
                 WHEN peoples.id IN (SELECT servises.boss_id FROM servises) THEN (SELECT servises.numb FROM servises WHERE servises.boss_id = peoples.id LIMIT 1)
        END,
                 truds.type
        FROM peoples
        LEFT JOIN positions ON positions.id = peoples.pos_id
        LEFT JOIN forms ON forms.id = peoples.form_id
        LEFT JOIN otdels ON otdels.id = peoples.otd_id
        LEFT JOIN servises ON servises.id = otdels.servise_id
        LEFT JOIN truds ON truds.id = peoples.trud_id
        WHERE peoples.id > 0
                 """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (7, )
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {}
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
Lables("Табельный...", 9, 2, 0, 1, 1),
Lables("Должность... ", 9, 2, 2, 1, 1),
Lables("Фамилия ... ", 9, 2, 4, 1, 1),
Lables("Отдел ...", 9, 3, 0, 1, 1),
Lables("Трудовой статус ...", 9, 3, 2, 1, 1),
Lables("Служба ...", 9, 3, 4, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Табельный ...", 2, 1, 1, 1, dict = {}),
        Edits(2, "Должность ...", 2, 3, 1, 1, dict = {} ),
        Edits(3, "Фамилия ...", 2, 5, 1, 1, dict = {} ),
        Edits(6, "Отдел ...", 3, 1, 1, 1, dict = {} ),
        Edits(8, "Служба ...", 3, 5, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (категории)
types = ("", "Работает", "Уволен", "Отпуск", "Больничный")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(9, "Трудовой статус...", "truds", 1, types, 3, 3, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = ()
TABLE_ATTR = TabTableAttr("Сотрудники", "сотрудника с ID: ", "peoples", "id", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"peoples": RelField(type = "OneTab-NoBag", table_tab = "peoples", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "peoples", pkey_bag = "id", pkey_bag_idx = 0),
"users":   RelField(type = "ManyTab-OneBag", table_tab = "users", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "people_id", fkey_bag_idx = 3, table_bag = "peoples", pkey_bag = "id", pkey_bag_idx = 0),
"responsibles":  RelField(type = "ManyTab-OneBag", table_tab = "responsibles", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "people_id", fkey_bag_idx = 3, table_bag = "peoples", pkey_bag = "id", pkey_bag_idx = 0),
"ords_user":        RelField(type = "OneTab-ManyBt-ManyBt-OneBag", table_tab = "ords", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "users", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4, table_bag = "peoples", pkey_bag = "id", pkey_bag_idx = 0, fkey_bag = "people_id", fkey_bt_bag_idx = 3),
"ords_resp":        RelField(type = "OneTab-ManyBt-ManyBt-OneBag", table_tab = "ords", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "responsibles", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4, table_bag = "peoples", pkey_bag = "id", pkey_bag_idx = 0, fkey_bag = "people_id", fkey_bt_bag_idx = 3),
}
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["peoples"], table_name = "peoples", tab_name = "Сотрудники", map_list = mapper_lists["peoples"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["users"], table_name = "users", tab_name = "Учетные записи", map_list = mapper_lists["users"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["responsibles"], table_name = "responsibles", tab_name = "Ответсвенные", map_list = mapper_lists["responsibles"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["ords_user"], table_name = "ords", tab_name = "ОРД(учетные записи)", map_list = mapper_lists["ords"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["ords_resp"], table_name = "ords", tab_name = "ОРД(ответственные)", map_list = mapper_lists["ords"], permissions = ("r", "w"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}
DOP_TABLE_WIDTHS = dict([(0, 50),])
TABLE_DOP_NAME = ("Сотрудники", "сотрудника с ID: ", "peoples", "id", "id")
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }