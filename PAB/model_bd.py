import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import CheckConstraint, UniqueConstraint, ForeignKeyConstraint, or_, and_, not_
from datetime import date, time
from PyQt5.QtCore import Qt, QDate
import datetime
#Для формирования списков ограниченных значений
import enum
from sqlalchemy import Enum
import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Устанавливаем соединение с postgres
connection = psycopg2.connect(user="postgres", password="z-123456")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Создаем курсор для выполнения операций с базой данных
cursor = connection.cursor()
# Создаем базу данных
cursor.execute('create database test12')
# Закрываем соединение
cursor.close()
connection.close()




#для работы с БД используем библиотеку sqlalchemy на уровне языка выражений ORM
#В объекте MetaData содержится всю информацию о базе данных и таблицах

meta=sa.MetaData()
#создаем пул подключения и подключаемся к файлу test2.db
#conn=sa.create_engine('psycopg2:///test11.db')

conn = sa.create_engine("postgresql+psycopg2://postgres:z-123456@localhost/test12")



#Создаем классы (для каждой таблицы свой) и связываем их атрибуты со столбцами
Base=declarative_base()

"""
Связывающая таблица assets_room для организации связи многие-многие между Assets и Rooms:
1 - id_asset - номер объекта (ключевое поле в таблице Assets)
2 - id_room - номер помещения (ключевое поле в таблице Rooms)
"""
asset_rooms = sa.Table('asset_rooms', Base.metadata,
    sa.Column('id_asset', sa.Integer, sa.ForeignKey('assets.id')),
    sa.Column('id_room', sa.Integer, sa.ForeignKey('rooms.id'))
)
"""
Связывающая таблица assets_SZI для организации связи многие-многие между Assets и SZIs:
1 - id_asset - номер объекта (ключевое поле в таблице Assets)
2 - id_SZI - номер СЗИ (ключевое поле в таблице SZIs)
"""
asset_szis = sa.Table('asset_szis', Base.metadata,
    sa.Column('id_asset', sa.Integer, sa.ForeignKey('assets.id')),
    sa.Column('id_szi', sa.Integer, sa.ForeignKey('szis.id'))
)
"""
Связывающая таблица assets_responsible для организации связи многие-многие между Assets и Responsibles:
1 - id_asset - номер объекта (ключевое поле в таблице Assets)
2 - id_responsible - номер ответственного (ключевое поле в таблице Responsibles)
"""
asset_responsibles = sa.Table('asset_responsibles', Base.metadata,
    sa.Column('id_asset', sa.Integer, sa.ForeignKey('assets.id')),
    sa.Column('id_responsible', sa.Integer, sa.ForeignKey('responsibles.id'))
)
"""
Связывающая таблица asset_ords для организации связи многие-многие между Assets и Responsibles:
1 - id_asset - номер объекта (ключевое поле в таблице Assets)
2 - id_ord - номер ответственного (ключевое поле в таблице Responsibles)
"""
asset_ords = sa.Table('asset_ords', Base.metadata,
    sa.Column('id_asset', sa.Integer, sa.ForeignKey('assets.id')),
    sa.Column('id_ord', sa.Integer, sa.ForeignKey('ords.id'))
)

"""
Связывающая таблица asset_attdocs для организации связи многие-многие между Assets и Responsibles:
1 - id_asset - номер объекта (ключевое поле в таблице Assets)
2 - id_attdoc - номер ответственного (ключевое поле в таблице Responsibles)
"""
asset_attdocs = sa.Table('asset_attdocs', Base.metadata,
    sa.Column('id_asset', sa.Integer, sa.ForeignKey('assets.id')),
    sa.Column('id_attdoc', sa.Integer, sa.ForeignKey('attdocs.id'))
)

"""
Связывающая таблица soft_otdels для организации связи многие-многие между экземплярами по и отделами, которым разрешено ими пользоваться:
1 - id_soft - номер объекта (ключевое поле в таблице Assets)
2 - id_otdel - номер отдела, которому разрешено им ользоваться
"""
soft_otdels = sa.Table('soft_otdels', Base.metadata,
    sa.Column('id_soft', sa.Integer, sa.ForeignKey('bd_softs.id')),
    sa.Column('id_otdel', sa.Integer, sa.ForeignKey('otdels.id'))
)
"""
Дополнительный класс AType со столбцами:
1 - id -порядковый номер типа объекта (ключевое поле)
2 - type - название типа
3 - kom - комментарий
"""
class AType(Base):
    __tablename__='atypes'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return "<AType({},{})>".format(self.id, self.type)

"""
Дополнительный класс RPType со столбцами:
1 - id -порядковый номер типа помещения (ключевое поле)
2 - type - название типа помещения
"""
class RPType(Base):
    __tablename__='rptypes'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<RPType({},{})>".format(self.id, self.type)

"""
Дополнительный класс DType со столбцами:
1 - id -порядковый номер типа документа (ключевое поле)
2 - type - название типа
"""
class DType(Base):
    __tablename__='dtypes'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<DType({},{},{})>".format(self.id, self.type)

"""
Дополнительный класс DDType со столбцами:
1 - id -порядковый номер типа документа (ключевое поле)
2 - type - название типа по времени
"""
class DDType(Base):
    __tablename__='ddtypes'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return "<DDType({},{},{})>".format(self.id, self.type)
"""
Дополнительный класс RType со столбцами:
1 - id - порядковый номер типа ответсвенного (ключевое поле)
2 - type - название типа
3 - kom - комментарий
"""
class RType(Base):
    __tablename__='rtypes'
    id = sa.Column('id', sa.Integer, primary_key=True)
    type = sa.Column('type', sa.String(100), unique = True)
    kom = sa.Column('kom', sa.String(100))

    def __init__(self, id, type, kom):
        self.id = id
        self.type = type
        self.kom = kom

    def __repr__(self):
        return "<RType({},{},{})>".format(self.id, self.type, self.kom)

"""
Дополнительный класс SType со столбцами:
1 - id -порядковый номер типа СЗИ (ключевое поле)
2 - type - название типа
"""
class SType(Base):
    __tablename__='stypes'
    id = sa.Column('id', sa.Integer, primary_key=True)
    type = sa.Column('type', sa.String(100), unique = True)         # Наша классификация

    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return "<SType({},{})>".format(self.id, self.type)

"""
Дополнительный класс SElement со столбцами:
1 - id -порядковый номер модели СЗИ (ключевое поле)
2 - type - название модели
"""
class SElement(Base):
    __tablename__='selements'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(50), unique = True) #То, что в кавычках в столбце реестра ...(шифр)

    def __init__(self, id, name):
        self.id = id
        self.name = name          #ип составных частей и Если есть, отдельное название составных частей (srcret net touch memory card)
    def __repr__(self):
        return "<SElement({},{})>".format(self.id, self.name)


"""
Дополнительный класс OType со столбцами:
1 - id -порядковый номер типа ОРД (ключевое поле)
2 - type - название типа
3 - kom - комментарий
"""
class OType(Base):
    __tablename__='otypes'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)
    kom = sa.Column('kom', sa.String(100))

    def __init__(self, id, type, kom):
        self.id = id
        self.type = type
        self.kom = kom

    def __repr__(self):
        return "<OType({},{},{})>".format(self.id, self.type, self.kom)
"""
Дополнительный класс TType со столбцами:
1 - id -порядковый номер типа ТС (ключевое поле)
2 - type - название типа

"""

class TType(Base):
    __tablename__='ttypes'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)

    def __init__(self, id, type, kom):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<OType({},{})>".format(self.id, self.type)
"""
Дополнительный класс Akat со столбцами:
1 - id -порядковый номер категории (ключевое поле)
2 - type - название категории
"""
class AKat(Base):
    __tablename__='akats'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<AKat({},{})>".format(self.id, self.type)

"""
Дополнительный класс Aklass со столбцами:
1 - id -порядковый номер класса (ключевое поле)
2 - type - название категории
"""
class AKlass(Base):
    __tablename__='aklasses'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<AKlass({},{})>".format(self.id, self.type)

"""
Дополнительный класс AStatus со столбцами:
1 - id -порядковый номер статуса (ключевое поле)
2 - type - тип статуса
"""
class AStatus(Base):
    __tablename__='astatuses'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<AStatuses({},{})>".format(self.id, self.type)

