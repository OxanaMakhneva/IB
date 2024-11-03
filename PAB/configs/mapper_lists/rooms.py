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
[(0, 30), (1, 120), (2, 80), (3, 80), (4, 100), (5, 100), (6, 100), (7, 100),
(8, 100), (9, 100), (10, 100), (11, 100), (12, 150),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Номер помещения", "Территория", "Этаж", "Оси", "Аттестат РП, №",
"Аттестат РП, от", "Аттестат РП, до", "Аттестат РП, инв.", "Тип РП",
"РП, спец. опция", "Выделенное", "Объекты")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = ''' SELECT
                Rooms.id, Rooms.numb, Territores.numb, Rooms.floor, Rooms.osi,
                AttestatumRPs.numb, AttestatumRPs.begin, AttestatumRPs.end,
                AttestatumRPs.inv,
                RPTypes.type,
                AttestatumRPs.spets, AttestatumRPs.vp,
                GROUP_CONCAT(Assets.name, ', ')
                FROM Rooms
                LEFT JOIN Territores ON Territores.id = Rooms.terr_id
                LEFT JOIN AttestatumRPs ON AttestatumRPs.id = Rooms.attRP_id
                LEFT JOIN RPTypes ON RPTypes.id = AttestatumRPs.type_id
                LEFT JOIN asset_rooms ON Rooms.id = asset_rooms.id_room
                LEFT JOIN Assets ON Assets.id = asset_rooms.id_asset
                WHERE Rooms.id > 0
                GROUP BY  Rooms.id
            '''
QUERY_STR['QPSQL7'] = ''' SELECT DISTINCT
                rooms.id, rooms.numb, territores.numb, rooms.floor, rooms.osi,
                attestatumrps.numb, attestatumrps.begin, attestatumrps.end,
                attestatumrps.inv,
                rptypes.type,
                attestatumrps.spets, attestatumrps.vp,
                string_agg(assets.name, ',')
                FROM rooms
                LEFT JOIN territores ON territores.id = rooms.terr_id
                LEFT JOIN attestatumRPs ON attestatumRPs.id = rooms.attrp_id
                LEFT JOIN rptypes ON rptypes.id = attestatumrps.type_id
                LEFT JOIN asset_rooms ON rooms.id = asset_rooms.id_room
                LEFT JOIN assets ON assets.id = asset_rooms.id_asset
                WHERE rooms.id > 0
                GROUP BY  rooms.id, territores.numb, attestatumrps.numb, 
				attestatumrps.begin, attestatumrps.end, attestatumrps.inv,
				rptypes.type, attestatumrps.spets, attestatumrps.vp
            '''


#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = ()
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = ()
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
              6:  DateColums(),
              7:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta" , None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
Lables("Территория...", 9, 2, 0, 1, 1),
Lables("Тип помещения ...", 9, 2, 2, 1, 1),
Lables("Спец.помещение ... ", 9, 2, 4, 1, 1),
Lables("Выделенное ... ", 9, 2, 6, 1, 1),
Lables("Номер помещения ...", 9, 3, 0, 1, 1),
Lables("Номер аттестата РП ...", 9, 3, 2, 1, 1),
Lables("Инвентарный ...", 9, 3, 4, 1, 1),
Lables("Срок аттестата РП до, с ...", 9, 4, 0, 1, 1),
Lables("Срок аттестата РП до, по ...", 9, 4, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Номер помещения ...", 3, 1, 1, 1, dict = {}),
        Edits(5, "Номер аттестата РП ...", 3, 3, 1, 1, dict = {} ),
        Edits(8, "Инвентарный ...", 3, 5, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (типы)
types = ("", "дневное", "круглосуточное", "склад")
terr = ("", "1", "2", "3", "4")
vp = ("", "Да", "Нет")
stets = ("", "Да", "Нет",)

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(2, "Территория...", "territores", 1, terr, 2, 1, 1, 1, dict = {}),
        Combos(9, "Тип помещения ...", "rptypes", 1, types, 2, 3, 1, 1, dict = {}),
        Combos(10, "Спец.помещение ...", None, None, stets, 2, 5, 1, 1, dict = {}),
        Combos(11, "Выделенное ... ", None, None, vp, 2, 7, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(7, 0, -20, 4, 1, 1, 1, dict = {}),
        Dates(7, 1, 0, 4, 3, 1, 1, dict = {}),
        )
TABLE_ATTR = TabTableAttr("Помещения", "Помещение №", "rooms", "numb", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"rooms":       RelField(type = "OneTab-NoBag", table_tab = "rooms", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "rooms", pkey_bag = "id", pkey_bag_idx = 0),
"attestatumrps":RelField(type = "OneTab-ManyBag", table_tab = "attestatumrps", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "rooms", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "attRP_id", fkey_tab_idx = 5),
"assets":      RelField(type = "ManyTab-ManyBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "rooms", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_rooms", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_room", pfkey_bag_idx = 1),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["rooms"], table_name = "rooms", tab_name = "Помещения", map_list = mapper_lists["rooms"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["attestatumrps"], table_name = "attestatumrps", tab_name = "Аттестат РП", map_list = mapper_lists["attestatumrps"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "Assets", tab_name = "Объекты", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {"asset_rooms": ""}
DOP_TABLE_WIDTHS = dict([(0, 50)])
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            }