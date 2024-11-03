from models.manipulations_in_TabWin import MapperField

#В файле хранятся конструкции класса  <MapperField> (описание полей см.в определении класса),
#определяющие основу для создания полей ввода/вывода мэппера в табулированных
#дополнительных окнах
# Поля для вкладки "Объект"
asset_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "assets", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "year", index_map = 1, lable = "Год", table = "assets", pkey = "id", pkey_idx = 0, column = "year", type = "edit", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 2, lable = "Тип объекта", table = "atypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 3, lable = "Название объекта", table = "assets", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "kat_id", index_map = 4, lable = "Категория объекта", table = "akats", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "klass_id", index_map = 5, lable = "Класс объекта", table = "aklasses", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "status_id", index_map = 6, lable = "Статус", table = "astatuses", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Аттестат"
att_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "attestatums", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Название аттестата", table = "attestatums", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 2, lable = "Номер аттестата", table = "attestatums", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "begin", index_map = 3, lable = "Действует с", table = "attestatums", pkey = "id", pkey_idx = 0, column = "begin", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "end", index_map = 4, lable = "Действует по", table = "attestatums", pkey = "id", pkey_idx = 0, column = "end", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "inv", index_map = 5, lable = "Инвентарный", table = "attestatums", pkey = "id", pkey_idx = 0, column = "inv", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "secret_id", index_map = 6, lable = "Пометка", table = "secrets", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "asset_id", index_map = 7, lable = "Объект", table = "assets", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Помещение"
room_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "rooms", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 1, lable = "Номер помещения", table = "rooms", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "terr_id", index_map = 2, lable = "Территория", table = "territores", pkey = "id", pkey_idx = 0, column = "numb", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "floor", index_map = 3, lable = "Этаж", table = "rooms", pkey = "id", pkey_idx = 0, column = "floor", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "osi", index_map = 4, lable = "Оси", table = "rooms", pkey = "id", pkey_idx = 0, column = "osi", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "attRP_id", index_map = 5, lable = "Аттестат РП", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "full_name", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Документы"
doc_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "attdocs", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 1, lable = "Тип", table = "dtypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "typed_id", index_map = 2, lable = "Категория", table = "ddtypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 3, lable = "Название документа", table = "attdocs", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "full_name", index_map = 4, lable = "Полное название документа", table = "attdocs", pkey = "id", pkey_idx = 0, column = "full_name", type = "calc", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 5, lable = "Номер документа", table = "attdocs", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "begin", index_map = 6, lable = "Дата, от", table = "attdocs", pkey = "id", pkey_idx = 0, column = "begin", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "inv", index_map = 7, lable = "Инвентарный", table = "attdocs", pkey = "id", pkey_idx = 0, column = "inv", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "secret_id", index_map = 8, lable = "Пометка", table = "secrets", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "ТС"
tehno_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "tehnos", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 1, lable = "Тип ТС", table = "ttypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 2, lable = "Название ТС", table = "tehnos", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "model", index_map = 3, lable = "Модель ТС", table = "tehnos", pkey = "id", pkey_idx = 0, column = "model", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 4, lable = "Номер ТС", table = "tehnos", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "sz", index_map = 5, lable = "Номер СЗ", table = "tehnos", pkey = "id", pkey_idx = 0, column = "SZ", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "attdoc_id", index_map = 6, lable = "Заключение", table = "attdocs", pkey = "id", pkey_idx = 0, column = "full_name", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "arm_id", index_map = 7, lable = "АРМ", table = "arms", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "ОРД"
ord_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "ords", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 1, lable = "Тип ОРД", table = "otypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "typed_id", index_map = 2, lable = "Тип док-та", table = "ddtypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 3, lable = "Название ОРД", table = "ords", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "full_name", index_map = 4, lable = "Полное название ОРД", table = "ords", pkey = "id", pkey_idx = 0, column = "full_name", type = "calc", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 5,  lable = "Номер ОРД", table = "ords", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "begin", index_map = 6, lable = "Дата, от", table = "ords", pkey = "id", pkey_idx = 0, column = "begin", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "end", index_map = 7, lable = "Дата, до", table = "ords", pkey = "id", pkey_idx = 0, column = "end", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "inv", index_map = 8, lable = "Инвентарный", table = "ords", pkey = "id", pkey_idx = 0, column = "inv", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "secret_id", index_map = 9, lable = "Пометка", table = "secrets", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "СЗИ"
szi_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "szis", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "element_id", index_map = 1, lable = "Название элемента СЗИ", table = "selements", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 2, lable = "Номер  элемента СЗИ", table = "SZIs", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "szz", index_map = 3, lable = "СЗЗ элемента СЗИ", table = "szis", pkey = "id", pkey_idx = 0, column = "szz", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "sert_id", index_map = 4, lable = "Сертификат, номер", table = "serts", pkey = "id", pkey_idx = 0, column = "numb", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Ответственные"
resp_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "responsibles", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Полное наименование ответсвенности", table = "responsibles", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 2, lable = "Тип ответсвенности", table = "rtypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "people_id", index_map = 3, lable = "ФИО ответственного", table = "peoples", pkey = "id", pkey_idx = 0, column = "fio", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "ord_id", index_map = 4, lable = "ОРД-основание", table = "ords", pkey = "id", pkey_idx = 0, column = "full_name", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Сотрудники"
people_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "peoples", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "card", index_map = 1, lable = "Табельный номер", table = "peoples", pkey = "id", pkey_idx = 0, column = "card", type = "edit", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "pos_id", index_map = 2, lable = "Должность", table = "positions", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "fio", index_map = 3, lable = "ФИО", table = "peoples", pkey = "id", pkey_idx = 0, column = "fio", type = "edit", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "tel", index_map = 4, lable = "вн. телефон", table = "peoples", pkey = "id", pkey_idx = 0, column = "tel", type = "edit", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "otd_id", index_map = 5, lable = "Отдел", table = "otdels", pkey = "id", pkey_idx = 0, column = "numb", type = "combo", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "trud_id", index_map = 6, lable = "Статус", table = "truds", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "form_id", index_map = 7, lable = "Форма", table = "forms", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "yes",  wid = {"obj": ""}),
            )
