import os
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QGridLayout, QWidget, QCheckBox, QVBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import  Qt
from PyQt5.QtCore import QDate
from pathlib import Path
from models.read_write.manipulate_exell import read_myexell, read_myexell_head, read_myexell_sheet
from models.read_write.manipulate_word import read_myword
from models.read_write.manipulate_json import read_myjson, read_myjson_head, read_myjson_sheet, write_json,  read_json
import app_logger
logger = app_logger.get_logger(__name__)

class ImportModel():
    FILE_programm = {"word": "Текстовый редактор Word (*.docx)", "exell": "Книга exell (*.xlsx)", "json": "Конфигурационный файл (*.txt)", "txt": "Конфигурационный файл (*.txt)"}
    FILE_end_of_name = {"word": ".docx", "exell": ".xlsx", "json": ".txt"}
    FILE_import_command = {"word": read_myword, "exell": read_myexell, "json": read_myjson}
    FILE_head_command = {"exell": read_myexell_head, "json": read_myjson_head}
    FILE_sheet_command = {"exell": read_myexell_sheet, "json": read_myjson_sheet}

    def __init__(self, window, where: str, file_name: str, location: str,  bd_head = None, sheet = None, etalon_dict = {}, first_row = None, prymary_col = None, uniq_db_col = None,  uniq_file_col = None, not_import_col = [], calc_col = [], combo_col = [], row_in_pack = 10):
        self.window = window
        self.where = where
        self.location = location
        self.file_name = file_name
        self.bd_head = bd_head
        self.sheet = sheet
        self.etalon_dict = etalon_dict
        self.first_row = first_row
        self.prymary_col = prymary_col
        self.uniq_db_col = uniq_db_col
        self.uniq_file_col = uniq_file_col
        self.not_import_col = not_import_col
        self.calc_col = calc_col
        self.combo_col = combo_col
        self.row_in_pack = row_in_pack
        #Заголовок для таблицы, фиксирующей изиенения в БД
        self.check_table = [["Уникальный столбец", "Уникальное значение", "Название изменившегося столбца", "Было в БД", "Стало-бы", "Стало в БД"],]
        self.stop = False



    def choose_file_name(self):
        #Рсчитываем полный путь
        file_name = self.file_name +  ImportModel.FILE_end_of_name.get(self.where, "")
        full_path = os.path.join(Path.cwd(), self.location, file_name)
        file_name, _ = QFileDialog.getOpenFileName(self.window, "Считать файл с именем ...", str(full_path),  ImportModel.FILE_programm[self.where],)
        self.file_name = file_name
        if self.file_name:
            return True

    def read_head(self):
        #выбираем подходящую функцию и запускаем ее
        function_for_read = ImportModel.FILE_head_command[self.where]
        head = function_for_read(self.file_name, self.sheet, self.first_row)
        if head:
            return head
        else:
            Err_str = f'Не удалось считать заголовок табличных данных из выбранного файла'
            logger.error(Err_str)
            return None

    def read_sheets(self):
        try:
            #выбираем подходящую функцию и запускаем ее
            function_for_read = ImportModel.FILE_sheet_command[self.where]
            sheets = function_for_read(self.file_name)
            return sheets
        except Exception as other:
            Err_str = f'Не удалось считать данные из выбранного файла. Ошибка {other}'
            logger.error(Err_str)
            return None

    #Метод, который экспортирует данные в файл зажанного типа
    def read_data_for_import(self):
        #выбираем подходящую функцию и запускаем ее
        try:
            #выбираем подходящую функцию и запускаем ее
            function_for_import = ImportModel.FILE_import_command[self.where]
            import_data = function_for_import(self.file_name, self.sheet, self.first_row)
            import_data.del_enter_from_header()
            import_data.choose_data_with_header(self.etalon_dict)
            import_data.change_date_in_data_table(self.etalon_dict)
            import_data.data_table = self.delete_null_records(import_data.data_table)
            return import_data
        except Exception as other:
            Err_str = f'Не удалось считать данные из выбранного файла. Ошибка {other}'
            logger.error(Err_str)
            return False

    #Метод удаляеит из импортированных данных нулевые строчки
    def delete_null_records(self, import_data):
        new_import_data = []
        import collections
        from collections import Counter
        for record in import_data:
            cnt = collections.Counter(record)
            if cnt[None] < len(record):
                new_import_data.append(record)
            else:
                pass
        return new_import_data

    #Метод, который сохраняет модель импорта в файл
    def save(self, window, table_name):
        import_params = {
        "file_name": self.file_name,
        "where": self.where,
        "bd_head": self.bd_head,
        "sheet": self.sheet,
        "etalon_dict": self.etalon_dict,
        "first_row": self.first_row,
        "prymary_col": self.prymary_col,
        "uniq_db_col": self.uniq_db_col,
        "uniq_file_col": self.uniq_file_col,
        "not_import_col": self.not_import_col,
        "calc_col": self.calc_col,
        "combo_col": self.combo_col,
        }
        file_for_save = f'import_model-{table_name}-{QDate.currentDate().toString("dd.MM.yyyy")}.txt'
        #Проверяем, есть ли заданная директория, если нет - создаем ее
        if not Path("import_models").exists():
            Path("import_models").mkdir(parents = True)
        full_path = os.path.join(Path.cwd(), "import_models", file_for_save)
        #Активируем экспорт
        write_json(import_params, full_path)

    #Метод, который считывает модель импорта из файла
    def load(self, file_name):
        params = read_json(file_name)
        self.file_name = params.get("file_name", None)
        self.where  = params.get("where", None)
        self.bd_head  = params.get("bd_head", None)
        self.sheet  = params.get("sheet", None)
        self.first_row  = params.get("first_row", None)
        self.prymary_col  = params.get("prymary_col", None)
        self.uniq_db_col  = params.get("uniq_db_col", None)
        self.uniq_file_col  = params.get("uniq_file_col", None)
        self.not_import_col  = params.get("not_import_col", None)
        self.calc_col  = params.get("calc_col", None)
        self.combo_col  = params.get("combo_col", None)
        etalon_dict  = params.get("etalon_dict", None)
        self.etalon_dict = {int(key): item for key, item in etalon_dict.items()}

