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
[(0, 30), (1, 90), (2, 90), (3, 90), (4, 120), (5, 250), (6, 150), (7, 150),
(8, 90), (9, 200),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "№ сертификата", "Дата выдачи", "Дата окончания", "Тип СЗИ", "Наименовани СЗИ(шифр)",
"Соот. требованиям","Схема сертификации", "Окончание ТП", "Номера СЗИ")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                 Serts.id, Serts.numb, Serts.begin, Serts.end,
                 STypes.type, Serts.name, Serts.req_doc, Serts.scheme, Serts.end_tp,
                 GROUP_CONCAT("СЗИ № " || SZIs.numb || " (" || '"' || Assets.name ||'"' || ")", "; ")
                 FROM Serts
                 LEFT JOIN STypes ON STypes.id = Serts.type_id
                 LEFT JOIN SZIs ON Serts.id = SZIs.sert_id
                 LEFT JOIN asset_SZIs ON asset_SZIs.id_SZI = SZIs.id
                 LEFT JOIN  Assets ON Assets.id = asset_SZIs.id_asset
                 GROUP BY  Serts.id
                 """

QUERY_STR['QPSQL7'] = """ SELECT DISTINCT
                 serts.id, serts.numb, serts.begin, serts.end,
                 stypes.type, serts.name, serts.req_doc, serts.scheme, serts.end_tp,
                 string_agg(CONCAT('СЗИ № ', szis.numb,' (', assets.name, ') '), ',')
				 FROM serts
                 LEFT JOIN stypes ON stypes.id = serts.type_id
                 LEFT JOIN szis ON Serts.id = szis.sert_id
                 LEFT JOIN asset_szis ON asset_szis.id_szi = szis.id
                 LEFT JOIN  assets ON assets.id = asset_szis.id_asset
                 GROUP BY  serts.id, stypes.type 
                 """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (5, )
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              2:  DateColums(None, None, None, None, None),
              3:  DateColums(None, None, None, None, None),
              8:  DateColums(None, QDate.currentDate().addMonths(-6), None, "red", None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип СЗИ ...", 9, 2, 0, 1, 1),
    Lables("Название(шифр) СЗИ ...", 9, 2, 2, 1, 1),
    Lables("Схема сертификации ", 9, 3, 0, 1, 1),
    Lables("Соответствие документам ...", 9, 3, 2, 1, 1),
    Lables("Окончание срока, с ...", 9, 6, 0, 1, 1),
    Lables("Окончание срока, по ...", 9, 6, 2, 1, 1),
    Lables("Окончание ТП, с ...", 9, 7, 0, 1, 1),
    Lables("Окончание ТП, по ...", 9, 7, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
    Edits(5, "Название(шифр) СЗИ ...", 2, 3, 1, 1, dict = {}),
    Edits(6, "Соответствие документам ...", 3, 3, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (категории)
sheme = ("","серия","штучно","срок действия продлен для СЗИ, эксплуатируемых на ОИ",)
types = ("", "защита ПЭМН", "акустическая и вибрационная защита",
"защита телефонных линий", "фильтры помехоподавляющие", "СВТ","СЗИ от НСД",
"МЭ", "СОВ", "антивирусная защита", "доверенная загрузка",
"контроль съемных машинных носителей", "ОС", "СКЗИ", "защита ЭЦП",
"изделие информационных технологий")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
            Combos(4, "Тип СЗИ ...", "STypes", 1, types, 2, 1, 1, 1, dict = {}),
            Combos(7, "Схема сертификации...", "Serts", 7, sheme, 3, 1, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
    Dates(2, 0, -20, 6, 1, 1, 1, dict = {}),
    Dates(2, 1, 0, 6, 3, 1, 1, dict = {}),
    Dates(8, 0, -20, 7, 1, 1, 1, dict = {}),
    Dates(8, 1, 0, 7, 3, 1, 1, dict = {}),
)
TABLE_ATTR = TabTableAttr("Сертификаты", "сертификата № ", "serts", "numb", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"serts":       RelField(type = "OneTab-NoBag", table_tab = "serts", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "serts", pkey_bag = "id", pkey_bag_idx = 0),
"szis":        RelField(type = "ManyTab-OneBag", table_tab = "szis", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "sert_id", fkey_bag_idx = 4, table_bag = "serts", pkey_bag = "id", pkey_bag_idx = 0),
"assets":      RelField(type = "ManyTab-ManyBt-ManyBt-OneBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0, table_bt = "szis", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "sert_id", fkey_bag_idx = 4, table_bag = "serts", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_SZIs", pfkey_bt_tab = "id_szi", pfkey_bt_tab_idx = 1, pfkey_tab = "id_asset", pfkey_tab_idx = 0),
                }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["serts"], table_name = "serts", tab_name = "Сертификаты", map_list = mapper_lists["serts"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["szis"], table_name = "szis", tab_name = "СЗИ", map_list = mapper_lists["szis"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объект", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {"asset_szis": "",}
DOP_TABLE_WIDTHS = dict([(0, 50),])

#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }