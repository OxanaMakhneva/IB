import pandas as pd
from all_functions import *
import app_logger
logger = app_logger.get_logger(__name__)
from pathlib import Path

pc_path = Path("C:\\fstek_ready\\pc.xlsx").absolute()
bd_path = Path("C:\\fstek_ready\\bd.xlsx").absolute()

#Загрузка данных по уязвимостям
logger.info("Чтение данных из файла с уязвимостями ...")
bd_soft = read_data(bd_path, "xlsx", "уязвимостями")
logger.info("Чтение данных из файла с ПК ...")
pc_soft = read_data(pc_path, "xlsx", "ПО из ИС")

## Обработка загруженных данных (ПО ПК)
pc_soft.columns = ['name', 'version', 'developer', 'numb_dev', 'comment', 'ts', 'tel', 'update', 'update_rule', 'install']
pc_soft = pc_soft.drop(['comment', 'ts', 'tel', 'update', 'update_rule'], axis = 1)
pc_soft.numb_dev = pc_soft.numb_dev.transform(lambda x: -1 if x == 'Не поддерживается' else x)
#Удаление чисел
template = re.compile(r'(\d+)')
pc_soft.name = pc_soft.name.transform(lambda x: re.sub(template, '', str(x), count = 0))
#Поиск всех уникальных названий ПО, установленных на ПК
pc_soft_names = [element for element in \
                 list(set(pc_soft.name.transform(lambda x: norm_sentence(x)).values)) \
                 if len(element) > 1]

## Предобработка загруженных данных (ПО с БД)
bd_soft = bd_soft.iloc[2:,:]
bd_soft.columns = ['id', 'name', 'about', 'vendor', 'soft', 'version', 'type',\
                'OS', 'class', 'date', 'cvss_2', 'cvss_3', 'level','mera', \
                'status', 'exployt', 'fix', 'source', 'cve', 'info', \
                'name_error', 'type_error']
#Перевод дат в тип datetime
bd_soft.date = bd_soft.date.transform(lambda x: change_date(x))
#Выборка только тех данных, которые актуальны для заданного периода
user_date = pd.to_datetime(input("Введите дату, с которой вывести уязвимости:  "), format='%d.%m.%Y')
bd_soft = bd_soft.query('date > @user_date')

logger.info("Обработка данных ...")
#Обработка столбца с версиями. Удаление пропущенных значений
bd_soft = bd_soft.dropna(subset = ['version'], axis = 0)
#Удаление дубликатов внутри списков с версиями
bd_soft.version = bd_soft.version.transform(lambda x: ', '.join(sorted(list(set(map(str.strip, x.split(',')))))))
#Удаление пропущенных значений в версиях
bd_soft = bd_soft.dropna(subset = ['version'], axis = 0)
#Удаление дубликатов внутри списков с версиями
bd_soft.version = bd_soft.version.transform(lambda x: ', '.join(sorted(list(set(map(str.strip, x.split(',')))))))
#Поиск всех уникальных комбинаций версия (название ПО) в ДФ БДУ
#Расчет словаря-сопоставления {название версии: название ПО}
bd_vers_names = calc_bd_version_dict(bd_soft)

##Отбор из БДУ только тех записей, которые можно сопоставить с записями с ПК
#Расчет словаря {название ПО из БД: [все уникальные подходящие навазания из ПК]}
bd_pc_soft = search_common_dict(list(set(bd_vers_names.values())), pc_soft_names, 0.8, 0.5)

#Выбор только тех данных, которые актуальны для заданного списка ПО
#Расчет столбца с названиями ПО из БДУ, которым нашлись подходящие значения с ПК
logger.info("Исключение из столбца soft ПО, которыму не нашлись подходящие значения в файле с ПО с ПК ...")
bd_soft.soft = bd_soft.soft.transform(lambda x: search_common_soft(x, bd_pc_soft))
#Исключение нерелевантных записей
bd_soft = bd_soft.query('soft != "no"')
#Пересчет словаря сопоставления {название версии: название ПО}
bd_vers_names = calc_bd_version_dict(bd_soft)
#Исключаем из словаря сопоставления названия версий, которые связаны с названиями ПО, которого нет на ПК
bd_vers_names = {key: value for key, value in bd_vers_names.items() if bd_pc_soft.get(value)}


#Обработка столбцов в отфильтрованом ДФ БДУ
#Расчет наиболее критических уровней опасности для каждой уязвимости
logger.info("Расчет наиболее критичных уровней опасности ...")
bd_soft.level = bd_soft.level.transform(lambda x:  calc_max_level(x))
#Отсеивание неактуальных версий
logger.info("Исключение из данных для отчета записей с версиями, по которым для ПО с ПК нет актуальных уязвимостей ...")
#Расчет словаря {название ПО на ПК: название версии на ПК}
all_names = list(pc_soft.name.values)
all_vers = list(pc_soft.version.values)
name_vers_pc = {norm_sentence(all_names[ind]): all_vers[ind] for ind in range(len(all_names))}
#Расчет списка актуальных версий
actual_vers = calc_actual_versions(bd_vers_names, bd_pc_soft, name_vers_pc)
#Удаляем из словаря сопоставления все версии из БДУ, которые не признаны актуальными
bd_vers_names = {key: value for key, value in bd_vers_names.items() if key in actual_vers}

