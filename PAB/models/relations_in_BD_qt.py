from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QMessageBox

import app_logger
logger = app_logger.get_logger(__name__)

class RelField():
    def __init__(self, *args, **kwargs):
        self.type = kwargs.get("type")                        #тип связи
        self.table_tab = kwargs.get("table_tab")              #имя таблицы вкладки
        self.pkey_tab = kwargs.get("pkey_tab")                #имя столбца в таблице вкладки с primary key
        self.pkey_tab_idx =  kwargs.get("pkey_tab_idx")       #индекс столбца в таблице вкладки с primary key
        self.fkey_bt_tab = kwargs.get("fkey_bt_tab")          #имя столбца в таблице вкладки с внешним ключом к промежуточной таблице (для связей второго уровня)
        self.fkey_bt_tab_idx = kwargs.get("fkey_bt_tab_idx")  #индекс столбца в таблице вкладки с внешним ключом к промежуточной таблице (для связей второго уровня)
        self.table_bt = kwargs.get("table_bt")                #имя промежуточной таблицы (для связей второго уровня)
        self.pkey_bt = kwargs.get("pkey_bt")                  #имя столбца в промежуточной таблице с primary key
        self.pkey_bt_idx = kwargs.get("pkey_bt_idx")          #индекс столбца в промежуточной таблице с primary key
        self.fkey_tab = kwargs.get("fkey_tab")                #имя столбца в промежуточной таблице (для связей 2 уровня) или в основной таблице (для связей 1 уровня) с внешним ключом к таблице вкладки
        self.fkey_tab_idx = kwargs.get("fkey_tab_idx")        #индекс столбца в промежуточной таблице (для связей 2 уровня) или в основной таблице (для связей 1 уровня) с внешним ключом к таблице вкладки
        self.fkey_bag = kwargs.get("fkey_bag")               #имя столбца в промежуточной таблице (для связей 2 уровня) или в таблице вкладки (для связей 1 уровня) с внешним ключом к основной таблице
        self.fkey_bag_idx = kwargs.get("fkey_bag_idx")       #индекс столбца в промежуточной таблице (для связей 2 уровня) или в таблице вкладки (для связей 1 уровня) с внешним ключом к основной таблице
        self.table_bag =  kwargs.get("table_bag")              #имя основной таблицы
        self.pkey_bag = kwargs.get("pkey_bag")                #имя столбца в основной таблице с primary key
        self.pkey_bag_idx = kwargs.get("pkey_bag_idx")        #индекс столбца в основной таблице с primary key
        self.fkey_bt_bag = kwargs.get("fkey_bt_bag")          #имя столбца в промежуточной таблице с внешним ключом для основной таблицы
        self.fkey_bt_bag_idx = kwargs.get("fkey_bt_bag_idx")  #индекс столбца в промежуточной таблице с внешним ключом для основной таблицы
        self.table_prom_tab = kwargs.get("table_prom_tab")    #имя общей таблицы, связанной с таблицей вкладки
        self.pfkey_bt_tab = kwargs.get("pfkey_bt_tab")       #имя столбца в общей таблице, связанной с таблицей вкладки, хранящего внешний включ для промежуточной таблицы
        self.pfkey_bt_tab_idx = kwargs.get("pfkey_bt_tab_idx")#индекс столбца в общей таблице, связанной с таблицей вкладки, хранящего внешний включ для промежуточной таблицы
        self.pfkey_tab = kwargs.get("pfkey_tab")              #имя столбца в общей таблице, связанной с таблицей вкладки, хранящего внешний включ для  с таблицы вкладки
        self.pfkey_tab_idx = kwargs.get("pfkey_tab_idx")      #индекс столбца в общей таблице, связанной с таблицей вкладки, хранящего внешний включ для  с таблицы вкладки
        self.table_prom_bag = kwargs.get("table_prom_bag")    #имя общей таблицы, связанной с основной таблицей
        self.pfkey_bt_bag = kwargs.get("pfkey_bt_bag")        #имя столбца в общей таблице, связанной с основной таблицей, хранящего внешний включ для промежуточной таблицы
        self.pfkey_bt_bag_idx = kwargs.get("pfkey_bt_bag_idx")#индекс столбца в общей таблице, связанной с основной таблицей, хранящего внешний включ для промежуточной таблицы
        self.pfkey_bag = kwargs.get("pfkey_bag")              #имя столбца в общей таблице, связанной с основной таблицей, хранящего внешний включ для основной таблицы
        self.pfkey_bag_idx = kwargs.get("pfkey_bag_idx")      #индекс столбца в общей таблице, связанной с основной таблицей, хранящего внешний включ для основной таблицы

    def __str__(self):
        return f'Объект данных {self.__class__.__name__} для управления связью типа {self.type} между таблицами {self.table_tab} и {self.table_bag} '

    def __repr__(self):
        return (f'{self.__class__.__name__}'
        f' (type: {self.type}, table_tab: {self.table_tab},'
        f' pkey_tab: {self.pkey_tab}, fkey_tab: {self.fkey_tab}, table_bag: {self.table_bag},'
        f' pkey_bag: {self.pkey_bag}, fkey_bag: {self.fkey_bag},')

    #Метод, который формирует списки значений primary key (id) для таблиц вкладок (table_tab),
    #связанных со строкой, выбранной в основной таблице (table_bag)
    #1. <choose_id> - значение primary key (id) выбранного объекта
    def find_id_level(self, db, choose_id):
        if self.type in ("ManyTab-OneBt-ManyBt-OneBag", "ManyTab-OneBt-OneBt-ManyBag", "OneTab-ManyBt-ManyBt-OneBag", "OneTab-ManyBt-OneBt-ManyBag", "ManyTab-ManyBt-ManyBt-ManyBag", "ManyTab-OneBt-ManyBt-ManyBag", "OneTab-ManyBt-ManyBt-ManyBag", "ManyTab-ManyBt-OneBt-ManyBag", "ManyTab-ManyBt-ManyBt-OneBag"):
            id_list = self.find_id_level2(db, choose_id)
        elif self.type in ("OneTab-ManyBag", "ManyTab-OneBag", "ManyTab-ManyBag", "OneTab-NoBag" ):
            id_list = self.find_id_level1(db, choose_id)
        else:
            Error_str = (f'Значение для параметра rel.type = {self.type} задано некорректно, поиск не может быть выполнен')
            logger.error(Error_str)
            assert False, (Error_str)
        return id_list
        #Конец метода find_id_level1 класса <TabWindow>

    #"Подметод" метода <find_id_level> для связей первого уровня
    #("ManyTab-ManyBag", "ManyTab-OneBag", "OneTab-ManyBag", OneTab-NoBag)
    def find_id_level1(self, db, choose_id):
        if not choose_id:
            return []
        id_list = []
        if self.type == "OneTab-NoBag":
            id_list = [choose_id]
        else:
            #назначаем названия для таблиц и их полей, по которым будет осуществляться поиск
            _choose_dict = {
            "OneTab-ManyBag": (self.table_bag, self.fkey_tab, self.pkey_bag),
            "ManyTab-OneBag": (self.table_tab, self.pkey_tab, self.fkey_bag),
            "ManyTab-ManyBag": (self.table_prom_tab, self.pfkey_tab, self.pfkey_bag),}
            (table, id_seek, id_check) = _choose_dict[self.type]
            assert table not in ("", None), (f'Имя таблицы с информацией о primary key основной таблицы для связи {self.type} не задано или имеет нулевое значение: table = {table}')
            assert id_seek not in ("", None), (f'Имя столбца с информацией о primary key таблицы вкладки {self.table_tab}, для связи {self.type} не задано или имеет нулевое значение: id_seek = {id_seek}')
            assert id_check not in ("", None), (f'Имя столбца с информацией о primary key основной таблицы {self.table_bag}, для связи {self.type} не задано или имеет нулевое значение: id_check = {id_check}')
            #формируем шаблон поисковой строки для поиска списка значений, которые соответствуют
            #зачениям primary key таблицы вкладки, связанным с выбранной записью в основной таблице
            if db.driverName() == "QPSQL7":
                query_str = f"SELECT {table}.{id_seek} FROM {table} WHERE {table}.{id_check} = {choose_id} "
            else:
                query_str = f'SELECT {table}.{id_seek} FROM {table} WHERE {table}.{id_check} = {choose_id} '
            model_q = query_model(db, query_str)
            if model_q:
                #добавляем в список все id для таблицы вкладки, полученные по результатам запроса
                id_list = [model_q.record(idx).value(0) for idx in range(0, model_q.rowCount()) if model_q.record(idx).value(0) != ""]
            else:
                return []

        return list(sorted(set(id_list)))
        #Конец метода find_id_level1 класса <TabWindow>

    #"Подметод" метода <find_id_level> для связей второго уровня
    def find_id_level2(self, db, choose_id):
        if not choose_id:
            return []
        id_list = []
        _choose_dict = {
        "ManyTab-OneBt-ManyBt-OneBag": (self.table_bt, self.pkey_bt, self.fkey_bag, self.table_tab, self.pkey_tab, self.fkey_bt_tab),
        "ManyTab-OneBt-OneBt-ManyBag": (self.table_bag, self.fkey_bt_bag, self.pkey_bag, self.table_tab, self.pkey_tab, self.fkey_bt_tab),
        "ManyTab-OneBt-ManyBt-ManyBag": (self.table_prom_bag, self.pfkey_bt_bag, self.pfkey_bag, self.table_tab, self.pkey_tab, self.fkey_bt_tab),
        "ManyTab-ManyBt-ManyBt-ManyBag": (self.table_prom_bag, self.pfkey_bt_bag, self.pfkey_bag, self.table_prom_tab, self.pfkey_tab, self.pfkey_bt_tab),
        "ManyTab-ManyBt-OneBt-ManyBag": (self.table_bag, self.fkey_bt_bag, self.fkey_bag, self.table_prom_tab, self.pfkey_tab, self.pfkey_bt_tab),
        "ManyTab-ManyBt-ManyBt-OneBag": (self.table_bt, self.pkey_bt, self.fkey_bag, self.table_prom_tab, self.pfkey_tab, self.pfkey_bt_tab),
        "OneTab-ManyBt-ManyBt-OneBag": (self.table_bt, self.pkey_bt, self.fkey_bag, self.table_bt, self.fkey_tab, self.pkey_bt),
        "OneTab-ManyBt-OneBt-ManyBag": (self.table_bag, self.fkey_bt_bag, self.pkey_bag, self.table_bt, self.fkey_tab, self.pkey_bt),
        "OneTab-ManyBt-ManyBt-ManyBag": (self.table_prom_bag, self.pfkey_bt_bag, self.pfkey_bag, self.table_bt, self.fkey_tab, self.pkey_bt),
        }
        (table1, id_seek1, id_check1, table2, id_seek2, id_check2) = _choose_dict[self.type]
        assert table1 not in ("", None), (f'Имя таблицы с информацией о primary key основной таблицы для связи {self.type} не задано или имеет нулевое значение: table1 = {table1}')
        assert id_seek1 not in ("", None), (f'Имя столбца, связывающего основную таблицу {self.table_bag} с промежуточной {self.table_bt}, для связи {self.type} не задано или имеет нулевое значение: id_seek1 = {id_seek1}')
        assert id_check1 not in ("", None), (f'Имя столбца, со значениями, равными primary key основной таблицы {self.table_bag}, для связи {self.type} не задано или имеет нулевое значение: id_check1 = {id_check1}')
        assert table2 not in ("", None), (f'Имя таблицы с информацией о primary key промежуточной таблицы {self.table_bt} для связи {self.type} не задано или имеет нулевое значение: table2 = {table2}')
        assert id_seek2 not in ("", None), (f'Имя столбца, связывающего таблицу вкладки {self.table_tab} с промежуточной {self.table_bt}, для связи {self.type} не задано или имеет нулевое значение: id_seek2 = {id_seek2}')
        assert id_check2 not in ("", None), (f'Имя столбца, со значениями, равными primary key таблицы вкладки {self.table_tab}, для связи {self.type} не задано или имеет нулевое значение: id_check2 = {id_check2}')
        #для всех связей формируем шаблон поисковой строки для поиска списка значений, которые соответствуют
        #зачениям primary key промежуточной таблицы <table_bt>, связанным с выбранной записью в осной таблице <table_bag>
        if db.driverName() == "QPSQL7":
            query_str_bt = f" SELECT {table1}.{id_seek1} FROM {table1} WHERE {table1}.{id_check1} = {choose_id} "
        else:
            query_str_bt = f' SELECT {table1}.{id_seek1} FROM {table1} WHERE {table1}.{id_check1} = {choose_id} '
        model_q = query_model(db, query_str_bt)
        #добавляем в список все значения primary key промежуточной таблицы <table_bt>, полученные по результатам запроса
        id_list_bt = [model_q.record(idx).value(0) for idx in range(0, model_q.rowCount()) if model_q.record(idx).value(0) != ""]
        #формируем строку запроса, чтобы найти список значений primary key таблицы вкладки <table_tab>,
        #для записей, связанных с записями из промежуточной таблицы <table_bt> с primary key из <id_list_bt>
        if id_list_bt:
            #формируем строку из значений primary key
            str_id_list_bt = [str(_id) for _id in id_list_bt]
            pr_str = ",".join(str_id_list_bt)
            #добавляем строку с значениями primary key в строку запроса
            if db.driverName() == "QPSQL7":
                query_str = f"SELECT {table2}.{id_seek2} FROM {table2} WHERE {table2}.{id_check2} IN ({pr_str}) "
            else:
                query_str = f'SELECT {table2}.{id_seek2} FROM {table2} WHERE {table2}.{id_check2} IN ({pr_str}) '
            model_q = query_model(db, query_str)
            #добавляем в список все значения primary key для таблицы вкладки <table_tab>, полученные по результатам запроса
            id_list = [model_q.record(idx).value(0) for idx in range(0, model_q.rowCount()) if model_q.record(idx).value(0) != ""]
        return list(sorted(set(id_list)))
        #Конец метода find_id_level2 класса <TabWindow>

    #Метод, который формирует итоговую строку фильтрации для модели вкладки
    #1. <id_list> - список значений primary key для таблицы вкладки <table_tab>, связанных с выбранным объектом
    #2. <window> - объект окна вкладки
    def find_str_level(self, id_list, db):
        #назначаем названия для таблиц и их полей, по которым будет формироваться строка фильтрации
        Error_str = (f'Значение для параметра rel.type = {self.type} задано некорректно, поиск не может быть выполнен')
        assert self.type in ("OneTab-ManyBag", "ManyTab-OneBag","ManyTab-ManyBag", "OneTab-NoBag", "ManyTab-OneBt-ManyBt-OneBag", "ManyTab-OneBt-OneBt-ManyBag", "OneTab-ManyBt-ManyBt-OneBag", "OneTab-ManyBt-OneBt-ManyBag", "ManyTab-ManyBt-ManyBt-ManyBag", "ManyTab-OneBt-ManyBt-ManyBag", "OneTab-ManyBt-ManyBt-ManyBag", "ManyTab-ManyBt-OneBt-ManyBag", "ManyTab-ManyBt-ManyBt-OneBag"), (Error_str)
        table = self.table_tab
        id_check = self.pkey_tab
        #assert id_list != None, (f'Значение для параметра id_list = {id_list} задано некорректно, поиск не может быть выполнен')
        if len(id_list) == 0:
            if db.driverName() == "QPSQL7":
                filtr_str = f"{table}.{id_check} = 9999999 "
            else:
                filtr_str = f"{table}.{id_check} = '9999999' "
            logger.info(f"Так как список связанных сттрок пустой, использован фильтр - заглушка : {table}.{id_check} = '9999999' ")
        else:
            #Исключаем из списка 0, так он используется в служебных целях (для плашки не выбрано)
            str_id_list = [str(id) for id in id_list if id != 0]
            if db.driverName() == "QPSQL7":
                filtr_str = f'{table}.{id_check} = ' + f' OR {table}.{id_check} = '.join(str_id_list)
            else:
                filtr_str = f' {table}.{id_check} = ' + f' OR {table}.{id_check} = '.join(str_id_list)
        return filtr_str
        #Конец метода find_str_ff класса <TabWindow>

    def find_str_out_null(self, db):
    #назначаем названия для таблиц и их полей, по которым будет формироваться строка фильтрации
        table = self.table_tab
        id_check = self.pkey_tab
        #Фильр по-умолчанию чтобы не обображать нулевые строки-заглушки

        if db.driverName() == "QPSQL7":
            filtr_str = f"{table}.{id_check} != 0 "
        else:
            filtr_str = f'{table}.{id_check} != "0" '
        return filtr_str