# Поля для вкладки "Учетные записи"
user_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "users", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Название учетной записи", table = "users", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 2, lable = "Тип учетной записи", table = "users", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "people_id", index_map = 3, lable = "ФИО", table = "peoples", pkey = "id", pkey_idx = 0, column = "fio", type = "combo", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "ord_id", index_map = 4, lable = "ОРД", table = "ords", pkey = "id", pkey_idx = 0, column = "full_name", type = "combo", check = "yes",  wid = {"obj": ""}),
            MapperField(column_map = "arm_id", index_map = 5, lable = "АРМ", table = "arms", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "yes",  wid = {"obj": ""}),
            )
# Поля для вкладки "Аттестат РП"
attRP_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Наименование аттестата РП", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "full_name", index_map = 2, lable = "Полное наименование аттестата РП", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "full_name", type = "calc", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 3, lable = "Номер аттестата", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "begin", index_map = 4, lable = "Дата, от", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "begin", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "end", index_map = 5, lable = "Дата, до", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "end", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "inv", index_map = 6, lable = "Инвентарный", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "inv", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "secret_id", index_map = 7, lable = "Пометка", table = "secrets", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 8, lable = "Тип помещения", table = "rptypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "spets", index_map = 9, lable = "Спец.помещение", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "spets", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "vp", index_map = 10, lable = "Выделенное", table = "attestatumrps", pkey = "id", pkey_idx = 0, column = "vp", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Сертификаты"
sert_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "serts", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 1, lable = "Номер сертификата", table = "serts", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "begin", index_map = 2, lable = "Дата внесения в реестр", table = "serts", pkey = "id", pkey_idx = 0, column = "begin", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "end", index_map = 3, lable = "Срок действия", table = "serts", pkey = "id", pkey_idx = 0, column = "end", type = "date", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type_id", index_map = 4, lable = "Тип СЗИ", table = "stypes", pkey = "id", pkey_idx = 0, column = "type", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 5, lable = "Наименование средства(шифр)", table = "serts", pkey = "id", pkey_idx = 0, column = "name", check = "no", type = "edit", wid = {"obj": ""}),
            MapperField(column_map = "req_doc", index_map = 6, lable = "Документы, требованиям которых соответсвует", table = "serts", pkey = "id", pkey_idx = 0, column = "req_doc", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "scheme", index_map = 7, lable = "Схема сертификации", table = "serts", pkey = "id", pkey_idx = 0, column = "scheme", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "end_tp", index_map = 8, lable = "Окончание ТП", table = "serts", pkey = "id", pkey_idx = 0, column = "end_tp", type = "date", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Отделы"
otdel_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "otdels", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "servise_id", index_map = 1, lable = "Служба", table = "servises", pkey = "id", pkey_idx = 0, column = "numb", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 2, lable = "Номер", table = "otdels", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 3, lable = "Название", table = "otdels", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "lboss_id", index_map = 4, lable = "Начальник отдела", table = "peoples", pkey = "id", pkey_idx = 0, column = "fio", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Службы"
servise_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "servises", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 1, lable = "Номер", table = "servises", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 2, lable = "Название", table = "servises", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "boss_id", index_map = 3, lable = "Руководитель службы", table = "peoples", pkey = "id", pkey_idx = 0, column = "fio", type = "combo", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Категории объектов"
akat_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "akats", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Категория", table = "akats", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Классы объектов"
aklass_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "aklasses", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Классы", table = "aklasses", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Статусы объектов"
astatus_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "astatuses", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Статус", table = "astatuses", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Типы объектов"
atype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "atypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип объекта", table = "atypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Типы событий"
ddtype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "ddtypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип события", table = "ddtypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "Типы документов"
dtype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "dtypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип документа", table = "dtypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Типы ОРД"
otype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "otypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип ОРД", table = "otypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Типы режимных помещений"
rptype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "rptypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип РП", table = "rptypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Типы ответственных"
rtype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "rtypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип ответственного", table = "rtypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "kom", index_map = 2, lable = "Описание", table = "rtypes", pkey = "id", pkey_idx = 0, column = "kom", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Названия элементов СЗИ"
selement_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "selements", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Название элемента", table = "selements", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Названия элементов СЗИ"
stype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "stypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Категории СЗИ", table = "stypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Трудовые статусы"
trud_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "truds", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Статус", table = "truds", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Трудовые статусы"
terr_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "territores", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "numb", index_map = 1, lable = "Номер", table = "territores", pkey = "id", pkey_idx = 0, column = "numb", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Трудовые статусы"
form_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "forms", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Форма", table = "forms", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Трудовые статусы"
secret_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "secrets", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Пометка", table = "secrets", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "Типы ТС"
ttype_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "ttypes", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Типы ТС", table = "ttypes", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
              )