#Только для exell. Определяет номер строки файла, в которой хранится заголовок таблицы
class DialogImportHead(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Импорт ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        first_row_edit = QLineEdit()
        layout = QVBoxLayout()
        message_1 = QLabel("1. Введите номер строки exell-файла, в которой записаны названия столбцов (нумерация начинается с 1).")
        layout.addWidget(message_1)
        layout.addWidget(first_row_edit)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        #Присваиваем окну объект поля, чтобы обращаться к нему извне
        self.first_obj = first_row_edit

#Только для exell. Определяет название вкладки, в которой хранятся данные для импорта
class DialogImportSheetName(QDialog):
    def __init__(self, sheet_names):
        super().__init__()
        self.setWindowTitle("Импорт ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        sheet_edit = QComboBox()
        sheet_edit.setPlaceholderText(f'...')
        sheet_edit.addItems(sheet_names)
        sheet_edit.setCurrentIndex(-1)
        layout = QVBoxLayout()
        message_1 = QLabel("1. Выбирете название вкладки, из которой необходимо импортировать данные в БД .")
        layout.addWidget(message_1)
        layout.addWidget(sheet_edit)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        #Присваиваем окну объект поля, чтобы обращаться к нему извне
        self.sheet_edit = sheet_edit

#Сопоставление между столбцами БД и таблицы файла
class DialogImport(QDialog):
    def __init__(self, head_lables, calc_colums, import_head, what):
        date_formats = ["dd.MM.yyyy", "dd-MM-yyyy", "dd.MM.yy", "dd-MM-yy", "yyyy.MM.dd", "yyyy-MM-dd",]
        super().__init__()
        self.setWindowTitle("Импорт ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        check_layout = QGridLayout()
        check_box_box = QWidget()
        #Готовим словари для записи объектов взаимодействия с пользователем
        check_dict = {}
        edit_dict = {}
        date_dict = {}
        for idx, head in enumerate(head_lables):
            lable = QLabel(head)
            edit = QComboBox()
            edit.setPlaceholderText(f'...')
            edit.addItems(import_head)
            combo = QComboBox()
            combo.setPlaceholderText(f'...')
            combo.setCurrentIndex(-1)
            combo.addItems(date_formats)
            check_box = QCheckBox()
            check_box.setCheckState(Qt.Unchecked)
            if idx in calc_colums:
                edit.setCurrentIndex(0)
                edit.setDisabled(True)
                combo.setDisabled(True)
                check_box.setDisabled(True)
            else:
                edit.setCurrentIndex(-1)
            check_dict[idx] = check_box
            edit_dict[idx] = edit
            date_dict[idx] = combo
            check_layout.addWidget(lable, idx, 0, 1, 1, Qt.Alignment(0))
            check_layout.addWidget(edit, idx, 1, 1, 1, Qt.Alignment(0))
            check_layout.addWidget(check_box, idx, 2, 1, 1, Qt.Alignment(0))
            check_layout.addWidget(combo, idx, 3, 1, 1, Qt.Alignment(0))
        check_box_box.setLayout(check_layout)
        layout = QVBoxLayout()
        message_1 = QLabel("1. Выбирете столбец из БД, который не должен меняться при обновлении БД данными из файла (рекомендуется - ID)")
        message_2 = QLabel("2. Выбирете столбец из файла, с которым необходимо сопоставить  столбец из БД, который не должен меняться при обновлении БД данными из файла")
        message_3 = QLabel("3. Выберете названия столбцов из импортируемого файла, соответствующие указанным названиям столбцов в БД.")
        message_4 = QLabel("4. Отметьте позиции, которым соответсвуют столбцы с датами.")
        message_5 = QLabel("5. Выбирете используемый в импортирумом файле формат даты.")
        if what == "update":
            uniq_db = QComboBox()
            uniq_db.setPlaceholderText(f'...')
            uniq_db.setCurrentIndex(-1)
            uniq_db.addItems(head_lables)
            uniq_file = QComboBox()
            uniq_file.setPlaceholderText(f'...')
            uniq_file.setCurrentIndex(-1)
            uniq_file.addItems(import_head)
            layout.addWidget(message_1)
            layout.addWidget(uniq_db)
            layout.addWidget(message_2)
            layout.addWidget(uniq_file)
            self.uniq_file = uniq_file
            self.uniq_db = uniq_db
        layout.addWidget(message_3)
        layout.addWidget(message_4)
        layout.addWidget(message_5)
        layout.addWidget(check_box_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        #Присваиваем окну словари с объектами полей, чтобы обращаться к ним извне
        self.check_dict = check_dict
        self.edit_dict = edit_dict
        self.date_dict = date_dict

#Определяет, что планируется обновлять в процессе авто-импорта
class DialogImportConfigList(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Автоматический импорт ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        edit = QComboBox()
        edit.setPlaceholderText(f'...')
        edit.addItems(("Таблицы текущего(активного) окна", "Других таблиц"))
        edit.setCurrentIndex(-1)
        layout = QVBoxLayout()
        message_1 = QLabel("Планируется импорт и обновление: ")
        layout.addWidget(message_1)
        layout.addWidget(edit)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        #Присваиваем окну объект поля, чтобы обращаться к нему извне
        self.edit = edit

#Определяет, какие таблицы и с помощью каких моделей импорта планируется автоматически обновлять
class DialogImportConfigList2(QDialog):
    def __init__(self, tables):
        super().__init__()
        self.setWindowTitle("Автоматический импорт ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        message_1 = QLabel("Выбирете название таблицы, которую планируется обновить и подберите для нее файл с параметрами импорта.")
        layout.addWidget(message_1)
        self.combo_dict = {}
        self.edit_dict = {}
        for idx in range(5):
            combo = QComboBox()
            combo.setPlaceholderText(f'...')
            combo.addItems(tables)
            combo.setCurrentIndex(-1)
            self.combo_dict[idx] = combo
            self.create_act(combo, idx)
            edit = QLineEdit()
            self.edit_dict[idx] = edit
            layout.addWidget(combo)
            layout.addWidget(edit)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    #Определяет имя файла, из которого следует считать данные для импорта
    def choose_file(self, idx):
        file, _ = QFileDialog.getOpenFileName(self, "Выбрать файл с параметрами модели ...", "import_model", " (*.txt)",)
        self.edit_dict[idx].setText(file)

    def create_act(self, combo, idx):
        combo.currentIndexChanged.connect(lambda: self.choose_file(idx))
