from collections import namedtuple
from models.manipulations_in_TabWin import TabModels
#from model_TabWin import TabWindow
from models.model_MainWin import MainWindow, TabWindow
from models.manipulations_in_MainWin import MainWinModel


#Именованный кортеж для автоматического создания qactionc в панели управления дополнительных окон
QActions = namedtuple('params_for_qaction', ['permreq', 'menu_position', 'chekable_status', 'cheked_status', 'icon', 'name', 'about', 'func_obj', 'func_kwargs'])
#Именованный кортеж для автоматического создания qactionc в панели управления дополнительных окон
TAB_QACTIONS = (
           QActions("e", ("tool", "context"), False, False, "plus.png", "Добавить", "Вставить пустую запись в таблицу", TabModels.new_rec,  {}),
           QActions("e", ("context"), False, False, "...configs.minus.png", "Удалить", "Удалить выбранную запись из таблицы", TabModels.del_rec, {}),
           QActions("w", ("context"), False, False, "chain--plus.png", "Связать", "Для выбранной записи установить связь с объектом", TabModels.join_rec, {}),
           QActions("w", ("context"), False, False, "chain-unchain.png", "Разделить", "Для выбранной записи разорвать связь с объектом", TabModels.unjoin_rec, {}),
           QActions("e", ("context"), False, False, "document-copy.png", "Клонировать", "Клонировать выбранную запись", TabModels.copy_rec, {}),
           QActions("r", ("tool"), False, False, "blue-document-break.png", "Отменить фильтр", "Отменить фильтр по объекту (показывать все записи таблицы)", TabModels.del_filtr, {}),
           QActions("r", ("tool"), False, False, "blue-document-bookmark.png", "Восстановить фильтр", "Восстановить фильтр по объекту", TabModels.add_filtr, {}),
           QActions("r", ("file"), False, False, "blue-document-word-text.png", "Экспортировать карточку в Word", "Экспортировать все данные объекта в Word", TabModels.start_export, {"where": "word", "what": "all"}),
           QActions("r", ("file"), False, False, "blue-document-word-tick.png", "Выборочно экспортировать в Word", "Экспортировать выбранные таблицы в Word", TabModels.start_export, {"where": "word", "what": "list"}),
           QActions("r", ("file"), False, False, "blue-document-excel.png", "Экспортировать карточку в Exell", "Экспортировать все данные объекта в Exell", TabModels.start_export,  {"where":"exell", "what": "all"}),
           QActions("r", ("file"), False, False, "blue-document-excel-tick.png", "Выборочно экспортировать в Exell", "Экспортировать выбранные таблицы в Exell", TabModels.start_export, {"where": "exell", "what": "list"}),
           QActions("r", ("tool"), True, True, "balloon-twitter-retweet.png", "Автообновление", "Включить автоматическое обновление вкладок при изменении в БД", TabWindow.update_tabs, {}),
           QActions("r", ("context"), False, False, "balloon-twitter-retweet.png", "Карточка выделенной записи", "Открыть карточку для выделенной записи", TabWindow.open_window, {}),
           )