# Поля для вкладки "ПО БД"
bd_soft_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Название ПО", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 2, lable = "Тип ПО", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "catigory_id", index_map = 3, lable = "Категория", table = "softcats", pkey = "id", pkey_idx = 0, column = "catigory", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "legality", index_map = 4, lable = "Легальность", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "legality", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "developer", index_map = 5, lable = "Производитель", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "developer", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "license", index_map = 6, lable = "Лицензия", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "license", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "site", index_map = 7, lable = "Сайт", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "site", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "wiki_page", index_map = 8, lable = "WiKi-страница", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "wiki_page", type = "edit", check = "no", wid = {"obj": ""}),)

# Поля для вкладки "ПО БД" (таблица хранения)
pc_soft_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "pc_softs", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Название ПО", table = "pc_softs", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "yes", wid = {"obj": ""}, corr_import = "corr_edit", corr_table = "in_softs"),
            MapperField(column_map = "version", index_map = 2, lable = "Версия ПО", table = "pc_softs", pkey = "id", pkey_idx = 0, column = "version", type = "edit", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "install", index_map = 3, lable = "Установлено", table = "pc_softs", pkey = "id", pkey_idx = 0, column = "install", type = "date", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "soft_id", index_map = 4, lable = "Название БД", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "yes", wid = {"obj": ""}, corr_import = "corr_combo", corr_table = ""),
            MapperField(column_map = "arm_id", index_map = 5, lable = "АРМ установки", table = "arms", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "corr", index_map = 6, lable = "Корреляция", table = "pc_softs", pkey = "id", pkey_idx = 0, column = "corr", type = "edit", check = "yes", wid = {"obj": ""}, corr_import = "corr_corr", corr_table = ""),
            )