"""
Дополнительный класс Territores со столбцами:
1 - id -порядковый номер территории (ключевое поле)
2 - numb - номер территории
"""
class Territore(Base):
    __tablename__='territores'
    id = sa.Column('id', sa.Integer, primary_key = True)
    numb = sa.Column('numb', sa.String(10), unique = True)
    def __init__(self, id, numb):
        self.id = id
        self.numb = numb
    def __repr__(self):
        return "<Territores({},{})>".format(self.id, self.name)

"""
Дополнительный класс Secrets со столбцами:
1 - id -порядковый номер территории (ключевое поле)
2 - type - тип конфиденциальности
"""
class Secret(Base):
    __tablename__='secrets'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return "<Secrets({},{})>".format(self.id, self.type)
"""
Дополнительный класс ATodo со столбцами:
1 - id -порядковый номер статуса (ключевое поле)
2 - type - список дел
"""
class ATodo(Base):
    __tablename__='atodos'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "<ATodos({},{})>".format(self.id, self.type)

"""
Основная таблица Assets(собственность) со столбцами:
1 - id - номер объекта (ключевое поле)
2 - name - название объекта
3 - type_id - внешний ключ к таблице ATypes, указывает на id типа объекта
4 - kat_id - внешний ключ к таблице AKats, указывает на id категории объекта
5 - klass_id - внешний ключ к таблице Aklasses, указывает на id класса объекта
6 - attestatum_id - внешний ключ к таблице Attestatums, указывает на id аттестата
7 - status_id -  внешний ключ к таблице Statuses, указывает на id статуса (выведен, действует, аттестуется)
8 - todo_id -  внешний ключ к таблице Todos, указывает на id списка работ
"""

class Asset(Base):
    __tablename__='assets'
    id = sa.Column('id', sa.Integer, primary_key = True)
    year = sa.Column('year', sa.Integer)
    type_id = sa.Column('type_id', sa.Integer)
    name = sa.Column('name', sa.String(100))
    kat_id = sa.Column('kat_id', sa.Integer)
    klass_id = sa.Column('klass_id', sa.Integer)
    status_id = sa.Column('status_id', sa.Integer)
    todo_id = sa.Column('todo_id', sa.Integer)

    #Создаем внешний ключ, используется для отношения:
    #один из Assets ко многим из Attestatums,
    #один из Assets ко многим из Attdocs
    #!Проверить, реально ли один ко многим
    __table_args__ = (
                UniqueConstraint('year', 'name'),
                ForeignKeyConstraint(['type_id'], ['atypes.id']),
                ForeignKeyConstraint(['kat_id'], ['akats.id']),
                ForeignKeyConstraint(['klass_id'], ['aklasses.id']),
                ForeignKeyConstraint(['status_id'], ['astatuses.id']),
                ForeignKeyConstraint(['todo_id'], ['atodos.id']),
                    )

    # Объявляется отношение многие ко многим к Rooms,SZIs,Responsibles через промежуточные таблицы asset_rooms,asset_SZIs,asset_Responsibles
    room_s = relationship('Room', secondary=asset_rooms, backref = backref ('asset_s'))
    szi_s = relationship('SZI', secondary=asset_szis, backref='szi_s')
    responsible_s = relationship('Responsible', secondary=asset_responsibles, backref='responsible_s')


    def __init__(self, id, year, type_id, name, kat_id, klass_id, status_id, todo_id):
        self.id = id
        self.year = year
        self.type_id = type_id
        self.name = name
        self.kat_id = kat_id
        self.klass_id = klass_id
        self.status_id = status_id
        self.todo_id = todo_id

    def __repr__(self):
        return "<Asset({},{},{},{},{},{},{})>".format(self.id, self.type_id, self.name, att_id, self.kat_id, self.klass_id, self.status_id, self.todo_id)

"""
Дополнительная Attestatum(аттестаты) со столбцами:
1 - id - номер атестата (ключевое поле)
2 - name - название аттестата
3 - numb - регистрационный номер атестата
5 - begin - дата начала действия атестата
6 - end - дата окончания действия атестата
7 - inv - номер места хранения
"""

class Attestatum(Base):
    __tablename__='attestatums'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(100))
    numb = sa.Column('numb', sa.String(100), unique = True)
    begin = sa.Column('begin', sa.Date)
    end = sa.Column('end',  sa.Date)
    inv = sa.Column('inv', sa.String)
    secret_id = sa.Column('secret_id', sa.Integer)
    asset_id = sa.Column('asset_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                    UniqueConstraint('begin', 'numb'),
                    ForeignKeyConstraint(['asset_id'], ['assets.id'], use_alter=False),
                    ForeignKeyConstraint(['secret_id'], ['secrets.id']),
                        )
    def __init__(self, id, name, numb, begin, end, inv, secret_id, asset_id):
        self.id = id
        self.name = name
        self.numb = numb
        self.begin = begin
        self.end = end
        self.inv = inv
        self.secret_id = secret_id
        self.asset_id = asset_id
    def __repr__(self):
        return "<Attestatum({},{},{},{},{},{},{},{})>".format(self.id, self.name, self.numb, self.begin, self.end, self.inv, self.secret_id, self.asset_id)
"""
Дополнительная таблица AttestatumRP(аттестаты помещения) со столбцами:
1 - id -порядковый номер аттестата (ключевое поле)
3 - name - название аттестата
4 - numb - регистрационный номер атестата
5 - begin - дата начала действия атестата
6 - end - дата окончания действия атестата
7 - inv - номер места хранения
"""
class AttestatumRP(Base):
    __tablename__='attestatumrps'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(100))
    full_name = sa.Column('full_name', sa.String(200))
    numb = sa.Column('numb', sa.String(100))
    begin = sa.Column('begin', sa.Date)
    end = sa.Column('end', sa.Date)
    inv = sa.Column('inv', sa.String(100))
    secret_id = sa.Column('secret_id', sa.Integer)
    type_id = sa.Column('type_id', sa.Integer)
    spets = sa.Column('spets', sa.String(100))
    vp = sa.Column('vp', sa.String(100))
    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                    UniqueConstraint('numb', 'begin'),
                    ForeignKeyConstraint(['type_id'], ['rptypes.id']),
                    ForeignKeyConstraint(['secret_id'], ['secrets.id']),
                        )
    def __init__(self, id, name, full_name, numb, begin, end, inv, secret_id, type_id, spets, vp):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.numb = numb
        self.begin = begin
        self.end = end
        self.inv = inv
        self.secret_id = secret_id
        self.type_id = type_id
        self.spets = spets
        self.vp = vp
    def __repr__(self):
        return "<AttestatumRP({},{},{},{},{},{},{},{},{},{},{})>".format(self.id, self.name, self.full_name, self.numb, self.begin, self.end, self.inv, self.secret_id, self.type_id, self.spets, self.vp)

"""
Дополнительная таблица Room(помещения) со столбцами:
1 - id - номер помещения (ключевое поле)
2 - numb - номер помещения
3 - terr - территория
4 - floor - этаж
5 - osi - оси
6 - attRP_id - номер аттестата помещения (ключевое поле в таблице AttestatumRP)
Связана с таблицей Assets многие-многие через таблицу assets_rooms
"""

class Room(Base):
    __tablename__='rooms'
    id = sa.Column('id', sa.Integer, primary_key = True)
    numb = sa.Column('numb', sa.String(100))
    terr_id = sa.Column('terr_id', sa.Integer)
    floor = sa.Column('floor', sa.Integer)
    osi = sa.Column('osi', sa.String(100))
    attrp_id =  sa.Column('attrp_id', sa.Integer)

    #Создаем внешний ключ, используется для отношения один из AttestatumRP ко многим из Rooms
    __table_args__ = (
            ForeignKeyConstraint(['attrp_id'], ['attestatumrps.id']),
            ForeignKeyConstraint(['terr_id'], ['territores.id']),
                        )

    def __init__(self, id, numb, terr_id, floor, osi, attrp_id):
        self.id = id
        self.numb = numb
        self.terr = terr_id
        self.floor = floor
        self.osi = osi
        self.attrp_id = attrp_id

    def __repr__(self):
        return "<Room({},{},{},{},{},{})>".format(self.id, self.numb, self.terr_id, self.floor, self.osi, self.attrp_id)

"""
Дополнительная таблица Attdoc(документы по аттестации) со столбцами:
1 - id -порядковый номер документа (ключевое поле)
2 - name - название документа
3 - numb - регистрационный номер документа
4 - begin - дата документа
5 - inv - номер места хранения
6 - type_id - внешний ключ к таблице DTypes, указывает на id типа документа
7 - typeD_id - внешний ключ к таблице DDTypes, указывает на id типа документа по времени
"""
class Attdoc(Base):
    __tablename__ = 'attdocs'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type_id = sa.Column('type_id', sa.Integer)
    typed_id = sa.Column('typed_id', sa.Integer)
    name = sa.Column('name', sa.String(100))
    full_name = sa.Column('full_name', sa.String(100))
    numb = sa.Column('numb', sa.String(100), unique = True)
    begin = sa.Column('begin', sa.Date)
    inv = sa.Column('inv', sa.String(100))
    secret_id = sa.Column('secret_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                UniqueConstraint('numb', 'begin'),
                ForeignKeyConstraint(['type_id'], ['dtypes.id']),
                ForeignKeyConstraint(['typed_id'], ['ddtypes.id']),
                ForeignKeyConstraint(['secret_id'], ['secrets.id']),
    )
    def __init__(self, id, type_id, typed_id, name, full_name, numb, begin, end, inv, secret_id):
        self.id = id
        self.type_id = type_id
        self.typed_id = typed_id
        self.name = name
        self.full_name = full_name
        self.numb = numb
        self.begin = begin
        self.inv = inv
        self.secret_id = secret_id
    def __repr__(self):
        return "<Attdoc({},{},{},{},{},{},{},{},{},{})>".format(self.id, self.type_id, self.typed_id, self.name, self.full_name, self.numb, self.begin, self.end, self.inv, self.secret_id)


"""
Дополнительная таблица Tehnica (технические средства) со столбцами:
1 - id -порядковый номер ТС (ключевое поле)
2 - name - название ТС
3 - model - модель ТС
3 - numb - серийный номер
4 - sz - спец знак
5 - attdoc_id - внешний ключ к таблице Attdocs, указывает на id названия документа
6 - arm_id - внешний ключ к таблице ARMs, указывает на id АРМ
"""
class Tehno(Base):
    __tablename__ = 'tehnos'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type_id = sa.Column('type_id', sa.Integer)
    name = sa.Column('name', sa.String(100))
    model = sa.Column('model', sa.String(100))
    numb = sa.Column('numb', sa.String(100), unique = True)
    sz = sa.Column('sz', sa.String(100), unique = True)
    attdoc_id = sa.Column('attdoc_id', sa.Integer)
    arm_id = sa.Column('arm_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                ForeignKeyConstraint(['type_id'], ['ttypes.id']),
                ForeignKeyConstraint(['attdoc_id'], ['attdocs.id']),
                ForeignKeyConstraint(['arm_id'], ['arms.id']),
                )
    def __init__(self, id, type_id, name, model, numb, sz, attdoc_id, arm_id):
        self.id = id
        self.type_id = type_id
        self.name = name
        self.model = model
        self.numb = numb
        self.sz = sz
        self.attdoc_id = attdoc_id
        self.arm_id = arm_id
    def __repr__(self):
        return "<Tehnos({},{},{},{},{},{},{},{})>".format(self.id, self.type_id, self.name, self.model, self.numb, self.sz, self.attdoc_id, self.arm_id)

#Класс, определяющий ограничения для значений из списка тип для таблицы Users
class ARMTypeEnum(enum.Enum):
    one = "Интернет"
    two = "Всп"
    three = "Локальный"
    four = "Не выбрано"

"""
Дополнительная таблица ARM (технические средства) со столбцами:
1 - id -порядковый номер ARM (ключевое поле)
2 - type тип (сетевой, локальный)
3 - name - сетевое имя арм
4 - otdel_id - внешний ключ к таблице Otdels, указывает на id отдела
5 - asset_id - внешний ключ к таблице Assets, указывает на id объекта
"""
class ARM(Base):
    __tablename__ = 'arms'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), Enum(ARMTypeEnum))
    name = sa.Column('name', sa.String(100))
    otdel_id = sa.Column('otdel_id', sa.Integer)
    asset_id = sa.Column('asset_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                ForeignKeyConstraint(['otdel_id'], ['otdels.id']),
                ForeignKeyConstraint(['asset_id'], ['assets.id']),
                )
    def __init__(self, id, type, name, otdel_id, asset_id):
        self.id = id
        self.type = type
        self.name = name
        self.otdel_id = otdel_id
        self.asset_id = asset_id
    def __repr__(self):
        return "<ARMs({},{},{},{},{},{},{},{})>".format(self.id, self.type, self.name, self.otdel_id, self.asset_id)

"""
Дополнительная таблица ORDs(ответственные) со столбцами:
1 - id -порядковый номер ОРД (ключевое поле)
5 - name - наименование ОРД
6 - numb - номер ОРД
7 - begin - дата начала ОРД
8 - end - дата окончания ОРД
4 - type_id - внешний ключ к таблице OTypes, указывает на id типа ОРД
"""
class ORD(Base):
    __tablename__='ords'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type_id = sa.Column('type_id', sa.Integer)
    typed_id = sa.Column('typed_id', sa.Integer)
    name = sa.Column('name', sa.String(100))
    full_name = sa.Column('full_name', sa.String(100))
    numb = sa.Column('numb', sa.String(100))
    begin = sa.Column('begin', sa.Date)
    end = sa.Column('end', sa.Date)
    inv = sa.Column('inv', sa.String(100))
    secret_id = sa.Column('secret_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из Assets ко многим из ORDs
    __table_args__ = (
                UniqueConstraint('numb', 'begin'),
                ForeignKeyConstraint(['type_id'], ['otypes.id']),
                ForeignKeyConstraint(['typed_id'], ['ddtypes.id']),
                ForeignKeyConstraint(['secret_id'], ['secrets.id']),
    )

    def __init__(self, id, type_id, typed_id, name, full_name, numb, begin, end, inv, secret_id):
        self.id = id
        self.type_id = type_id
        self.typeD_id = typed_id
        self.name = name
        self.full_name = full_name
        self.numb = numb
        self.begin = begin
        self.end = end
        self.inv = inv
        self.secret_id = secret_id
    def __repr__(self):
        return "<ORD({},{},{},{},{},{},{},{},{})>".format(self.id, self.type_id, self.typed_id, self.name, self.full_name, self.numb, self.begin, self.end, self.inv)

"""
Дополнительная таблица Otdels(отделы) со столбцами:
1 - id -порядковый номер отдела (ключевое поле)
2 - servise_id - внешний ключ к таблице servises, указывает на id службы
4 - numb - номер отдела
5 - name - имя отдела
6 - lboss_id - внешний ключ к таблице Peoples, указывает на id начальника отдела
"""
class Otdel(Base):
    __tablename__='otdels'
    id = sa.Column('id', sa.Integer, primary_key = True)
    servise_id = sa.Column('servise_id', sa.Integer)
    numb = sa.Column('numb', sa.String(100), unique = True)
    name = sa.Column('name', sa.String(100))
    lboss_id = sa.Column('lboss_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    __table_args__ = (
            ForeignKeyConstraint(['servise_id'], ['servises.id']),
            ForeignKeyConstraint(['lboss_id'], ['peoples.id']))

    def __init__(self, id, servise_id, numb, name, lboss_id):
        self.id = id
        self.servise_id = servise_id
        self.numb = numb
        self.name = name
        self.lboss_id = lboss_id
    def __repr__(self):
        return "<Otdel({},{},{},{},{})>".format(self.id, self.servise_id, self.numb, self.name, self.lboss_id)

"""
Дополнительная таблица Otdels(отделы) со столбцами:
1 - id -порядковый номер отдела (ключевое поле)
2 - servise_id - внешний ключ к таблице servises, указывает на id службы
4 - numb - номер отдела
5 - name - имя отдела
6 - lboss_id - внешний ключ к таблице Peoples, указывает на id начальника отдела
"""
class Servise(Base):
    __tablename__='servises'
    id = sa.Column('id', sa.Integer, primary_key = True)
    numb = sa.Column('numb', sa.String(100), unique = True)
    name = sa.Column('name', sa.String(100))
    boss_id = sa.Column('boss_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    __table_args__ = (
                     ForeignKeyConstraint(['boss_id'], ['peoples.id']),
                     )
    def __init__(self, id, numb, name, boss_id):
        self.id = id
        self.numb = numb
        self.name = name
        self.boss_id = boss_id
    def __repr__(self):
        return "<Servise({},{},{},{})>".format(self.id, self.numb, self.name, self.boss_id)

"""
Дополнительная таблица Truds(отделы) со столбцами:
1 - id -порядковый номер категории (ключевое поле)
2 - type - тип категории
"""
class Trud(Base):
    __tablename__='truds'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(50), unique = True)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return "<Trud({},{})>".format(self.id, self.type)

"""
Дополнительная таблица Truds(отделы) со столбцами:
1 - id -порядковый номер категории (ключевое поле)
2 - name - должность
"""
class Position(Base):
    __tablename__='positions'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(100), unique = True)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __repr__(self):
        return "<Position({},{})>".format(self.id, self.name)

"""
Дополнительная таблица Forms(формы) со столбцами:
1 - id -порядковый номер категории (ключевое поле)
2 - type - тип формы
"""
class Form(Base):
    __tablename__='forms'
    id = sa.Column('id', sa.Integer, primary_key = True)
    type = sa.Column('type', sa.String(100), unique = True)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return "<Forms({},{})>".format(self.id, self.type)
"""
Дополнительная таблица People(люди) со столбцами:
1 - id -порядковый номер человека (ключевое поле)
2 - card - табельный номер
3 - sur - фамилия
4 - name - имя
5 - patr - отчество
6 - otd_id - внешний ключ к таблице Otdels, указывает на id отдела
7 - trud_id - внешний ключ к таблице Truds, указывает на id трудового состояния
"""
class People(Base):
    __tablename__='peoples'
    id = sa.Column('id', sa.Integer, primary_key = True)
    card = sa.Column('card', sa.String(100), unique = True)
    pos_id = sa.Column('pos_id', sa.Integer)
    fio = sa.Column('fio', sa.String(60))
    tel = sa.Column('tel', sa.String(100))
    otd_id = sa.Column('otd_id', sa.Integer)
    trud_id = sa.Column('trud_id', sa.Integer)
    form_id = sa.Column('form_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    __table_args__ = (
            ForeignKeyConstraint(['pos_id'], ['positions.id']),
            ForeignKeyConstraint(['otd_id'], ['otdels.id']),
            ForeignKeyConstraint(['trud_id'], ['truds.id']),
            ForeignKeyConstraint(['form_id'], ['forms.id']),
            )
    def __init__(self, id, card, pos_id, fio, tel, otd_id, trud_id, form_id):
        self.id = id
        self.card = card
        self.pos_id = pos_id
        self.fio = fio
        self.tel = tel
        self.otd_id = otd_id
        self.trud_id = trud_id
        self.form_id = form_id
    def __repr__(self):
        return "<People({},{},{},{},{},{},{},{})>".format(self.id, self.card, self.pos_id, self.fio, self.tel, self.otd_id, self.trud_id, self.form_id)
"""
Дополнительная таблица Responsible(ответственные) со столбцами:
1 - id -порядковый номер ответственного (ключевое поле)
2 - name - наименование ответственного
3 - fio - ФИО ответственного
4 - tel - телефон ответственного
5 - otd - отдел ответственного
7 - ord_id - внешний ключ к таблице ORDs, указывает на id ОРД
8 - type_id - внешний ключ к таблице RTypes, указывает на id типа ответственного
"""
class Responsible(Base):
    __tablename__='responsibles'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(100), unique = True)
    type_id = sa.Column('type_id', sa.Integer)
    people_id = sa.Column('people_id', sa.Integer)
    ord_id = sa.Column('ord_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    __table_args__ = (
            ForeignKeyConstraint(['ord_id'], ['ords.id']),
            ForeignKeyConstraint(['type_id'], ['rtypes.id']),
            ForeignKeyConstraint(['people_id'], ['peoples.id']),)
    def __init__(self, id, name,  type_id, people_id, ord_id):
        self.id = id
        self.name = name
        self.type_id = type_id
        self.people_id = people_id
        self.ord_id = ord_id
    def __repr__(self):
        return "<Responsible({},{},{},{},{},{})>".format(self.id, self.name, self.type_id, self.people_id, self.ord_id)

#Класс, определяющий ограничения для значений из списка тип для таблицы Users
class UserTypeEnum(enum.Enum):
    one = "локальная"
    two = "сетевая"
    three = "нулевой клиент"
    four = "Не выбрано"

"""
Дополнительная таблица Responsible(ответственные) со столбцами:
1 - id -порядковый номер ответственного (ключевое поле)
2 - name - наименование учетной записи
3 - type - тип учетной записи (локальная, сетевая)
4 - people_id - внешний ключ к таблице Peoples, указывает на id Человека
7 - ord_id - внешний ключ к таблице ORDs, указывает на id ОРД
8 - asset_id - внешний ключ к таблице Assets, указывает на id объекта
"""
class User(Base):
    __tablename__='users'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(100), unique = True)
    type = sa.Column('type', sa.String(100), Enum(UserTypeEnum)) #Enum(UserTypeEnum)
    people_id = sa.Column('people_id', sa.Integer)
    ord_id = sa.Column('ord_id', sa.Integer)
    arm_id = sa.Column('arm_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из ORDs ко многим из Responsibles
    __table_args__ = (
            ForeignKeyConstraint(['arm_id'], ['arms.id']),
            ForeignKeyConstraint(['ord_id'], ['ords.id']),
            ForeignKeyConstraint(['people_id'], ['peoples.id']),)
    def __init__(self, id, name,  type, people_id, ord_id, asset_id):
        self.id = id
        self.name = name
        self.type = type
        self.people_id = people_id
        self.ord_id = ord_id
        self.arm_id = asset_id
    def __repr__(self):
        return "<Responsible({},{},{},{},{},{})>".format(self.id, self.name, self.type, self.people_id, self.ord_id, self.asset_id)

"""
Дополнительная таблица Sert(документы по аттестации) со столбцами:
1 - id -порядковый номер сертификата (ключевое поле)
2 - name - название сертификата
3 - numb - регистрационный номер сертификата
4 - begin - дата начала сертификата
5 - end - дата окончания сертификата
6 - element_id - внешний ключ к таблице SElements, указывает на id модели СЗИ
7 - type_id - внешний ключ к таблице STypes, указывает на id типа СЗИ
"""
class Sert(Base):
    __tablename__='serts'
    id = sa.Column('id', sa.Integer, primary_key = True)
    numb = sa.Column('numb', sa.String(100), unique = True)         #№ сертификата
    begin = sa.Column('begin', sa.Date)                               #Дата внесения в реестр
    end = sa.Column('end', sa.Date)                                   #Срок действия сертификата
    type_id = sa.Column('type_id', sa.Integer)
    name = sa.Column('name', sa.String(100))         #Наименование средства(шифр)
    req_doc = sa.Column('req_doc', sa.String(100))   #Наименование документов, требованиям которых соответствует средство
    scheme = sa.Column('scheme', sa.String(100))     #Cхема сертификации
    end_tp = sa.Column('end_tp', sa.Date)                             #Информация об окончании срока технической поддержки, полученная от заявителя
    #Создаем внешний ключ, используется для отношения один из Serts ко многим из STypes
    __table_args__ = (
            ForeignKeyConstraint(['type_id'], ['stypes.id']),
            )
    def __init__(self, id, numb, begin, end, type_id, name, req_doc, scheme, end_tp):
        self.id = id
        self.numb = numb
        self.begin = begin
        self.end = end
        self.type_id = type_id
        self.name = name
        self.req_doc = req_doc
        self.scheme = scheme
        self.end_tp = end_tp
    def __repr__(self):
        return "<Sert({},{},{},{},{}, {}>".format(self.id, self.numb, self.begin, self.end, self.type_id, self.name, self.req_doc, self.scheme, self.end_tp)

"""
Дополнительная таблица SZI(СЗИ) со столбцами:
1 - id -порядковый номер СЗИ (ключевое поле)
2 - name - модель СЗИ
3 - numb - номер СЗИ
4 - SZZ - СЗЗ СЗИ
5 - sert_id - внешний ключ к таблице Serts, указывает на id сертификата
6 - type_id - внешний ключ к таблице STypes, указывает на id типа СЗИ
Связана многие ко многим с таблицей Assets через таблицу asset_SZIs
"""

class SZI(Base):
    __tablename__='szis'
    id = sa.Column('id', sa.Integer, primary_key = True)
    element_id = sa.Column('element_id', sa.Integer)    #Название составных частей (генератор, датчик, ПО, плата и т.д.)
    numb = sa.Column('numb', sa.String(100), unique = True)
    szz = sa.Column('szz', sa.String(100), unique = True)
    sert_id = sa.Column('sert_id', sa.Integer)
    #Создаем внешний ключ, используется для отношения один из Serts ко многим из SZIs
    __table_args__ = (
            ForeignKeyConstraint(['sert_id'], ['serts.id']),
            ForeignKeyConstraint(['element_id'], ['selements.id']),
    )
    def __init__(self, id, element_id, numb, szz, sert_id):
        self.id = id
        self.element_id = element_id
        self.numb = numb
        self.szz = szz
        self.sert_id = sert_id
    def __repr__(self):
        return "<SZI({},{},{},{},{})>".format(self.id, self.element_id, self.numb, self.szz, self.sert_id)

#Класс, определяющий ограничения для значений из списка тип для таблицы Users
class LegalityTypeEnum(enum.Enum):
    one = "Разрешено"
    two = "Запрещено"
    three = "Ситуационно"
    four = "Не выбрано"

"""
Дополнительная таблица BD_Soft (ПО) со столбцами:
1 - id -порядковый номер ПО (ключевое поле)
2 - name - название ПО
3 - type - тип ПО
4 - catigory_id - категория ПО
5 - legality - разрешенность ПО
6 - developer - производитель
7 - license - лицензия
8 - site - сайт ПО
9 - wiki_page - старница ВИКИ
"""
class BD_Soft(Base):
    __tablename__ = 'bd_softs'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(1000))
    type = sa.Column('type', sa.String(200))
    catigory_id = sa.Column('catigory_id', sa.Integer)
    legality = sa.Column('legality', sa.String(100), Enum(LegalityTypeEnum))
    developer = sa.Column('developer', sa.String(1000))
    license = sa.Column('license', sa.Unicode(1000))
    site = sa.Column('site', sa.String(1000))
    wiki_page = sa.Column('wiki_page', sa.String(1000))

    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                ForeignKeyConstraint(['catigory_id'], ['softcats.id']),
                )

    # Объявляется отношение многие ко многим к otdels через промежуточные таблицы soft_otdels
    otdel_s = relationship('Otdel', secondary = soft_otdels, backref = backref ('soft_s'))




    def __init__(self, id, name, type, catigory_id, legality, developer, license, site, wiki_page):
        self.id = id
        self.name = name
        self.type = type
        self.catigory_id = catigory_id
        self.legality = legality
        self.developer = developer
        self.license = license
        self.site = site
        self.wiki_page = wiki_page

    def __repr__(self):
        return "<BD_Softs({},{},{},{},{},{},{},{})>".format(self.id, self.name, self.type, self.catigory_id, self.legality, self.license, self.site, self.wiki_page)

"""
Дополнительный класс SoftCats со столбцами:
1 - id -порядковый номер класса (ключевое поле)
2 - catigory - название категории
"""
class SoftCat(Base):
    __tablename__='softcats'
    id = sa.Column('id', sa.Integer, primary_key = True)
    catigory = sa.Column('catigory', sa.String(100), unique = True)

    def __init__(self, id, catigory):
        self.id = id
        self.catigory = catigory

    def __repr__(self):
        return "<SoftCats({},{})>".format(self.id, self.catigory)

"""
Дополнительная таблица IN_Soft (ПО) со столбцами:
1 - id -порядковый номер ПО (ключевое поле)
2 - name - название ПО
3 - soft_id - ссылка на ПО из БД
"""
class IN_Soft(Base):
    __tablename__ = 'in_softs'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(1000))
    version = sa.Column('version', sa.String(200))
    install = sa.Column('install', sa.Date)
    soft_id = sa.Column('soft_id', sa.Integer)
    arm_id = sa.Column('arm_id', sa.Integer)
    corr = sa.Column('corr', sa.Float)

    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                ForeignKeyConstraint(['soft_id'], ['bd_softs.id']),
                ForeignKeyConstraint(['arm_id'], ['arms.id']),
                )
    def __init__(self, id, name, version, install, soft_id, arm_id, corr):
        self.id = id
        self.name = name
        self.version = version
        self.install = install
        self.soft_id = soft_id
        self.arm_id = arm_id
        self.corr = corr

    def __repr__(self):
        return "<IN_Softs({},{},{},{},{})>".format(self.id, self.name, self.version, self.install, self.soft_id, self.pc_id)

"""
Дополнительная таблица PC_Soft (ПО) со столбцами:
1 - id -порядковый номер ПО (ключевое поле)
2 - name - название ПО
3 - version - версия
4 - время установки
3 - soft_id - ссылка на ПО из БД
4 - arm_id - ссылка на системный блок, на котором установлено
"""
class PC_Soft(Base):
    __tablename__ = 'pc_softs'
    id = sa.Column('id', sa.Integer, primary_key = True)
    name = sa.Column('name', sa.String(1000))
    version = sa.Column('version', sa.String(200))
    install = sa.Column('install', sa.Date)
    soft_id = sa.Column('soft_id', sa.Integer)
    arm_id = sa.Column('arm_id', sa.Integer)
    corr = sa.Column('corr', sa.Float)

    #Создаем внешний ключ, используется для отношения один из Assets ко многим из Attdocs
    __table_args__ = (
                ForeignKeyConstraint(['soft_id'], ['bd_softs.id']),
                ForeignKeyConstraint(['arm_id'], ['arms.id']),
                )

    def __init__(self, id, name, version, install, soft_id, arm_id, corr):
        self.id = id
        self.install = install
        self.name = name
        self.version = version
        self.soft_id = soft_id
        self.arm_id = arm_id
        self.corr = corr

    def __repr__(self):
        return "<PC_Softs({},{},{},{},{},{})>".format(self.id, self.name, self.version, self.install, self.soft_id, self.pc_id)


#Создаем базу данных и таблицу
Base.metadata.create_all(conn)

#Создвем инф. объекты чтобы заполнить таблицу Truds
trud = (
        Trud(0, "Не выбрано"),
        Trud(1, "работает"),
        Trud(2, "длительное отсутствие"),
        Trud(3, "уволен"),
        )
#Создвем инф. объекты чтобы заполнить таблицу Secrets
secret = (
        Secret(0, "Не выбрано"),
        Secret(1, "без пометки"),
        Secret(2, "ДСП"),
        Secret(3, "конфиденциально"),
        )
#Создвем инф. объекты чтобы заполнить таблицу Forms
forms = (
        Form(0, "Не выбрано"),
        Form(1, "без формы"),
        Form(2, "с формой"),
        )
#Создвем инф. объекты чтобы заполнить таблицу Territores
terrs = (
        Territore(0, "Не выбрано"),
        Territore(1, "I"),
        Territore(2, "II"),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу RPTypes
RPT =  (
        RPType(0, 'Не выбрано'),
        RPType(1, 'склад'),
        RPType(2, 'офис'),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу TTypes
TCtypes =  (
            TType(0, 'Не выбрано', ""),
            TType(1, 'монитор', ""),
            TType(2, 'системный блок', ""),
            TType(3, 'манипулятор-мышь', ""),
            TType(4, 'клавиатура', ""),
            TType(5, 'ИБП', ""),
            TType(6, 'сетевой фильтр(удлинитель)', ""),
            TType(7, 'ЖМД', ""),
            TType(8, 'съемный накоитель (флэш)', ""),
            )
#Создвем инф. объекты чтобы создать и заполнить таблицу ATypes
AT =  (
        AType(0, 'Не выбрано'),
        AType(1, 'КИИ'),
        AType(2, 'ИСПДн'),
        AType(3, 'ГИС'),
        AType(4, 'АС - АРМ'),
        AType(5, 'АС - ЛВС'),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу DTypes
DT =  (
        DType(0, 'Не выбрано'),
        DType(1, 'Акт категорирования'),
        DType(2, 'Перечень ПО'),
        DType(3, 'Матрица доступа'),
        DType(4, 'Акт классификации'),
        DType(5, 'Модель угроз безопасности'),
        DType(6, 'Акт осмотра'),
        DType(7, 'Перечень программного обеспечения, разрешенного к использованию'),
        DType(8, 'Технический паспорт'),
        DType(9, 'Техническое задание'),
        DType(10, 'Протокол аттестационных испытаний'),
        DType(11, 'Заключение по результатам аттестационных испытаний'),
        DType(12, 'Аттестат'),
        DType(13, 'Протокол периодического контроля'),
        DType(14, 'Заключение по результатам периодического контроля'),
        DType(15, 'Заключение по ...'),
 )
#Создвем инф. объекты чтобы создать и заполнить таблицу DDTypes
DDT =  (
        DDType(0, 'Не выбрано'),
        DDType(1, 'Подготовительные мероприятия'),
        DDType(2, 'Аттестационные мероприятия'),
        DDType(3, 'Периодические мероприятия'),
        DDType(4, 'Текущие процессы'),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу OTypes
OT =  (
        OType(0, 'Не выбрано', None),
        OType(1, 'Приказ о контролируемых зонах', None),
        OType(3, 'Приказ о вводе', None),
        OType(4, 'Приказ о выводе', None),
        OType(5, 'Приказ о приостановке аттестата', None),
        OType(6, 'Приказ о внутреннем контроле', None),
        OType(7, 'Приказ об ответственных', None),
        OType(8, 'Распоряжение об ответсвенных', None),
        OType(9, 'Распоряжение об изменении в матрице доступа', None),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу RTypes
RT =  (
        RType(0, 'Не выбрано', ''),
        RType(1, 'Администратор АС', ''),
        RType(2, 'Администратор ИБ', ''),
        RType(3, 'Ответсвенный по защите информации', ''),
        RType(4, 'Оператор', ''),
        RType(5, 'Ответственный за эксплуатацию', ''),
    )
#Создвем инф. объекты чтобы создать и заполнить таблицу STypes
ST =  (
        SType(0, 'Не выбрано'),
        SType(1, 'Защита от ПЭМИН'),
        SType(2, 'Защита от ПЭМИ'),
        SType(3, 'акустическая и вибрационная защита'),
        SType(4, 'защита телефонных линий'),
        SType(5, 'защта от НСД (комплексная)'),
        SType(6, 'СВТ'),
        SType(7, 'МЭ'),
        SType(8, 'СОВ'),
        SType(9, 'антивирусная защита'),
        SType(10, 'доверенная загрузка'),
        SType(11, 'контроль съемных машинных носителей'),
        SType(12, 'ОС'),
        SType(13, 'СКЗИ'),
        SType(14, 'защита ЭЦП'),
        SType(15, 'изделие информационных технологий'),
        SType(16, 'фильтры помехоподавляющие'),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу AKat
AK =  (
        AKat(0, 'без категории'),
        AKat(1, '1 категория значимости'),
        AKat(2, '2 категория значимости'),
        AKat(3, '3 категория значимости'),
      )
#Создвем инф. объекты чтобы создать и заполнить таблицу AKlasses
AKl =  (
        AKlass(0, 'без класса'),
        AKlass(1, 'К1'),
        AKlass(2, 'К2'),
        AKlass(3, 'К3'),
        AKlass(4, 'К4'),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу AStatuses
AS =  (
        AStatus(0, 'Не выбрано'),
        AStatus(1, 'Проектируется'),
        AStatus(2, 'Аттестуется'),
        AStatus(3, 'Действует'),
        AStatus(4, 'Выводится'),
        AStatus(5, 'Выведен'),
        )
#Создвем инф. объекты чтобы создать и заполнить таблицу ATodos
#self.id, self.type
ATo0 =  (ATodo(0, 'Не выбрано'),)

#Создвем инф. объекты чтобы создать и заполнить таблицу AStatuses
SC =  (
        SoftCat(0, 'Не выбрано'),
        SoftCat(1, 'программирование'),
        SoftCat(2, 'запрещенное, соц. сети'),
        SoftCat(3, 'телефония'),
        SoftCat(4, 'административное ПО'),
        SoftCat(5, 'офисное'),
        SoftCat(6, 'мультимедиа'),
        SoftCat(7, 'запрещенное'),
        SoftCat(8, 'другие'),
        )

BD_S = (BD_Soft(0, 'не выбрано', 'не выбрано', None, 'Не выбрано', 'не выбрано', 'не выбрано', 'не выбрано', 'не выбрано'),)
PC_S = (PC_Soft(0, 'не выбрано','не выбрано', None, None, None, None),)
IN_S = (IN_Soft(0, 'не выбрано','не выбрано', None, None, None, None),)
#LSO = (LegsoftOtdel(0, None, None),)
################################################################33
#Создаем тестовые данные
#(self.id, self.year, self.type_id, self.name, self.kat_id, self.klass_id)
assets = (
        Asset(1, 2020, 1, 'Объект КИИ - АРМ оператора машины', 3, 0, 3, None),
        #Asset(2, 2021, 2, 'ИСПДн - Кадровая ЛВС', 0, 4, 3, None),
        #Asset(3, 2022, 2, 'ИСПДн - Финансовая ЛВС', 0, 4, 2, None),
        )

#self.id, self.servise_id, self.numb, self.name, self.lboss_id
otdels = (
        Otdel(0, None, "Не выбрано", "Не выбрано", None),
        #Otdel(1, 1, "01-1", "Отдел бухгалтерии", 8),
        #Otdel(2, 1, "01-2", "Отдел экономистов", 9),
        #Otdel(3, 2, "02-1", "Отдел найма", 10),
        #Otdel(4, 2, "02-2", "Отдел сопровождения", 11),
        #Otdel(5, 3, "03-1", "Отдел программистов", 12),
        #Otdel(6, 3, "03-2", "Отдел тестировщиков", 13),
        )
#self.id, self.numb, self.name, self.boss_id
servises = (
            Servise(0, "Не выбрано", "Не выбрано", None),
            #Servise(1, "01", "Финансовая служба", 14),
            #Servise(2, "02", "Кадровая служба", 15),
            #Servise(3, "03", "Техническая служба", 16),
            )
positions = (
            Position(0, "Не выбрано"),
            #Position(1, "Бухгалтер"),
            #Position(2, "Экономист"),
            #Position(3, "Кадровик"),
            #Position(4, "Менеджер"),
            #Position(5, "Программист"),
            #Position(6, "Тестировщик"),
            #Position(7, "Начальник отдела"),
            #Position(8, "Руководитель службы"),
            )
#self.id, self.sur, self.name, self.patr, self.otd_id, self.trud_id, self.form_id
peoples = (
            People(0, "0", None, "Не выбрано", "Не выбрано", None, None, None),
            #People(1, "001", 1, "Иванов Иван Иванович", "11-11", 1, 1, 0),
            #People(2, "002", 2, "Борисов Петр Петрович", "12-12", 2, 1, 0),
            #People(3, "003", 3, "Лютикова Лия Ивановна", "13-13", 3, 1, 0),
            #People(4, "004", 4, "Лютикова Лия Ивановна", "14-14", 4, 1, 0),
            # People(5, "005", 5, "Ромашкова Анна Викторовна", "15-15", 5, 1, 0),
            #People(6, "006", 5, "Астрова Елена Викторовна", "17-17", 5, 1, 0),
            #People(7, "007", 6, "Астрова Елена Викторовна", "17-17", 6, 1, 0),
            #People(8, "008", 7, "Васильев Василий Васильевич", "18-18", 1, 1, 0),
            #People(9, "009", 7, "Петров Петр Петрович", "19-19", 2, 1, 0),
            #People(10, "010", 7, "Александров Александ Александрович", "20-20", 3, 1, 0),
            #People(11, "011", 7, "Панкратов Иван Иванович", "21-21", 4, 1, 0),
            #People(12, "012", 7, "Семенов Семен Иванович", "22-22", 5, 1, 0),
            #People(13, "013", 7, "Жданов Никовай Иванович", "23-23", 5, 1, 0),
            #People(14, "014", 8, "Черных Геннадий Иванович", "24-24", None, 1, 0),
            #People(15, "015", 8, "Быстрых Валентин Дмитриевич", "25-25", None, 1, 0),
            #People(16, "016", 8, "Дмитриев Никовай Карлович", "26-26", None, 1, 0),
            )
#self.id, self.type_id, self.name, self.numb, self.begin, self.end, self.inv, self.secret_id)
ORDs = (
        ORD(0, None, None, 'Не выбрано', 'Не выбрано', 'Не выбрано', None, None, 'Не выбрано', None),
        #ORD(1, 20, 1, '"Распоряжение о вводе в действие матрицы доступа для финансовой ЛВС" ', '"Распоряжение о вводе в действие матрицы доступа для финансовой ЛВС" от 05.03.2020 № 100', '100', datetime.date(2020, 3, 5), datetime.date(2020, 3, 5), "Дело 1-2", 1),
        #ORD(2, 20, 1, '"Распоряжение о вводе в действие матрицы доступа для кадровой ЛВС"', '"Распоряжение о вводе в действие матрицы доступа для кадровой ЛВС" от 05.03.2020 № 101', '101', datetime.date(2020, 3, 5), datetime.date(2020, 7, 5), "Дело 1-2", 1),
        #ORD(3, 26, 1, '"Приказ о назначении ответсвенных за ИБ в кадровой ИСПДн"', '"Приказ о назначении ответсвенных за ИБ в кадровой ИСПДн" от 03.07.2020 № 11', '11', datetime.date(2020, 1, 3), datetime.date(2020, 7, 3), "Дело 1-1", 1),
        #ORD(4, 26, 1, '"Приказ о назначении ответсвенных за ИБ в финансовой ИСПДн"', '"Приказ о назначении ответсвенных за ИБ в финансовой ИСПДн" от 03.07.2020 № 12', '12', datetime.date(2020, 1, 3), datetime.date(2020, 7, 3), "Дело 1-1", 1),
        #ORD(5, 8, 1, '"Приказ о назначении ответсвенных за эксплуатацию в финансовой ИСПДн"', '"Приказ о назначении ответсвенных за эксплуатацию в финансовой ИСПДн" от 03.01.2020 № 13', '13', datetime.date(2020, 1, 3), datetime.date(2020, 7, 3), "Дело 1-1", 1),
        #ORD(6, 8, 1, '"Приказ о назначении ответсвенных за эксплуатацию в кадровой ИСПДн"', '"Приказ о назначении ответсвенных за эксплуатацию в кадровой ИСПДн" от 03.01.2020 № 14', '14', datetime.date(2020, 1, 3), datetime.date(2020, 7, 3), "Дело 1-1", 1),
        )
#self.id, self.name, self.type, self.people_id, self.ord_id, self.asset_id
users = (
        User(0, "Не выбрано", "Не выбрано", None, None, None),
        #User(1, "ФЛВС-АРМ2-user 1", "локальная" , 2, 1, 3),
        #User(2, "КЛВС-АРМ1-user 1", "локальная" , 3, 2, 2),
        #User(3, "КЛВС-АРМ1-user 2", "локальная" , 4, 2, 2),
        )
#self.id, self.type_id, self.people_id, self.ord_id
responsibles = (
                Responsible(0, "Не выбрано", None, None, None),
                #Responsible(1, "Администратор АС в финансовом", 1, 1, 4),
                #Responsible(2, "Администратор ИБ в финансовом", 2, 13, 4),
                #Responsible(3, "Администратор ИБ в кадровом", 2, 13, 3),
                #Responsible(4, "Администратор АС в кадровом", 1, 4, 3),
                #Responsible(5, "Ответственный по защите информации в кадровом", 3, 11, 3),
                #Responsible(6, "Ответственный по защите информации в финансовом", 3, 9, 4),
                #Responsible(7, "Ответственный за эксплуатацию в кадровом", 5, 10, 6),
                #Responsible(8, "Ответственный за эксплуатацию в финансовом", 5, 8, 5),
                )
#self.id, self.numb, self.terr, self.floor, self.osi, self.attRP_id
Rooms = (
        Room(0, 'Не выбрано', 'Не выбрано', None, 'Не выбрано', None),
        #Room(1, '101', 'I', 1, 'Не выбрано', 2),
        #Room(2, '102', 'I', 1, 'Не выбрано', 2),
        #Room(3, '501', 'II', 5, 'Не выбрано', 1),
        #Room(4, '201', 'I', 2, 'Не выбрано', 1),
        #Room(5, '202', 'I', 2, 'Не выбрано', None),
        #Room(6, '502', 'II', 5, 'Не выбрано', 1),
        #Room(7, '301', 'I', 3, 'Не выбрано', 2),
        )
#(self.id, self.name, self.numb, self.begin, self.end, self.inv, self.secret_id, self.type_id, self.stets, self.vp)
AttestatumRPs = (
                AttestatumRP(0, 'Не выбрано', 'Не выбрано', 'Не выбрано', None, None,'Не выбрано', None,  None, "Не выбрано", "Не выбрано"),
                #AttestatumRP(1, '"Аттестат рабочего помещения 101"',  '"Аттестат рабочего помещения 101" от 05.03.2020 № 888-1', '888-1', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  2, "Нет", "Нет"),
                #AttestatumRP(2, '"Аттестат рабочего помещения 102"',  '"Аттестат рабочего помещения 102" от 05.03.2020 № 888-1', '888-2', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  2, "Нет", "Нет"),
                #AttestatumRP(3, '"Аттестат рабочего помещения 501"',  '"Аттестат рабочего помещения 501" от 05.03.2020 № 888-1', '888-3', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  1, "Нет", "Нет"),
                #AttestatumRP(4, '"Аттестат рабочего помещения 201"',  '"Аттестат рабочего помещения 201" от 05.03.2020 № 888-1', '888-4', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  2, "Нет", "Нет"),
                #AttestatumRP(5, '"Аттестат рабочего помещения 202"',  '"Аттестат рабочего помещения 202" от 05.03.2020 № 888-1', '888-5', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  2, "Нет", "Нет"),
                #AttestatumRP(6, '"Аттестат рабочего помещения 502"',  '"Аттестат рабочего помещения 502" от 05.03.2020 № 888-1', '888-6', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  1, "Нет", "Нет"),
                #AttestatumRP(7, '"Аттестат рабочего помещения 301"',  '"Аттестат рабочего помещения 301" от 05.03.2020 № 888-1', '888-7', datetime.date(2020, 3, 5), datetime.date(2022, 3, 5),'Дело 888', 2,  2, "Нет", "Нет"),
                )
#self.id, self.type_id, self.typeD_id, self.name, self.numb, self.begin, self.end, self.inv, self.secret_id)
Attdocs = (
            Attdoc(0, None, None,  'Не выбрано', 'Не выбрано', 'Не выбрано', None, None, 'Не выбрано', None),
            #Attdoc(1, 9, 1,  '"Акт классификации ИСПДн кадры"', '"Акт классификации ИСПДн кадры" от 05.02.2020 № doc-1', 'doc-1', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(2, 8, 1,  '"Частная модель угроз кадры"', '"Частная модель угроз кадры" от 05.02.2020 № doc-2', 'doc-2', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(3, 7, 1,  '"Перечень программного обеспечения кадры"', '"Перечень программного обеспечения кадры" от 05.02.2020 № doc-3', 'doc-3', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(4, 10, 1,  '"Технический паспорт кадры"', '"Технический паспорт кадры" от 05.02.2020 № doc-4', 'doc-4', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(5, 22, 1,  '"Протокол аттестационных испытаний кадры"', '"Протокол аттестационных испытаний кадры" от 05.02.2020 № doc-5', 'doc-5', datetime.date(2020, 2, 5), datetime.date(2022, 2, 5), 'Дело 3', 1),
            #Attdoc(6, 23, 1,  '"Заключение по результатам аттестационных испытаний кадры" от 05.02.2020 № doc-6', '"Заключение по результатам аттестационных испытаний кадры"', 'doc-6', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(7, 9, 1,  '"Акт классификации ИСПДн финансы"', '"Акт классификации ИСПДн финансы" от 05.02.2020 № doc-7', 'doc-7', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(8, 8, 1,  '"Частная модель угроз финансы"', '"Частная модель угроз финансы" от 05.02.2020 № doc-8', 'doc-8', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(9, 7, 1,  '"Перечень программного обеспечения финансы"', '"Перечень программного обеспечения финансы" от 05.02.2020 № doc-9', 'doc-9', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(10, 10, 1,  '"Технический паспорт финансы"', '"Технический паспорт финансы" от 05.02.2020 № doc-10', 'doc-10', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(11, 22, 1,  '"Протокол аттестационных испытаний финансы"', '"Протокол аттестационных испытаний финансы" от 05.02.2020 № doc-11', 'doc-11', datetime.date(2020, 2, 5), datetime.date(2022, 2, 5), 'Дело 3', 1),
            #Attdoc(12, 23, 1,  '"Заключение по результатам аттестационных испытаний финансы"', '"Заключение по результатам аттестационных испытаний финансы" от 05.02.2020 № doc-12', 'doc-12', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 3', 1),
            #Attdoc(13, 27, 1,  '"Заключение по результатам ... ПК 1"', '"Заключение по результатам ... ПК 1" от 05.02.2020 № sp-1', 'sp-1', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 4', 1),
            #Attdoc(14, 27, 1,  '"Заключение по результатам ... ПК 2"', '"Заключение по результатам ... ПК 2" от 05.02.2020 № sp-1', 'sp-2', datetime.date(2020, 2, 5), datetime.date(2022, 3, 5), 'Дело 4', 1),
            )
            #Создвем инф. объекты чтобы заполнить таблицу Attestatums
#(self.id, self.name, self.numb, self.begin, self.end, self.inv, self.secret_id)
Attestatums = (
                Attestatum(0, 'Не выбрано', 'Не выбрано', None, None, 'Не выбрано', None, None),
                #Attestatum(1, '"Аттестат ИСПДн кадры"', '2020/2 ДСП', datetime.date(2020, 8, 7),datetime.date(2023, 8, 7), 'Дело 3', 1, 2),
                #Attestatum(2, '"Аттестат ИСПДн финансы"', '2020/1 ДСП', datetime.date(2020, 2, 1),datetime.date(2023, 2, 1), 'Дело 3', 1, 3),
                )
#(self.id, self.numb, self.begin, self.end, self.name, self.req_doc, self.scheme, self.end_tp, self.mod_id)
Serts = (
        Sert(0, 1,  None, None, None, "Не выбрано", "Не выбрано", "Не выбрано", None),
        #Sert(1, 3745,  datetime.date(2017, 5, 16), datetime.date(2025, 5, 16), 5, "cредство защиты информации Secret Net Studio", "Соответствует требованиям документов: Требования доверия(4), Требования к МЭ, Профиль защиты МЭ(В четвертого класса защиты. ИТ.МЭ.В4.ПЗ), Требования к САВЗ", "серия", datetime.date(2025, 5, 16)),
        #Sert(2, 3539,  datetime.date(2016, 3, 24), datetime.date(2024, 3, 24), 1, "средство активной защиты информации от утечки за счет побочных электромагнитных излучений и наводок «Соната-Р3.1»", "Соответствует требованиям документов: Требования к САЗ ПЭМИН-2014(А), Требования к САЗ ПЭМИН-2014(Б)", "серия", datetime.date(2024, 3, 24)),
        )
#self.id, self.type_id, self.mod_id self.numb, self.SZZ, , self.sert_id,
SZIs =  (
        SZI(0, None,  'Не выбрано', 'Не выбрано', None),
        #SZI(1, 1,  '33333', 'А33333', 1),
        #SZI(2, 1,  '33334', 'А33334', 1),
        #SZI(3, 2,  '22221', None, 1),
        #SZI(4, 2,  '22222', None, 1),
        #SZI(5, 3,  '11111', 'Б11111', 2),
        #SZI(6, 3,  '11112', 'Б11112', 2),
        )
#self, id, type_id, name, model, numb, SZ, attdoc_id, asset_id
Tehnos = (
            Tehno(0, None, "Не выбрано", "Не выбрано", "Не выбрано", "Не выбрано", None, None),
            #Tehno(1, 1, "Монитор", "Самсунг", "1111", "сз-111", 13, 2),
            #Tehno(2, 2, "Системный", "Юнит", "2222", "сз-112", 13, 2),
            #Tehno(3, 1, "Монитор", "Самсунг", "1112", "сз-113", 14, 3),
            #Tehno(4, 2, "Системный", "Юнит", "2223", "сз-114", 14, 3),
            )
#Создвем инф. объекты чтобы создать и заполнить таблицу SElements
#self.id, self.mode_type, self.mode_name
SElements =  (
            SElement(0, "Не выбрано"),
            SElement(1, "Установочный диск «Secret Net Studio»"),
            SElement(2, "Плата =Touch memory card="),
            SElement(3, "Основной блок «Соната-Р3.1»"),
            )

#Создвем таблицу связи asset-rooms
ar0=asset_rooms.insert().values(id_asset=2, id_room=1)
ar1=asset_rooms.insert().values(id_asset=2, id_room=2)
ar2=asset_rooms.insert().values(id_asset=3, id_room=4)
ar3=asset_rooms.insert().values(id_asset=3, id_room=5)

#Создвем таблицу связи asset-responsibles
are0=asset_responsibles.insert().values(id_asset=2, id_responsible=3)
are1=asset_responsibles.insert().values(id_asset=2, id_responsible=4)
are2=asset_responsibles.insert().values(id_asset=2, id_responsible=5)
are3=asset_responsibles.insert().values(id_asset=2, id_responsible=7)
are4=asset_responsibles.insert().values(id_asset=3, id_responsible=1)
are5=asset_responsibles.insert().values(id_asset=3, id_responsible=2)
are6=asset_responsibles.insert().values(id_asset=3, id_responsible=6)
are7=asset_responsibles.insert().values(id_asset=3, id_responsible=8)

#Создвем таблицу связи asset-SZIs
as0=asset_szis.insert().values(id_asset=2, id_SZI=1)
as1=asset_szis.insert().values(id_asset=2, id_SZI=3)
as2=asset_szis.insert().values(id_asset=2, id_SZI=5)
as3=asset_szis.insert().values(id_asset=3, id_SZI=2)
as4=asset_szis.insert().values(id_asset=3, id_SZI=4)
as5=asset_szis.insert().values(id_asset=3, id_SZI=6)

#Создвем таблицу связи asset-attdocs
ad0=asset_attdocs.insert().values(id_asset=2, id_attdoc=1)
ad1=asset_attdocs.insert().values(id_asset=2, id_attdoc=2)
ad2=asset_attdocs.insert().values(id_asset=2, id_attdoc=3)
ad3=asset_attdocs.insert().values(id_asset=2, id_attdoc=4)
ad4=asset_attdocs.insert().values(id_asset=2, id_attdoc=5)
ad5=asset_attdocs.insert().values(id_asset=2, id_attdoc=6)
ad6=asset_attdocs.insert().values(id_asset=3, id_attdoc=7)
ad7=asset_attdocs.insert().values(id_asset=3, id_attdoc=8)
ad8=asset_attdocs.insert().values(id_asset=3, id_attdoc=9)
ad9=asset_attdocs.insert().values(id_asset=3, id_attdoc=10)
ad10=asset_attdocs.insert().values(id_asset=3, id_attdoc=11)
ad11=asset_attdocs.insert().values(id_asset=3, id_attdoc=12)

#Создвем таблицу связи asset-ords
ao0=asset_ords.insert().values(id_asset=2, id_ord=2)
ao1=asset_ords.insert().values(id_asset=2, id_ord=3)
ao2=asset_ords.insert().values(id_asset=2, id_ord=6)
ao3=asset_ords.insert().values(id_asset=3, id_ord=1)
ao4=asset_ords.insert().values(id_asset=3, id_ord=4)
ao5=asset_ords.insert().values(id_asset=3, id_ord=5)

#Создвем таблицу связи soft_otdels
so0=soft_otdels.insert().values(id_soft=44, id_otdel=11)


executes = [ar0, ar1, ar2, ar3, are0, are1, are2, are3, are4, are5, are6, are7, are0, are0, are0, as0, as1, as2, as3, as4, as5, ad0, ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8, ad9, ad10, ad11, ao0, ao1, ao2, ao3, ao4, ao5]
#Создаем сессию для коммуникации с базой данных
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=conn)
session = Session()

add_list1 = [trud, secret, forms, terrs, RPT, TCtypes, AT, DT, DDT, OT, RT, ST, AK, AKl, AS, ATo0, SC, BD_S, PC_S, IN_S ]
add_list2 = [assets, otdels, servises, positions, peoples, ORDs, users, responsibles, Rooms, AttestatumRPs, Attdocs, Attestatums, Serts, SZIs, SElements, Tehnos]


for item in add_list1:
    session.add_all(item)

for item in add_list2:
    session.add_all(item)


"""
for exe in executes:
    session.execute(exe)
"""
#Завершаем сессию
session.commit()
