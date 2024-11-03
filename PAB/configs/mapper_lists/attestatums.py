from PyQt5.QtCore import QDate
from models.relations_in_BD_qt import RelField
from models.manipulations_in_TabWin import TabModels, MapperField, prom_model
from models.manipulations_in_MainWin import DateColums, Lables, Edits, Combos, Dates
from models.model_MainWin import TabWindow, TabTableAttr
from models.init_set.config_mapperfields import mapper_lists

#Основное окно
#Ширина столбцов таблицы
MAIN_TABLE_WIDTHS = dict(
[(0, 30), (1, 300), (2, 100), (3, 85), (4, 85), (5, 80), (6, 80),
(7, 200), (8, 80),])
#Заголовки, которые будут отображаться вместо служебных в основной таблице
HEADERS = (
"ID", "Название аттестата", "Номер", "Дата, от", "Дата, до", "Инвентарный", "Пометка",
"Название объекта", "Тип объекта", "Приказ о вводе", "Приказ, от")
QUERY_STR = {}
QUERY_STR['SQLLITE'] = """ SELECT
                Attestatums.id, Attestatums.name, Attestatums.numb,
                Attestatums.begin, Attestatums.end, Attestatums.inv, Secrets.type,
                GROUP_CONCAT( Assets.name || " ("  || Assets.year || ")", "; "),
                ATypes.type,
                CASE
                    WHEN OTypes.type LIKE '%' || "Приказ о вводе" || '%' THEN ORDs.full_name
                    ELSE ""
                    END ORDsFullName,
                CASE
                    WHEN OTypes.type LIKE '%' || "Приказ о вводе" || '%' THEN MAX(ORDs.begin)
                    ELSE ""
                    END ORDsBegin
                FROM Attestatums
                LEFT JOIN Assets ON Attestatums.asset_id = Assets.id
                LEFT JOIN  Secrets ON Attestatums.secret_id = Secrets.id
                LEFT JOIN  ATypes ON Assets.type_id = ATypes.id
                LEFT JOIN asset_ords ON asset_ords.id_asset = Assets.id
                LEFT JOIN  ORDs ON ORDs.id = asset_ords.id_ord
                LEFT JOIN OTypes ON ORDs.type_id = OTypes.id
                WHERE  Attestatums.id > 0
                GROUP BY  Attestatums.id
          
                
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

SELECT
attestatums.id, 
attestatums.name, 
attestatums.numb,
attestatums.begin, 
attestatums.end, 
attestatums.inv, 
secrets.type,
string_agg(CONCAT(assets.name,' (', assets.year, ') '), ','),
atypes.type,
ords.full_name
FROM attestatums
LEFT JOIN assets ON attestatums.asset_id = assets.id
LEFT JOIN  secrets ON attestatums.secret_id = secrets.id
LEFT JOIN  atypes ON assets.type_id = atypes.id
LEFT JOIN asset_ords ON asset_ords.id_asset = assets.id
LEFT JOIN  ords ON ords.id = asset_ords.id_ord
LEFT JOIN otypes ON ords.type_id = otypes.id
LEFT JOIN ord_prom ON ord_prom.asset_id = assets.id
WHERE  attestatums.id > 0 and ords.begin = ord_prom.dates
GROUP BY  attestatums.id, secrets.type, otypes.type, atypes.type, ords.full_name
 """
#Индексы столбцов, в которых храняться имена собственные, которые необходимо поместить в кавычки
NAME_COLUMS = (1, 7,)
#Индексы столбцов, в которых храняться данные, которые не надо отображать
NODISPLAY_COLUMS = (10, )
#Заполняется для всех столбцов, в которыхесть даты. Если разукрашивать не надо, последние три столбца оставить пустыми
DATE_COLUMS = {
            3:  DateColums(None, None, None, None, None),
            4:  DateColums(QDate.currentDate().addMonths(0), QDate.currentDate().addMonths(6), "red", "magenta", None),
            10:  DateColums(None, None, None, None, None),
              }
#Именованный кортеж для ярлыков поля фильтрации:
LABLES = (
        Lables("Панель для уточнения поискового запроса (условия применяются одновременно)", 11, 0, 0, 1, 4),
        Lables("Название аттестата...", 9, 2, 0, 1, 1),
        Lables("Номер аттестата ...", 9, 2, 2, 1, 1),
        Lables("Инвентарный... ", 9, 2, 4, 1, 1),
        Lables("Название объекта ...", 9, 3, 0, 1, 1),
        Lables("Тип объекта ...", 9, 3, 2, 1, 1),
        Lables("Аттестат выдан, с ...", 9, 4, 0, 1, 1),
        Lables("Аттестат выдан, по ...", 9, 4, 2, 1, 1),
        )
#Именованный кортеж для поля фильтрации:
EDITS = (
        Edits(1, "Название аттестата ...", 2, 1, 1, 1, dict = {}),
        Edits(2, "Номер аттестата ...", 2, 3, 1, 1, dict = {} ),
        Edits(6, "Инвентарный ...", 2, 5, 1, 1, dict = {} ),
        Edits(7, "Название объекта ...", 3, 1, 1, 1, dict = {} ),
        )
#Список значений для выпадающего списка (типы объектов)
types = ("", "ИСПДн", "ГИС", "КИИ")

#Именованный кортеж для выпадающих списков поля фильтрации:
COMBOS = (
        Combos(7, "Тип объекта...", "atypes", 1, types, 3, 3, 1, 1, dict = {}),
        )
#Именованный кортеж для ввода дат в поле фильтрации:
DATES = (
        Dates(4, 0, -20, 4, 1, 1, 1, dict = {}),
        Dates(4, 1, 0, 4, 3, 1, 1, dict = {}),
        )
TABLE_ATTR = TabTableAttr("Аттестаты", "аттестата №", "attestatums", "numb", "id", 0)
#Дополнительное окно
#Словарь для управления взаимодействием между связанными таблицами (каждая строчка соответствует таблице вкладки)
RELS_DICT = {
"attestatums":    RelField(type = "OneTab-NoBag", table_tab = "attestatums", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "attestatums", pkey_bag = "id", pkey_bag_idx = 0),
"assets":         RelField(type = "OneTab-ManyBag", table_tab = "assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "attestatums", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "asset_id", fkey_tab_idx = 7),
            }
#Список для хранения основных данных по таблмцам вкладок
TABS_LIST = (
TabModels(models = {}, relfield = RELS_DICT["attestatums"], table_name = "attestatums", tab_name = "Аттестат", map_list = mapper_lists["attestatums"], permissions = ("r", "w"), filter_str = "", filter_id = []),
TabModels(models = {}, relfield = RELS_DICT["assets"], table_name = "assets", tab_name = "Объект", map_list = mapper_lists["assets"], permissions = ("r"), filter_str = "", filter_id = []),
)
#Словарь для хранения моделей данных для общих таблиц
PROM_DICT= {}
#Словарь для хранения моделей данных для таблиц, которые потенциально могут ссылатся на текущую
LINK_DICT= {}

DOP_TABLE_WIDTHS = dict([(0, 50)])
