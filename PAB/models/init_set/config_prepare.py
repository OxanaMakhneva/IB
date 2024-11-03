#Для считывания конфигурационных данных из файлов .ini
import configparser
#Для реализации динамического импорта
import importlib


def prepare(inital_table_name):
    # Считываем общие для всех окон параметры
    from models.init_set.config_general import SVALIDATOR, IVALIDATOR, MASK
    from models.init_set.config_qactions import TAB_QACTIONS, MAIN_QACTIONS
    #Считываем данные БД из .ini
    config = configparser.ConfigParser()
    config.read('configs\config_general_param.ini')
    try:
        DB_TYPE = config['user']['DB_TYPE']
        DB_NAME = config['user']['DB_NAME']
        SERVISE_TABLE_PATH = config['config']['SERVISE_TABLE_PATH']
    except:
        DB_TYPE = 'QSQLITE'
        DB_NAME = 'test1.db'
        SERVISE_TABLE_PATH = 'C:\BD\configs\config_servise_tables.txt'


    #Считываем конфигурационные данные для основного окна, привязаного к asset и его дополнительных окон
    module_name = f'..{inital_table_name}'
    module_pkg = f'configs.mapper_lists.pkg'
    module = importlib.import_module(module_name, module_pkg)

    #Изымаем из списка моделей типа TabModels (TABS_LIST) список моделей для настройки мэппера первичной таблицы
    #Если конфиг заполнен корректно - искомый список находится в нулевой записи TABS_LIST, а запись о prymary key первичной таблицы - на нулевой позиции искомого списка
    map_list = module.TABS_LIST[0].map_list
    #Проверяем, что получена запись о полях первичной таблицы
    Error_str = f'В конфигурационном файле {module_name} поместите запись об основной таблице {inital_table_name} на нулевую позицию. Иначе возможно некорректное поведение приложения '
    assert (map_list[0].table == inital_table_name and map_list[0].column_map == map_list[0].pkey), (Error_str)

    #Сборка параметров в словари
    MAIN_PARAMS = {
    "LABLES": module.LABLES, "edits": module.EDITS, "combos": module.COMBOS, "dates": module.DATES,
    "HEADERS": module.HEADERS, "table_widths": module.MAIN_TABLE_WIDTHS, "QUERY_STR": module.QUERY_STR,
    "NAME_COLUMS": module.NAME_COLUMS, "NODISPLAY_COLUMS": module.NODISPLAY_COLUMS,
    "DATE_COLUMS": module.DATE_COLUMS, "TABLE_ATTR": module.TABLE_ATTR, "map_list": map_list}
    TAB_PARAMS = {
    "RELS_DICT": module.RELS_DICT, "tabs_list": module.TABS_LIST, "prom_dict": module.PROM_DICT,
    "link_dict": module.LINK_DICT, "table_width": module.DOP_TABLE_WIDTHS, "TAB_TABLE_ATTR": module.TABLE_ATTR,}
    #Формируем итоговые наборы параметров
    full_GERAL_PARAMS = {"DB_TYPE": DB_TYPE, "DB_NAME": DB_NAME, "SERVISE_TABLE_PATH": SERVISE_TABLE_PATH}
    full_MAIN_PARAMS = {"QACTIONS": MAIN_QACTIONS, **MAIN_PARAMS}
    full_TAB_PARAMS = {"SVALIDATOR": SVALIDATOR, "IVALIDATOR": IVALIDATOR,
                       "MASK": MASK, "QACTIONS": TAB_QACTIONS, **TAB_PARAMS}
    return full_GERAL_PARAMS, full_MAIN_PARAMS, full_TAB_PARAMS
