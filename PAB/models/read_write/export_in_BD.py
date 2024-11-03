import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from models.read_write.manipulate_exell import create_myexell
from models.read_write.manipulate_word import create_myword
from models.read_write.manipulate_json import create_myjson
from models.read_write.manipulate_csv import create_mycsv
from pathlib import Path

class ExportModel():
    FILE_programm = {"word": "Текстовый редактор Word (*.docx)",
                     "exell": "Книга exell (*.xlsx)",
                     "json": "Конфигурационный файл (*.txt)",
                     "csv": "Конфигурационный файл (*.txt)"}
    FILE_end_of_name = {"word": ".docx", "exell": ".xlsx", "json": ".txt", "csv": ".csv"}
    FILE_command = {"word": create_myword, "exell": create_myexell, "json": create_myjson, "csv": create_mycsv}

    def __init__(self, window, export_sets: list, where: str, file_name: str, location: str):
        self.window = window
        self.export_sets = export_sets
        self.where = where
        self.location = location
        self.file_name = file_name

    def choose_file_name(self):
        #Проверяем, есть ли заданная директория, если нет - создаем ее
        if not Path(self.location).exists():
            Path(self.location).mkdir(parents = True)
        #Рсчитываем полный путь
        file_name = self.file_name +  ExportModel.FILE_end_of_name[self.where]
        full_path = os.path.join(Path.cwd(), self.location, file_name)
        #Определяем название файла с пользователем
        file_name, _ = QFileDialog.getSaveFileName(self.window, "Сохранить файл с именем ...", str(full_path),  ExportModel.FILE_programm[self.where],)
        self.file_name = file_name
        if self.file_name:
            return True
        print(self.file_name)

    #Метод, который экспортирует данные в файл зажанного типа
    def export(self):
        try:
            #выбираем подходящую функцию и запускаем ее
            function_for_export = ExportModel.FILE_command[self.where]
            function_for_export(self.export_sets, self.file_name)
            Inf_str = f'Выбранные данные сохранены в файле "{self.file_name}". Открыть его ?'
            dialog = QMessageBox.question(self.window, "Уведомление", Inf_str)
            if dialog == QMessageBox.Yes:
                os.startfile(self.file_name)
        except Exception as other:
            Error_str = f'Не удалось экспортировать данные в файл. Ошибка {other}'
            print(Error_str)
            return False