logger.info("Расчет данных для сводной таблицы (список ПО и актуальных уязвимостей) ...")
#Подготовка первого ДФ, в котором центральными элементами будут не уязвимости, а название ПО и его версии
#Расчет словаря с уровнями опасностей, на базе которого будет построен отдельный ДФ
#{название столбца с уровнем опасности: [строки с перечислением уязвимостей для каждой версии]}

#НАзвания уровней опасности
all_levels = ['Критический', 'Высокий', 'Средний', 'Низкий', 'Нет']
all_levels_name = ['critic', 'hight', 'medium', 'low', 'no']
#Расчет словаря  {версия: {уровень: [список уязвимостей]}},где:
#- версия - это ключи из всех уникальных версий (all_versions)
#- уровень - это ключи из всех уникальных названий уровней опасности (all_levels)
#Шаблон словаря
ubds = {version: {level: [] for level in all_levels} for version in bd_vers_names.keys()}
#Заполнение промежуточного словаря
for index, row in bd_soft.iterrows():
    for version in  bd_vers_names.keys():
        if version in row.version.split(','):
            ubds[version][row.level].append(row.id)
#Заполнение основного словаря
levels = \
{all_levels_name[idx]: ['; '.join(ubds[version][all_levels[idx]]) for version in bd_vers_names.keys()] for idx in range(len(all_levels))}
#Добавление к словарю данных по названиям версий
levels['version'] = bd_vers_names.keys()
#Посторение ДФ
df_levels = pd.DataFrame(levels)
#Расчет словаря с данными по ПО, на базе которого будет построен отдельный ДФ
#Для каждой уникальной комбинации заполянем столбцы (ПО, производитель, список уязвимостей)
soft = pd.DataFrame({'version':  bd_vers_names.keys(), 'name':  bd_vers_names.values()})

#Объединение с данными по уровням опасности
soft = df_levels.merge(soft, on = 'version')
del df_levels
#Отчищение от записей без уязвимостей
soft = soft.query("critic != '' or medium != '' or hight != '' or low != ''")
#Перестановка столбцов
soft = soft[['name', 'version', 'critic', 'hight', 'medium', 'low']].sort_values(by = 'name')

#Расчет индексов общих строк для объединения в таблице word
name_indexes = soft.name.value_counts().sort_index(ascending = True).cumsum().shift(1).fillna(0)
name_indexes = name_indexes.astype(int)
name_indexes = name_indexes.to_dict()
#Словарь с индексами (индекс - фактически номер строчки в таблице, в которой впервые встречается новое название ПО)
dict_indexes = {value: key for key, value in name_indexes.items()}

logger.info("Расчет данных для сводной таблицы (данные по уязвимостям) ...")
## Подготовка второго ДФ таблицы с описанием всех уязвимостей, которые актальны для ПО к ПК
#Обработка столбцов со списками уязвимостей, чтобы их можно было объединить
u_cols = ['critic', 'hight', 'medium', 'low']
for col in u_cols:
    soft[f'{col}_cumsum'] = soft[col].transform(lambda x: x + ";" if x else x)
#Формируем список всех актуальных уязвимостей (собираем все из отчетного ДФ)
cumsum_cols = ['critic_cumsum', 'hight_cumsum', 'medium_cumsum', 'low_cumsum']
all_us = list(set(map(str.strip, soft[cumsum_cols].sum().sum().split(";"))))
#Отфильтровываем ДФ с инф. об уязвимостях по списку актуальных версий
soft = soft.drop(cumsum_cols, axis = 1)
bd_soft = bd_soft.query('id in @all_us')

logger.info("Запись отчета в word...")
#Запись полученного ДФ в таблицу word
width_1 = [100, 400, 400, 400, 400]
width_2 = [100, 100, 100, 100, 100, 100, 100]
width_3 = [200, 400]
need_col = ['id', 'name', 'class', 'date', 'level', 'mera', 'fix']
output = input("Данные подготовлены для записи отчета. Введите название файла для его сохранения (без расширения): ")
output = output + ".docx"
create_myword(\
    [soft.drop('name', axis = 1), bd_soft[need_col], pd.DataFrame({'bd': bd_pc_soft.keys(), 'pc': bd_pc_soft.values()})],\
    output, [dict_indexes, None, None], [width_1, width_2, width_3])
