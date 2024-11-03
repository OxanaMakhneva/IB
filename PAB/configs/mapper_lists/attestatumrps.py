from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Настройки для семейства окон "Аттестат"
#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict([(0, 50), (1, 300), (2, 100), (3, 120), (4, 120), (5, 100), (6, 150), (7, 100), (8, 100),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Название атт.", "Номер атт.", "Дата, от",
"Дата, до", "Инвентарный", "Пометка", "Тип помещения", "Спец.тип", "Выделенное")
QUERY_STR = {}
QUERY_STR['QPSQL7'] = ''' SELECT DISTINCT
                 attestatumrps.id, attestatumrps.name, attestatumrps.numb,
                 attestatumrps.begin, attestatumrps.end, attestatumrps.inv, secrets.type,
                 rptypes.type, attestatumrps.spets, attestatumrps.vp
                 FROM  attestatumrps
                 LEFT JOIN secrets ON secrets.id = attestatumrps.secret_id
                 LEFT JOIN rptypes ON rptypes.id = attestatumrps.type_id
                 LEFT JOIN rooms ON attestatumrps.id = Rooms.attrp_id
                 WHERE attestatumRPs.id > 0
                 GROUP BY attestatumrps.id, secrets.type, rptypes.type 
                 '''
QUERY_STR['SQLLITE'] = ''' SELECT
                 AttestatumRPs.id, AttestatumRPs.name, AttestatumRPs.numb,
                 AttestatumRPs.begin, AttestatumRPs.end, AttestatumRPs.inv, Secrets.type,
                 RPTypes.type, AttestatumRPs.spets, AttestatumRPs.vp
                 FROM  AttestatumRPs
                 LEFT JOIN Secrets ON Secrets.id = AttestatumRPs.secret_id
                 LEFT JOIN RPTypes ON RPTypes.id = AttestatumRPs.type_id
                 LEFT JOIN Rooms ON AttestatumRPs.id = Rooms.attRP_id
                 WHERE AttestatumRPs.id > 0
                 GROUP BY AttestatumRPs.id

            '''
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (1, )
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              3:  DateColums(),
              4:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta" , None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
Lables("Тип помещения ...", 9, 2, 0, 1, 1),
Lables("Спец.помещение ...", 9, 2, 2, 1, 1),
Lables("Выделенное ... ", 9, 2, 4, 1, 1),
Lables("Название аттестата ...", 9, 3, 0, 1, 1),
Lables("Номер аттестата ...", 9, 3, 2, 1, 1),
Lables("Инвентарный ...", 9, 3, 4, 1, 1),
Lables("Окончание срока, с ...", 9, 4, 0, 1, 1),
Lables("Окончание срока, по ...", 9, 4, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Название аттестата ...", 3, 1, 1, 1, dict = {}),
        Edits(2, "Номер аттестата ...", 3, 3, 1, 1, dict = {} ),
        Edits(5, "Инвентарный ...", 3, 5, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (типы)
types = ("", "дневное", "круглосуточное", "склад")
#Список значений для выпадающего списка (спец. опция)
stets = ("","Да", "Нет",)
#Список значений для выпадающего списка (выделенное)
vp = ("","Да", "Нет",)
#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
            Combos(7, "Тип помещения ...", "rptypes", 1, types, 2, 1, 1, 1, dict = {}),
            Combos(8, "Спец.помещение ...", None, None, stets, 2, 3, 1, 1, dict = {}),
            Combos(9, "Выделенное ...", None, None, vp, 2, 5, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
Dates(4, 0, -20, 4, 1, 1, 1, dict = {}),
Dates(4, 1, 0, 4, 3, 1, 1, dict = {}),
)
TABLE_ATTR = TabTableAttr("Аттестаты РП", "аттестата", "attestatumrps", "full_name", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"attestatumrps":    RelField(type = "OneTab-NoBag", table_tab = "attestatumRPs", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "attestatumrps", pkey_bag = "id", pkey_bag_idx = 0),
"rooms":            RelField(type = "ManyTab-OneBag", table_tab = "rooms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "attrp_id", fkey_bag_idx = 5, table_bag = "attestatumrps", pkey_bag = "id", pkey_bag_idx = 0),
"assets":           RelField(type = "ManyTab-ManyBt-ManyBt-OneBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0, table_bt = "rooms", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "attrp_id", fkey_bag_idx = 5, table_bag = "attestatumrps", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_rooms", pfkey_bt_tab = "id_room", pfkey_bt_tab_idx = 1, pfkey_tab = "id_asset", pfkey_tab_idx = 0),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["attestatumrps"], table_name = "attestatumrps", tab_name = "Аттестаты РП", map_list = mapper_lists["attestatumrps"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["rooms"], table_name = "Rooms", tab_name = "Помещения", map_list = mapper_lists["rooms"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "Assets", tab_name = "Объекты", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {"asset_rooms": "",}
DOP_TABLE_WIDTHS = dict([(0, 50), (1, 150), (2, 120), (3, 120), (4, 100), (5, 100), (6, 120), (7, 120), (8, 120), (9, 120), (10, 120)])