def query_model(db, query_str, *args):
    model_q=QSqlQueryModel()
    query = QSqlQuery(db = db)
    query.prepare(query_str)
    if args:
        choose_id = args[0]
        query.bindValue(":choose_id", choose_id)
    if query.exec_():
        model_q.setQuery(query)
        return model_q
    else:
        #ПЕРЕПИСАТЬ ЧТОБЫ ЗДЕСЬ ВЫЗЫВАЛАСЬ ОШИБКА
        Error_str = f'Поискокой запрос {query_str} завершился ошибкой: {query.lastError().text()} '
        logger.warning(Error_str)
        return None

#Метод для определения имени объекта по его primary key (id)
#1. - <choose_id> - значение primary key (id) выбранного объекта
def find_choose_name(db, table_name, field_name, pkey_name, choose_id):
    if db.driverName() == "QPSQL7":
        query_str = f'''
        SELECT {table_name}.{field_name} 
        FROM {table_name} 
        WHERE {table_name}.{pkey_name}  = :choose_id '''
    else:
        query_str = f'''
        SELECT {table_name}.{field_name} 
        FROM {table_name} 
        WHERE {table_name}.{pkey_name}  = :choose_id '''

    model_q = query_model(db, query_str, choose_id)
    name = model_q.record(0).value(0)
    return name
    # Конец метода <find_name_asset> класса <TabWindow>

