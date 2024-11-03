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
[(0, 30), (1, 150), (2, 200), (3, 200), (4, 100), (5, 100), (6, 130),
(7, 130), (8, 80),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Тип СЗИ", "Модель(шифр)", "Название элемента", "Номер серийный", "СЗЗ", "Номер сертификата",
"Статус сертификата", "Срок ТП", "Объекты")

QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                 SZIs.id, STypes.type, Serts.name, SElements.name,
                 SZIs.numb, SZIs.SZZ, Serts.numb, Serts.scheme, Serts.end_tp,
                 GROUP_CONCAT(Assets.name, ', ')
                 FROM SZIs
                 LEFT JOIN SElements ON SElements.id = SZIs.element_id
                 LEFT JOIN Serts ON Serts.id = SZIs.sert_id
                 LEFT JOIN STypes ON STypes.id = Serts.type_id
                 LEFT JOIN asset_SZIs ON asset_SZIs.id_SZI = SZIs.id
                 LEFT JOIN  Assets ON Assets.id = asset_SZIs.id_asset
                 WHERE SZIs.id > 0
                 GROUP BY  SZIs.id
                 """

QUERY_STR['QPSQL7'] = """ SELECT DISTINCT
                 szis.id, stypes.type, serts.name, selements.name,
                 szis.numb, szis.szz, serts.numb, serts.scheme, serts.end_tp,
                 string_agg(assets.name,',')
                 FROM szis
                 LEFT JOIN selements ON selements.id = szis.element_id
                 LEFT JOIN serts ON serts.id = szis.sert_id
                 LEFT JOIN stypes ON stypes.id = serts.type_id
                 LEFT JOIN asset_szis ON asset_szis.id_szi = szis.id
                 LEFT JOIN  assets ON assets.id = asset_szis.id_asset
                 WHERE szis.id > 0
                 GROUP BY  szis.id, stypes.type, serts.name, selements.name,
				 serts.numb, serts.scheme, serts.end_tp
                 """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = ()
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              8:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta" , None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
    Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
    Lables("Тип СЗИ...", 9, 3, 4, 1, 1),
    Lables("Номер СЗИ ... ", 9, 2, 0, 1, 1),
    Lables("Номер СЗЗ ... ", 9, 2, 2, 1, 1),
    Lables("Модель СЗИ ...", 9, 2, 4, 1, 1),
    Lables("Название элемента ...", 9, 3, 0, 1, 1),
    Lables("Номер сертификата ...", 9, 3, 2, 1, 1),
    Lables("Срок ТП до, с ...", 9, 4, 0, 1, 1),
    Lables("Срок ТП до, по ...", 9, 4, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(4, "Номер СЗИ ...", 2, 1, 1, 1, dict = {}),
        Edits(5, "Номер СЗЗ ...", 2, 3, 1, 1, dict = {} ),
        Edits(2, "Модель СЗИ ...", 2, 5, 1, 1, dict = {} ),
        Edits(3, "Название элемента ...", 3, 1, 1, 1, dict = {} ),
        Edits(6, "Номер сертификата ...", 3, 3, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (категории)
types = ("", "Защита от ПЭМИН", "Защита от ПЭМИ", "акустическая и вибрационная защита", "защита телефонных линий",
     "фильтры помехоподавляющие", "СВТ","СЗИ от НСД", "МЭ", "СОВ", "антивирусная защита",
     "доверенная загрузка", "контроль съемных машинных носителей", "ОС", "СКЗИ", "защита ЭЦП",
     "изделие информационных технологий")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(1, "Тип СЗИ...","stypes", 1, types, 3, 5, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(8, 0, -20, 4, 1, 1, 1, dict = {}),
        Dates(8, 1, 0, 4, 3, 1, 1, dict = {}),
        )
TABLE_ATTR = TabTableAttr("СЗИ", "СЗИ №", "szis", "numb", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"szis":       RelField(type = "OneTab-NoBag", table_tab = "szis", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "szis", pkey_bag = "id", pkey_bag_idx = 0),
"serts":      RelField(type = "OneTab-ManyBag", table_tab = "serts", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "szis", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "sert_id", fkey_tab_idx = 4),
"assets":     RelField(type = "ManyTab-ManyBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "szis", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_szis", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_szi", pfkey_bag_idx = 1),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["szis"], table_name = "szis", tab_name = "СЗИ", map_list = mapper_lists["szis"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["serts"], table_name = "serts", tab_name = "Сертификаты", map_list = mapper_lists["serts"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объекты", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {"asset_szis": ""}
DOP_TABLE_WIDTHS = dict([(0, 50),])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }