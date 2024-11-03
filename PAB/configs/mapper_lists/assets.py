from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 30), (1, 30), (2, 120), (3, 75), (4, 65), (5, 65), (6, 120), (7, 100),
 (8, 80), (9, 80), (10, 120), (11, 100), (12, 80), (13, 80),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Ст-с", "Название объекта", "Тип объекта", "Категория", "Класс",
"Аттестат", "Аттестат, номер", "Аттестат, от", "Аттестат, до", "Приказ о вводе",
"Приказ, номер", "Приказ, от", "Приказ, до", "Инвентарный")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                Assets.id, Assets.status_id,
                GROUP_CONCAT( Assets.name || " ("  || Assets.year || ")", "; "),
                ATypes.type, AKats.type, AKlasses.type,
                Attestatums.name, Attestatums.numb, Attestatums.begin,
                Attestatums.end,
                CASE
                    WHEN OTypes.type LIKE '%' || "Приказ о вводе" || '%' THEN ORDs.name
                    ELSE ""
                    END ORDsName,
                CASE
                    WHEN OTypes.type LIKE '%' || "Приказ о вводе" || '%' THEN ORDs.numb
                    ELSE ""
                    END ORDsNumb,
                CASE
                    WHEN OTypes.type LIKE '%' || "Приказ о вводе" || '%' THEN MAX(ORDs.begin)
                    ELSE ""
                    END ORDsBegin,
                CASE
                    WHEN OTypes.type LIKE '%' || "Приказ о вводе" || '%' THEN ORDs.end
                    ELSE ""
                    END ORDsEnd,
                Attestatums.inv
                FROM Assets
                LEFT JOIN ATypes ON ATypes.id = Assets.type_id
                LEFT JOIN AKats ON AKats.id = Assets.kat_id
                LEFT JOIN AKlasses ON AKlasses.id = Assets.klass_id
                LEFT JOIN Attestatums ON Attestatums.asset_id = Assets.id
                LEFT JOIN asset_ords ON asset_ords.id_asset = Assets.id
                LEFT JOIN  ORDs ON ORDs.id = asset_ords.id_ord
                LEFT JOIN OTypes ON ORDs.type_id = OTypes.id
                WHERE Assets.id > 0
                GROUP BY Assets.id
             """

QUERY_STR['QPSQL7'] = """ 
WITH ord_prom AS (
SELECT
MAX(ords.begin) AS dates,
assets.id AS asset_id

FROM ords
LEFT JOIN otypes ON ords.type_id = otypes.id
LEFT JOIN asset_ords ON asset_ords.id_ord = ords.id
LEFT JOIN  assets ON assets.id = asset_ords.id_asset
WHERE otypes.type like '%Приказ о вводе%'
GROUP BY assets.id
)

SELECT assets.id, 
assets.status_id,
string_agg(CONCAT(assets.name,' (', assets.year, ') '), ','),
atypes.type, akats.type, aklasses.type,
attestatums.name, attestatums.numb, attestatums.begin,
attestatums.end,
ords.name,
ords.numb,
ords.begin,
ords.end,
attestatums.inv
FROM assets
LEFT JOIN atypes ON atypes.id = assets.type_id
LEFT JOIN akats ON akats.id = assets.kat_id
LEFT JOIN aklasses ON aklasses.id = assets.klass_id
LEFT JOIN attestatums ON attestatums.asset_id = assets.id
LEFT JOIN asset_ords ON asset_ords.id_asset = assets.id
LEFT JOIN  ords ON ords.id = asset_ords.id_ord
LEFT JOIN otypes ON ords.type_id = otypes.id
LEFT JOIN ord_prom ON ord_prom.asset_id = assets.id
--WHERE assets.id > 0 and ords.begin = ord_prom.dates
GROUP BY assets.id, attestatums.name, attestatums.numb, 
				attestatums.begin, attestatums.end, attestatums.inv,
				atypes.type, akats.type, aklasses.type, otypes.type, 
				ords.name, ords.numb, ords.begin, ords.end
