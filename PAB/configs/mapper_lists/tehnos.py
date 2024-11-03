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
[(0, 30), (1, 150), (2, 120), (3, 250), (4, 100), (5, 100), (6, 100),
(7, 80), (8, 100), ])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Тип ТС", "Название ТС", "Модель ТС", "Номер ТС", "СЗ ТС", "Заключение",
"Заключение, от", "Заключение, №", "Заключение, инв.", "Название объекта")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                Tehnos.id, TTypes.type, Tehnos.name, Tehnos.model, Tehnos.numb, Tehnos.SZ,
                Attdocs.full_name, Attdocs.begin, Attdocs.numb, Attdocs.inv,
                GROUP_CONCAT(Assets.name, ', ')
                FROM Tehnos
                LEFT JOIN TTypes ON TTypes.id = Tehnos.type_id
                LEFT JOIN Attdocs ON Attdocs.id = Tehnos.attdoc_id
                LEFT JOIN ARMs ON ARMs.id = Tehnos.arm_id
                LEFT JOIN Assets ON Assets.id = ARMs.asset_id
                WHERE Tehnos.id > 0
                GROUP BY  Tehnos.id
            """

QUERY_STR['QPSQL7'] = """ SELECT DISTINCT
                tehnos.id, ttypes.type, tehnos.name, tehnos.model, tehnos.numb, tehnos.SZ,
                attdocs.full_name, attdocs.begin, attdocs.numb, attdocs.inv,
                string_agg(assets.name,',')
                FROM tehnos
                LEFT JOIN ttypes ON ttypes.id = tehnos.type_id
                LEFT JOIN attdocs ON attdocs.id = tehnos.attdoc_id
                LEFT JOIN arms ON arms.id = tehnos.arm_id
                LEFT JOIN assets ON assets.id = arms.asset_id
                WHERE tehnos.id > 0
                GROUP BY  tehnos.id, ttypes.type, attdocs.full_name, attdocs.begin,
				attdocs.numb, attdocs.inv
            """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (2, 3)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              7: DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta" , None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип ТС...", 9, 2, 0, 1, 1),
    Lables("Название ТС ...", 9, 2, 2, 1, 1),
    Lables("Модель ТС ... ", 9, 2, 4, 1, 1),
    Lables("Номер ТС ...", 9, 3, 0, 1, 1),
    Lables("Номер СЗ ...", 9, 3, 2, 1, 1),
    Lables("Заключение, номер ...", 9, 3, 4, 1, 1),
    Lables("Заключение, инвентарный ...", 9, 4, 0, 1, 1),
    Lables("Заключение от, с ...", 9, 5, 0, 1, 1),
    Lables("Заключение от, по ...", 9, 5, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(2, "Название ТС ...", 2, 3, 1, 1, dict = {}),
        Edits(3, "Модель ТС ...", 2, 5, 1, 1, dict = {} ),
        Edits(4, "Номер ТС ...", 3, 1, 1, 1, dict = {} ),
        Edits(5, "Номер СЗ ...", 3, 3, 1, 1, dict = {} ),
        Edits(8, "Заключение, № ...", 3, 5, 1, 1, dict = {} ),
        Edits(9, "Заключение, инв. ...", 4, 1, 1, 1, dict = {} ),
        )

#Список значений для выпадающего списка (типы)
types = ("", "Системный блок",)

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(1, "Тип ТС...", "ttypes", 1, types, 2, 1, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(7, 0, -20, 5, 1, 1, 1, dict = {}),
        Dates(7, 1, 0, 4, 5, 1, 1, dict = {}),
        )

TABLE_ATTR = TabTableAttr("Технические средства", "ТС", "tehnos", "numb", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"tehnos":    RelField(type = "OneTab-NoBag", table_tab = "tehnos", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "tehnos", pkey_bag = "id", pkey_bag_idx = 0),
"attdocs":   RelField(type = "OneTab-ManyBag", table_tab = "attdocs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "tehnos", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "attdoc_id", fkey_tab_idx = 6),
"arms":      RelField(type = "OneTab-ManyBag", table_tab = "arms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "tehnos", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "arm_id", fkey_tab_idx = 7),
"assets":    RelField(type = "OneTab-ManyBt-OneBt-ManyBag", table_tab = "assets",  pkey_tab = "id", table_bag = "tehnos", fkey_bt_bag = "arm_id", fkey_bt_bag_idx = 7, pkey_bag = "id", pkey_bag_idx = 0, table_bt = "arms", fkey_tab = "asset_id", fkey_tab_idx = 4,  pkey_bt = "id", pkey_bt_idx = 0),
"otdels":    RelField(type = "OneTab-ManyBt-OneBt-ManyBag", table_tab = "otdels",  pkey_tab = "id", table_bag = "tehnos", fkey_bt_bag = "arm_id", fkey_bt_bag_idx = 7, pkey_bag = "id", pkey_bag_idx = 0, table_bt = "arms", fkey_tab = "otdel_id", fkey_tab_idx = 3,  pkey_bt = "id", pkey_bt_idx = 0),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["tehnos"], table_name = "tehnos", tab_name = "ТС", map_list = mapper_lists["tehnos"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["attdocs"], table_name = "attdocs", tab_name = "Заключение", map_list = mapper_lists["attdocs"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["arms"], table_name = "arms", tab_name = "АРМ", map_list = mapper_lists["arms"], permissions = ("r", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объект", map_list = mapper_lists["assets"], permissions = ("r", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["otdels"], table_name = "otdels", tab_name = "Отдел", map_list = mapper_lists["otdels"], permissions = ("r", "e"), filter_str = "", filter_id = []),
)

#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }