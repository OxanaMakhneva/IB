from datetime import datetime
from PyQt5.QtCore import  QDate, Qt, QEvent, QIdentityProxyModel, QAbstractProxyModel, QSortFilterProxyModel
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView, QTableView

#Класс - делегат для того чтобы пробрасывать функцию выравнивая в объекты типа <QTableView>
class CustomAlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CustomAlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
#Конец оисания класса AlignDelegate

#Подкласс класса <QTableView>. На вход принимает все аргументы, предусмотренные
#родительским классом и словарь для столбцов, у которых необходимо при
#инициалмизации таблицы настроить ширину <width> (<индекс столбца>: ширина столбца)
class CustomTableView(QTableView):
    def __init__(self, window, width = dict(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        #self.verticalHeader().hide()
        # Коннектор - при изменении ширины столбца вызывается метод <section_resized>
        self.horizontalHeader().sectionResized.connect(self.section_resized)
        # Флаг - столбцы еще не изменялись динамически
        self.dynamically_resized = False
        # Словарь значений столбцов с настроенной статически шириной
        self.fixed_section_widths = width
        for column_index, width in self.fixed_section_widths.items():
            self.setColumnWidth(column_index, width)
        self.setWordWrap(False)
    #Декоратор
    #Чтобы после динамической настройки столбцов методом <dynamic_column_resize>
    #не запустился метод <section_resized>, который подлючен к событию изменения ширины,
    #перед запуском метода <dynamic_column_resize> декоратором отключаем метод
    #<section_resized> от коннектора, а после завершения метода <dynamic_column_resize>,
    #оключаем его обратно
    def disconnect_section_resized(func):
        def wrapper(self):
            self.horizontalHeader().sectionResized.disconnect(self.section_resized)
            func(self)
            self.horizontalHeader().sectionResized.connect(self.section_resized)
        return wrapper

    @disconnect_section_resized
    #Метод, который автоматически изменяет ширину всех столбцов, которые
    #НЕ записаны в словарь с фиксированными значениями ширины <self.fixed_section_widths>
    def dynamic_column_resize(self):
        #общая ширина, досупная для автоматического распределения
        flexible_width = self.width() - 10 - sum(self.fixed_section_widths.values())
        #общее кол-во столбцов и  количество настраиваемых столбцов
        column_count = self.model().columnCount()
        flexible_column_count = column_count - len(self.fixed_section_widths)
        #ширина одного настраиваемого столбца
        column_width = flexible_width // flexible_column_count if flexible_column_count else 1
        #ширина последнего настраиваемого столбца
        last_flexible_column_width = column_width + flexible_width % column_width if column_width else 1
        #итерируем по всем столбцам
        for column_index in range(column_count):
            if column_index not in self.fixed_section_widths:
                #определяем ширину всех настраиваемых столбцов (кроме последнего) равной <column_width>
                #для последнего берем ширину с хвостиком <last_flexible_column_width>
                width = column_width if flexible_column_count > 1 else last_flexible_column_width
                flexible_column_count = flexible_column_count - 1
            else:
                #определяем ширину фиксированных столбцов
                width = self.fixed_section_widths[column_index]
            #устанавливаем ширину
            self.setColumnWidth(column_index, width)
        #устанавливаем флаг - динамически настроено
        self.dynamically_resized = True

    #Метод, который запускает динамическую настройку только после ручного изменения
    #ширины столбца пользователем и только тогда, когда флаг динамической настройки установлен
    def section_resized(self, column_index, old_size, new_size):
        #если динамически еще не настроено - ничего не делаем
        if not self.dynamically_resized:
            return
        #если динамически уже настроено и пользователь поменял какой-то столбец
        #сохраняем в словаре для фиксированных широт пару индекс столбца - текущая ширина
        self.fixed_section_widths[column_index] = self.columnWidth(column_index)
        #запускаем динамическую настройку остальных широт
        self.dynamic_column_resize()

    def eventFilter(self, obj, event):
        #если произошло событие программного изменения ширины
        if event.type() == QEvent.Resize:
            #вызываем метод динамического изменения ширины
            self.dynamic_column_resize()
            return True
        #возвращаем результаты работы родительского метода eventFilter
        return super(QTableView, self).eventFilter(obj, event)


    #Метод, который добавляет заголовки в объект обработки данных класса <QSqlQueryModel>
    #или его подкласса <CustomSqlModel>, который
    #потом самостоятельно транслтрует их в модель отображения данных <QTableView>
    #На вход передается объект класса <QSqlQueryModel> или <CustomSqlModel> и список заголовков
    def add_headers(self, model, table_headers = None):
        if table_headers:
            for idx, head in enumerate(table_headers):
                model.setHeaderData(idx, Qt.Horizontal, head)
    #Конец метода add_headers

    #Метод, который настраивает внешний вид модели отображения данных <QTableView>
    #(ширину столбцов, размер шрифта, выравнивание текста в таблице)
    #На вход передается объект типа <QTableView>, словарь значений ширины и размер шрифта
    def set_table_style(self, table_widths = None, table_font = 10):
        #Настраиваем размер шрифта таблицы
        font = self.font()
        font.setPointSize(table_font)
        self.setFont(font)
        #Настраиваем выравнивание текста в таблице. Используем класс - делегат
        delegate_cust = CustomAlignDelegate(self)
        self.setItemDelegate(delegate_cust)
    #Конец метода set_table_style класса MainWindow

class CustomQSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, viewmodel):
        super().__init__(viewmodel)
        self.viewmodel = viewmodel

    def flags(self, index):
        flag = super().flags(index)
        if (index.column() != 0):
            return flag & ~ Qt.ItemIsEditable
        else:
            return flag &  Qt.ItemIsSelectable

# flag & ~ Qt.ItemIsEditable - устанавливаем значение флага в <0> независимо от предыдущего состояния
# flag & Qt.ItemIsSelectable - устанавливаем значение флага в <1> независимо от предыдущего состояния
# если использовать | будет учитываться пред.состояние
    def set_maplist(self, map_list):
        self.map_list = map_list

    def data(self, index, role):
        value = super().data(index, role)
        # Так как и sqlalchemy и QDate при записи в БД дату преобразует в строку формата "yyyy-MM-dd",
        # которая нас визуально не устраивает, при выдаче данныхна отображение, подменяем их на "dd.MM.yyyy"
        if isinstance(value, str) and role == Qt.DisplayRole:
            if index.column() < len(self.map_list):
                if self.map_list[index.column()].type == "date":
                    try:
                        value_d = QDate.fromString(value, "yyyy-MM-dd")
                        value = value_d.toString("dd.MM.yyyy")
                    except:
                        return value
        return value