"""
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (2, 6, 10)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = (1, )
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {8:  DateColums(),
               9:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta" , None),
               12: DateColums(QDate.currentDate()),
               13: DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta" , None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
        Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 20),
        Lables("Основная информация по объектам", 9, 1, 0, 1, 7),
        Lables("Основная информация по документам", 9, 5, 0, 1, 10),
        Lables("Тип объекта ...", 9, 1, 7, 1, 3),
        Lables("Категория объекта ...", 9, 1, 10, 1, 3),
        Lables("Класс объекта ...", 9, 1, 13, 1, 3),
        Lables("Календарные периоды ", 9, 9, 0, 1, 20),
        Lables("Аттестат выдан с ...", 9, 10, 0, 1, 2),
        Lables("Аттестат выдан по ....", 9, 10, 5, 1, 2),
        Lables("Окончание срока с ...", 9, 10, 10, 1, 2),
        Lables("Окончание срока по ...", 9, 10, 15, 1, 2),
        Lables("Приказ утвержден с ...", 9, 14, 0, 1, 2),
        Lables("Приказ утвержден по ...", 9, 14, 5, 1, 2),)
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(2, "Название объекта ...", 2, 0, 1, 7, dict = {}),
        Edits(6, "Название аттестата ...", 6, 0, 1, 6, dict = {} ),
        Edits(7, "Номер аттестата ...", 6, 6, 1, 4, dict = {} ),
        Edits(10, "Название приказа о вводе...", 6, 10, 1, 6, dict = {}),
        Edits(11, "Номер приказа о вводе...", 6, 16, 1, 4, dict = {}),
        Edits(14, "Инвентарный объекта ...", 2, 16, 1, 4, dict = {}),)

#Список значений для выпадающего списка (категории)
types = ("","АС","ИСПДн","ГИС","КИИ",)
kats = ("",)
klasses = ("",)

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(3, "Тип объекта ...", "ATypes", 1, types, 2, 7, 1, 3, dict = {}),
        Combos(4, "Категория объекта ...", "AKats", 1, kats, 2, 10, 1, 3, dict = {}),
        Combos(5, "Класс объекта ...", "AKlasses", 1, klasses, 2, 13, 1, 3, dict = {}),)
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(8, 0, -20, 10, 2, 1, 3, dict = {}),
        Dates(8, 1, 0, 10, 7, 1, 3, dict = {}),
        Dates(9, 0, -20, 10, 12, 1, 3, dict = {}),
        Dates(9, 1, 20, 10, 17, 1, 3, dict = {}),
        Dates(12, 0, -20, 14, 2, 1, 3, dict = {}),
        Dates(12, 1, 0, 14, 7, 1, 3, dict = {}),)

TABLE_ATTR = TabTableAttr(inital_lable = "Объекты", entity_lable = "объекта", inital_table_name = "assets",  entity_column_name = "name", inital_prymary_name = "id", inital_prymary_idx = 0)

#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"assets":       RelField(type = "OneTab-NoBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0),
"attestatums":  RelField(type = "ManyTab-OneBag", table_tab = "attestatums", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "asset_id", fkey_bag_idx = 7, table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0),
"rooms":        RelField(type = "ManyTab-ManyBag", table_tab = "rooms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_rooms", pfkey_tab = "id_room", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"attdocs":      RelField(type = "ManyTab-ManyBag", table_tab = "attdocs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_attdocs", pfkey_tab = "id_attdoc", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"ords":         RelField(type = "ManyTab-ManyBag", table_tab = "ords", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_ords", pfkey_tab = "id_ord", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"szis":         RelField(type = "ManyTab-ManyBag", table_tab = "szis", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_szis", pfkey_tab = "id_szi", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"responsibles": RelField(type = "ManyTab-ManyBag", table_tab = "responsibles", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_responsibles", pfkey_tab = "id_responsible", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"attestatumrps":RelField(type = "OneTab-ManyBt-ManyBt-ManyBag", table_tab = "attestatumrps", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "rooms", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "attRP_id", fkey_tab_idx = 5, table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_bag = "asset_rooms", pfkey_bt_bag = "id_room", pfkey_bt_bag_idx = 1, pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"serts":        RelField(type = "OneTab-ManyBt-ManyBt-ManyBag", table_tab = "serts", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "szis", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "sert_id", fkey_tab_idx = 5, table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_bag = "asset_szis", pfkey_bt_bag = "id_szi", pfkey_bt_bag_idx = 1, pfkey_bag = "id_asset", pfkey_bag_idx = 0),
"arms":         RelField(type = "ManyTab-OneBag", table_tab = "ARMs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "asset_id", fkey_bag_idx = 4, table_bag = "assets", pkey_bag = "id", pkey_bag_idx = 0),
"tehnos":       RelField(type = "ManyTab-OneBt-ManyBt-OneBag", table_bt = "arms", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "asset_id", fkey_bag_idx = 7, table_tab = "tehnos", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "arm_id", fkey_bt_tab_idx = 4),
"pc_softs":     RelField(type = "ManyTab-OneBt-ManyBt-OneBag", table_bt = "arms", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "asset_id", fkey_bag_idx = 4, table_tab = "pc_softs", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "arm_id", fkey_bt_tab_idx = 7),
"users":        RelField(type = "ManyTab-OneBt-ManyBt-OneBag", table_bt = "arms", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "asset_id", fkey_bag_idx = 4, table_tab = "users", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "arm_id", fkey_bt_tab_idx = 5),
                }

#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объект", map_list = mapper_lists["assets"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["attestatums"], table_name = "attestatums", tab_name = "Аттестат соответствия", map_list = mapper_lists["attestatums"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["rooms"], table_name = "rooms", tab_name = "Помещения", map_list = mapper_lists["rooms"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["attdocs"], table_name = "attdocs", tab_name = "Документы", map_list = mapper_lists["attdocs"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["ords"], table_name = "ords", tab_name = "ОРД", map_list = mapper_lists["ords"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["szis"], table_name = "szis", tab_name = "СЗИ", map_list = mapper_lists["szis"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["responsibles"], table_name = "responsibles", tab_name = "Ответственные", map_list = mapper_lists["responsibles"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["users"], table_name = "users", tab_name = "Учетные записи", map_list = mapper_lists["users"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["attestatumrps"], table_name = "attestatumrps", tab_name = "Аттестаты РП", map_list = mapper_lists["attestatumrps"], permissions = ("r"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["serts"], table_name = "serts", tab_name = "Сертификаты", map_list = mapper_lists["serts"], permissions = ("r"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["arms"], table_name = "arms", tab_name = "АРМы", map_list = mapper_lists["arms"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["tehnos"], table_name = "tehnos", tab_name = "ТС", map_list = mapper_lists["tehnos"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),
#TabModels(models = {}, relfield = RELS_DICT["pc_softs"], table_name = "pc_softs", tab_name = "ПО", map_list = mapper_lists["pc_softs"], permissions = ("r", "w", "e"), filter_str = "", filter_id = []),

                )
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {
            "asset_rooms": "",
            "asset_szis": "",
            "asset_responsibles": "",
            "asset_ords": "",
            "asset_attdocs": "",
            }

#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {
            "attestatums": ('id', 7),
            "arms": ('id', 4),
            }
#DOP_TABLE_WIDTHS = dict([(0, 30), (1, 150), (2, 400), (3, 150), (4, 150), (5, 150),])
DOP_TABLE_WIDTHS = dict([(0, 50)])
