#Вспомогательные методы
from datetime import datetime
from PyQt5.QtCore import  QDate, Qt, QEvent
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QHeaderView, QWidget, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QCheckBox
from dataclasses import dataclass
from PyQt5.QtWidgets import QCompleter, QDialog, QDialogButtonBox, QGridLayout, QWidget, QCheckBox, QVBoxLayout, QLabel, QLineEdit, QComboBox



# Созжаем на основе класса QWidget подкласс Color (закрашенное моноцветом окно)
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
    #Конец метода init класса Color
#Конец описания класса Color

class CustomDialog(QDialog):
    def __init__(self, tab_list, check_dict):
        super().__init__()
        self.tab_list = tab_list
        self.setWindowTitle("Эксорт ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        check_layout = QGridLayout()
        check_box_box = QWidget()
        for idx, tab in enumerate(tab_list):
            check_box = QCheckBox(f'{tab.tab_name}')
            check_box.setCheckState(Qt.Unchecked)
            check_dict[tab.tab_name] = check_box
            check_layout.addWidget(check_box, (idx % 3), 5*(idx//3), 1, 5, Qt.Alignment(0))
        check_box_box.setLayout(check_layout)
        self.layout = QVBoxLayout()
        message = QLabel("Выберите таблицы, которые следует экспортировать")
        self.layout.addWidget(message)
        self.layout.addWidget(check_box_box)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class NewItemDialog(QDialog):
    def __init__(self, column_name):
        super().__init__()
        self.setWindowTitle("Конфликт уникальных значений ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.edit = QLineEdit()
        self.layout = QVBoxLayout()
        message = QLabel(f'Введите значение для столбца "{column_name}", которым следует заменить конфликтное значение.')
        self.layout.addWidget(message)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class DialogAskCorr(QDialog):
    #pair_values = [(row_in, in_value, bd_value), ...]
    def __init__(self, pair_values, all_bd_values):
        super().__init__()
        self.setWindowTitle("Подбор подходящих связанных значений ...")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        check_layout = QGridLayout()
        check_box_box = QWidget()
        #Готовим словари для записи объектов взаимодействия с пользователем
        out_dict = {}
        lable_in = QLabel("Импортированное значение")
        lable_bd = QLabel("Автоматически подобранный вариант из БД")
        lable_out = QLabel("Выбранный вариант")
        check_layout.addWidget(lable_in,0, 0, 1, 1, Qt.Alignment(0))
        check_layout.addWidget(lable_bd, 0, 1, 1, 1, Qt.Alignment(0))
        check_layout.addWidget(lable_out, 0, 2, 1, 1, Qt.Alignment(0))
        for idx, soft in enumerate(pair_values):
            val_in = QLineEdit(soft[1])
            val_in.setDisabled(True)
            val_out = QLineEdit(soft[2])
            val_out.setDisabled(True)
            val_ask = QComboBox()
            val_ask.addItems(all_bd_values)
            val_ask.setCurrentIndex(val_ask.findText(soft[2]))
            #Настраиваем комплиттер
            val_ask.setEditable(True)
            val_ask.completer().setCompletionMode(QCompleter.PopupCompletion)
            val_ask.setInsertPolicy(QComboBox.NoInsert)



            out_dict[idx] = val_ask
            check_layout.addWidget(val_in, idx + 1, 0, 1, 1, Qt.Alignment(0))
            check_layout.addWidget(val_out, idx + 1, 1, 1, 1, Qt.Alignment(0))
            check_layout.addWidget(val_ask, idx + 1, 2, 1, 1, Qt.Alignment(0))
        check_box_box.setLayout(check_layout)
        layout = QVBoxLayout()
        message_1 = QLabel("1. Подберите для всех импортированных элементов подходящие значения, изменив состояние выпадающего списка")
        layout.addWidget(message_1)
        layout.addWidget(check_box_box)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        #Присваиваем окну словари с объектами полей, чтобы обращаться к ним извне
        self.out_dict = out_dict