# Поля для вкладки "загрузка ПО БД" (таблица загрузки)
in_soft_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "in_softs", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Название ПО", table = "in_softs", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "version", index_map = 2, lable = "Версия ПО", table = "in_softs", pkey = "id", pkey_idx = 0, column = "version", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "install", index_map = 3, lable = "Установлено", table = "in_softs", pkey = "id", pkey_idx = 0, column = "install", type = "edit", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "soft_id", index_map = 4, lable = "Название БД", table = "bd_softs", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "arm_id", index_map = 5, lable = "АРМ установки", table = "arms", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "corr", index_map = 6, lable = "Корреляция", table = "in_softs", pkey = "id", pkey_idx = 0, column = "corr", type = "edit", check = "no", wid = {"obj": ""}),
            )
# Поля для вкладки "категории БД"
soft_cats_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "softcats", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "catigory", index_map = 1, lable = "Категория", table = "softcats", pkey = "id", pkey_idx = 0, column = "catigory", type = "edit", check = "no", wid = {"obj": ""}),
            )

# Поля для вкладки "АРМы"
arms_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "arms", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "type", index_map = 1, lable = "Тип", table = "arms", pkey = "id", pkey_idx = 0, column = "type", type = "edit", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 2, lable = "Имя ПК", table = "arms", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "otdel_id", index_map = 3, lable = "Отдел", table = "otdels", pkey = "id", pkey_idx = 0, column = "numb", type = "combo", check = "yes", wid = {"obj": ""}),
            MapperField(column_map = "asset_id", index_map = 4, lable = "Объект", table = "assets", pkey = "id", pkey_idx = 0, column = "name", type = "combo", check = "yes", wid = {"obj": ""}),
            )

# Поля для вкладки "Названия должностей"
positions_list = (
            MapperField(column_map = "id", index_map = 0, lable = "ID", table = "positions", pkey = "id", pkey_idx = 0, column = "id", type = "spin", check = "no", wid = {"obj": ""}),
            MapperField(column_map = "name", index_map = 1, lable = "Названия должностей", table = "positions", pkey = "id", pkey_idx = 0, column = "name", type = "edit", check = "no", wid = {"obj": ""}),
              )

mapper_lists = {
"assets": asset_list, "attestatums": att_list, "rooms": room_list,
"attdocs": doc_list, "ords": ord_list, "szis": szi_list,
"responsibles": resp_list, "peoples": people_list, "users": user_list, "attestatumrps": attRP_list,
"serts": sert_list, "otdels": otdel_list, "servises": servise_list,
"akats": akat_list, "aklasses": aklass_list,
"astatuses": astatus_list, "atypes": atype_list, "ddtypes": ddtype_list,
"dtypes": dtype_list, "otypes": otype_list, "rptypes": rptype_list,
"rtypes": rtype_list, "selements": selement_list, "stypes": stype_list,
"truds": trud_list, "territores": terr_list, "forms": form_list,
"secrets": secret_list, "tehnos": tehno_list, "ttypes": ttype_list,
"bd_softs": bd_soft_list, "pc_softs": pc_soft_list, "softcats": soft_cats_list,
"in_softs": in_soft_list, "arms": arms_list, "positions": positions_list}