#Метод, для поиска списка строк, содержащих заданную пару значений primary key <id0> - <id1> в общей таблице с именем <table_name>
#1. <table_name> - имя общей таблицы (table_prom)
#2. <table_field0> - имя столбца, хранящего primary key основной таблицы (table_bag)
#3. <id0> - значение primary key основной таблицы (table_bag)
#4. <table_field1> - имя столбца, хранящего primary key таблицы вкладки (table_tab)
#5. <id1> - значение primary key таблицы вкладки (table_tab)
def find_item_row_MM(db, table_name, table_field0, id0, table_field1, id1):
    #Извлекаем из общей таблицы все строки
    if db.driverName() == "QPSQL7":
        query_str = f"SELECT {table_name}.{table_field0}, {table_name}.{table_field1} FROM {table_name} "
    else:
        query_str = f'SELECT {table_name}.{table_field0}, {table_name}.{table_field1} FROM {table_name} '

    model_q = query_model(db, query_str)
    row_list_choose = [row for row in range(0, model_q.rowCount()) if model_q.record(row).value(0) == id0 and model_q.record(row).value(1) == id1]
    if row_list_choose == []:
        Log_str = f'В таблице {table_name} не найдена строка(и), в которых {table_field0} = {id0} и {table_field1} = {id1} '
        logger.info(Log_str)
    return row_list_choose