#Именованный кортеж для автоматического создания qactionc в меню файл основного окна
MAIN_QACTIONS = (
           QActions("rw", ("file"),  False, False, "application-plus.png", "Аттестатам", "Открыть основное окно, прявязанное к аттестатам", MainWindow.open_main_window,  {"config_module_name": "attestatums"}),
           QActions("rw", ("file"), False, False, "application-plus.png", "Документам", "Открыть основное окно, прявязанное к документам", MainWindow.open_main_window,  {"config_module_name": "attdocs"}),
            QActions("rw", ("file"), False, False, "application-plus.png", "АРМ-ам", "Открыть основное окно, прявязанное к АРМ-ам", MainWindow.open_main_window,  {"config_module_name": "arms"}),
           QActions("rw", ("file"),  False, False, "application-plus.png", "ОРД", "Открыть основное окно, прявязанное к ОРД", MainWindow.open_main_window,  {"config_module_name": "ords"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "Помещениям", "Открыть основное окно, прявязанное к помещениям", MainWindow.open_main_window,  {"config_module_name": "rooms"}),
           QActions("rw", ("file"),  False, False, "application-plus.png", "СЗИ", "Открыть основное окно, прявязанное к СЗИ", MainWindow.open_main_window,  {"config_module_name": "szis"}),
           QActions("rw", ("file"),  False, False, "application-plus.png", "Ответственным", "Открыть основное окно, прявязанное к ответсвенным", MainWindow.open_main_window,  {"config_module_name": "responsibles"}),
           QActions("rw", ("file"),  False, False, "application-plus.png", "Учетным записям", "Открыть основное окно, прявязанное к учетным записям", MainWindow.open_main_window,  {"config_module_name": "users"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "Аттестатам РП", "Открыть основное окно, прявязанное к аттестатам режимных помещений", MainWindow.open_main_window,  {"config_module_name": "attestatumrps"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "Сертификатам", "Открыть основное окно, прявязанное к сертификатам", MainWindow.open_main_window,  {"config_module_name": "serts"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "Сотрудникам", "Открыть основное окно, прявязанное к списку сотрудников", MainWindow.open_main_window,  {"config_module_name": "peoples"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "Отделам", "Открыть основное окно, прявязанное к списку отделов", MainWindow.open_main_window,  {"config_module_name": "otdels"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "Службам", "Открыть основное окно, прявязанное к списку служб", MainWindow.open_main_window,  {"config_module_name": "servises"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Категории объектов", "Открыть основное окно, прявязанное к категориями объектов", MainWindow.open_main_window,  {"config_module_name": "akats"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Классы объектов", "Открыть основное окно, прявязанное к классам объектов", MainWindow.open_main_window,  {"config_module_name": "aklasses"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы объектов", "Открыть основное окно, прявязанное к типам объектов", MainWindow.open_main_window,  {"config_module_name": "atypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы документов", "Открыть основное окно, прявязанное к типам документов", MainWindow.open_main_window,  {"config_module_name": "dtypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы событий", "Открыть основное окно, прявязанное к типам событий", MainWindow.open_main_window,  {"config_module_name": "ddtypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы ОРД", "Открыть основное окно, прявязанное к типам ОРД", MainWindow.open_main_window,  {"config_module_name": "otypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы ответственных", "Открыть основное окно, прявязанное к типам ответственных", MainWindow.open_main_window,  {"config_module_name": "rtypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы СЗИ", "Открыть основное окно, прявязанное к типам СЗИ", MainWindow.open_main_window,  {"config_module_name": "stypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы РП", "Открыть основное окно, прявязанное к типам РП", MainWindow.open_main_window,  {"config_module_name": "rptypes"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Элементы СЗИ", "Открыть основное окно, прявязанное к элементам СЗИ", MainWindow.open_main_window,  {"config_module_name": "selements"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы статусов", "Открыть основное окно, прявязанное к типам статусов", MainWindow.open_main_window,  {"config_module_name": "astatuses"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы трудовых статусов", "Открыть основное окно, прявязанное к типам трудовых статусов", MainWindow.open_main_window,  {"config_module_name": "truds"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Номера территорий", "Открыть основное окно, прявязанное к номерам территорий", MainWindow.open_main_window,  {"config_module_name": "territores"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Пометки конфиденциальности", "Открыть основное окно, прявязанное к пометкам конфиденциальности", MainWindow.open_main_window,  {"config_module_name": "secrets"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Названия форм", "Открыть основное окно, прявязанное к названиям форм", MainWindow.open_main_window,  {"config_module_name": "forms"}),
           QActions("rw", ("file"),  False, False, "application-plus.png", "ТС", "Открыть основное окно, прявязанное к ТС", MainWindow.open_main_window,  {"config_module_name": "tehnos"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Типы ТС", "Открыть основное окно, прявязанное к типам ТС", MainWindow.open_main_window,  {"config_module_name": "ttypes"}),
           QActions("r", ("file"),  False, False, "application-plus.png", "ПО с wiki", "Открыть основное окно, прявязанное к ПО с wiki", MainWindow.open_main_window,  {"config_module_name": "bd_softs"}),
           QActions("rw", ("file"),  False, False, "application-plus.png", "ПО с ПК", "Открыть основное окно, прявязанное к ПО с ПК", MainWindow.open_main_window,  {"config_module_name": "pc_softs"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Категория ПО", "Открыть основное окно, прявязанное к категориям ПО", MainWindow.open_main_window,  {"config_module_name": "softcats"}),
           QActions("s", ("file"),  False, False, "application-plus.png", "Названия должностей", "Открыть основное окно, прявязанное к названиям должностей", MainWindow.open_main_window,  {"config_module_name": "positions"}),
           QActions("ex", ("file"),  False, False, "blue-document-word-array.png", "Экспортировать данные в Word", "Экспортировать все данные объекта в Word",  MainWinModel.start_export, {"where": "word"}),
           QActions("ex", ("file"),  False, False, "blue-document-excel-arrow.png", "Экспортировать данные в Exell", "Экспортировать все данные объекта в Exell", MainWinModel.start_export,  {"where":"exell"}),
           QActions("ex", ("file"),  False, False, "notebook--arrow.png", "Экспортировать данные в json", "Экспортировать все данные объекта в json", MainWinModel.start_export,  {"where":"json"}),
           QActions("ex", ("file"),  False, False, "notebook--arrow.png", "Экспортировать данные в csv", "Экспортировать все данные объекта в csv", MainWinModel.start_export,  {"where":"csv"}),
           QActions("im", ("file"),  False, False, "blue-document-excel-plus.png", "Импортировать данные из Exell", "Импортировать все данные из Exell", MainWinModel.start_import, {"where":"exell", "what": "add"}),
           QActions("im", ("file"),  False, False, "notebook--plus.png", "Импортировать данные из json", "Импортировать все данные из json", MainWinModel.start_import, {"where":"json", "what": "add"}),
           QActions("up", ("file"),  False, False, "blue-document-excel-pencill.png", "Обновить данными из Exell", "Обновить данными из Exell", MainWinModel.start_import, {"where":"exell", "what": "update"}),
           QActions("up", ("file"),  False, False, "notebook--pencil.png", "Обновить данными из json", "Обновить данными из json", MainWinModel.start_import, {"where":"json", "what": "update"}),
           QActions("up", ("file"),  False, False, "blue-document-excel-pencill.png", "Обновить данными из Exell", "Обновить данными из Exell", MainWinModel.start_auto_update, {"where":"exell", "what": "update"}),
           QActions("r", ("tool", "context"), False, False, "book-open-text-image.png", "Карточка", "Открыть карточку для выбранной записи", MainWindow.open_tab_window, {}),
           QActions("r", ("tool", "context"), False, False, "plus.png", "Добавить", "Вставить пустую запись в таблицу", MainWindow.new_rec_window,  {}),
           QActions("r", ("context"), False, False, "minus.png", "Удалить", "Удалить выбранную запись из таблицы", MainWinModel.del_rec, {}),
            )