#Метод, для поиска списка строк, содержащих все пары значений primary key <id0> - <любое значние> в общей таблице с именем <table_name>
#1. <table_name> - имя общей таблицы (table_prom)
#2. <table_field0> - имя столбца, хранящего primary key основной таблицы (table_bag)
#3. <id0> - значение primary key основной таблицы (table_bag)
#4. <table_field1> - имя столбца, хранящего primary key таблицы вкладки (table_tab)

#???????????????????????????
def find_item_row_MM_2(db, table_name, table_field0, id0, table_field1):
    #Извлекаем из общей таблицы все строки
    if db.driverName() == "QPSQL7":
        query_str = f"SELECT {table_name}.{table_field0}, {table_name}.{table_field1} FROM {table_name} "
    else:
        query_str = f'SELECT {table_name}.{table_field0}, {table_name}.{table_field1} FROM {table_name} '

    model_q = query_model(db, query_str)
    row_list_choose = [row for row in range(0, model_q.rowCount()) if model_q.record(row).value(0) == id0]
    if row_list_choose == []:
        Log_str = f'В таблице {table_name} не найдена строка(и), в которых {table_field0} = {id0} '
        logger.info(Log_str)
    return row_list_choose







#Метод, для поиска значения primary key последней добавленной в таблицу строки
#1. <table_name> - имя таблицы вкладки, в которой определяется значение primary key  добавленной записи
#2. <table_field> - имя поля, хранящего primary key таблицы
def find_add_item_id(db, table_name, table_field):
    if db.driverName() == "QPSQL7":
        query_str = f"SELECT {table_name}.{table_field} FROM {table_name} "
    else:
        query_str = f'SELECT {table_name}.{table_field} FROM {table_name} '

    model_q = query_model(db, query_str)
    id_list = [model_q.record(row).value(0) for row in range(0, model_q.rowCount())]
    return max(id_list)
