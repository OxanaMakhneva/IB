#Test cases to test MainWinModel methods
import unittest
from PyQt5.QtSql import QSqlDatabase
from relations_in_BD_qt import RelField, find_choose_name, find_item_row_MM, find_add_item_id

class RelationsTest(unittest.TestCase):
    #setUp method is overridden from the parent class TestCase
    DB_TYPE = "QSQLITE"
    DB_NAME = "test1.db"
    choose_id = 1

    def setUp(self):
        #Подключаемся к БД
        self.db = QSqlDatabase(self.DB_TYPE)
        self.db.setDatabaseName(self.DB_NAME)
        self.db.open()
        #Создаем тестируемый объект
        self.rel_Assets_Attestatums = RelField(type = "ManyTab-OneBag", table_tab = "Attestatums", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "asset_id", fkey_bag_idx = 7, table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0)
        self.rel_Assets_Rooms = RelField(type = "ManyTab-ManyBag", table_tab = "Rooms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_rooms", pfkey_tab = "id_room", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Assets_Attdocs = RelField(type = "ManyTab-ManyBag", table_tab = "Attdocs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_attdocs", pfkey_tab = "id_attdoc", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Assets_ORDs = RelField(type = "ManyTab-ManyBag", table_tab = "ORDs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_ords", pfkey_tab = "id_ord", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Assets_SZIs = RelField(type = "ManyTab-ManyBag", table_tab = "SZIs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_SZIs", pfkey_tab = "id_SZI", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Assets_Responsibles = RelField(type = "ManyTab-ManyBag", table_tab = "Responsibles", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_responsibles", pfkey_tab = "id_responsible", pfkey_tab_idx = 1,  pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Assets_Users = RelField(type = "ManyTab-OneBag", table_tab = "Users", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "asset_id", fkey_bag_idx = 5, table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0)
        self.rel_Assets_AttestatumRPs = RelField(type = "OneTab-ManyBt-ManyBt-ManyBag", table_tab = "AttestatumRPs", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "Rooms", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "attRP_id", fkey_tab_idx = 5, table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_bag = "asset_rooms", pfkey_bt_bag = "id_room", pfkey_bt_bag_idx = 1, pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Assets_Serts = RelField(type = "OneTab-ManyBt-ManyBt-ManyBag", table_tab = "Serts", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "SZIs", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "sert_id", fkey_tab_idx = 5, table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0, table_prom_bag = "asset_SZIs", pfkey_bt_bag = "id_SZI", pfkey_bt_bag_idx = 1, pfkey_bag = "id_asset", pfkey_bag_idx = 0)
        self.rel_Attdocs_Assets = RelField(type = "ManyTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Attdocs", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_attdocs", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_attdoc", pfkey_bag_idx = 1)
        self.rel_AttestatumRPs_Rooms = RelField(type = "ManyTab-OneBag", table_tab = "Rooms", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "attRP_id", fkey_bag_idx = 5, table_bag = "AttestatumRPs", pkey_bag = "id", pkey_bag_idx = 0)
        self.rel_AttestatumRPs_Assets = RelField(type = "ManyTab-ManyBt-ManyBt-OneBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0, table_bt = "Rooms", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "attRP_id", fkey_bag_idx = 5, table_bag = "AttestatumRPs", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_rooms", pfkey_bt_tab = "id_room", pfkey_bt_tab_idx = 1, pfkey_tab = "id_asset", pfkey_tab_idx = 0)
        self.rel_Attestatums_Assets = RelField(type = "OneTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Attestatums", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "asset_id", fkey_tab_idx = 7)
        self.rel_ORDs_Assets = RelField(type = "ManyTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "ORDs", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_ords", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_ord", pfkey_bag_idx = 1)
        self.rel_Peoples_Users = RelField(type = "ManyTab-OneBag", table_tab = "Users", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "people_id", fkey_bag_idx = 3, table_bag = "Peoples", pkey_bag = "id", pkey_bag_idx = 0)
        self.rel_Peoples_Responsibles = RelField(type = "ManyTab-OneBag", table_tab = "Responsibles", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "people_id", fkey_bag_idx = 3, table_bag = "Peoples", pkey_bag = "id", pkey_bag_idx = 0)
        self.rel_Peoples_ORDs_user = RelField(type = "OneTab-ManyBt-ManyBt-OneBag", table_tab = "ORDs", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "Users", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4, table_bag = "Peoples", pkey_bag = "id", pkey_bag_idx = 0, fkey_bag = "people_id", fkey_bt_bag_idx = 3)
        self.rel_Peoples_ORDs_resp = RelField(type = "OneTab-ManyBt-ManyBt-OneBag", table_tab = "ORDs", pkey_tab = "id", pkey_tab_idx = 0, fkey_bt_tab = "", fkey_bt_tab_idx = "", table_bt = "Responsibles", pkey_bt = "id", pkey_bt_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4, table_bag = "Peoples", pkey_bag = "id", pkey_bag_idx = 0, fkey_bag = "people_id", fkey_bt_bag_idx = 3)
        self.rel_Responsibles_Peoples = RelField(type = "OneTab-ManyBag", table_tab = "Peoples", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Responsibles", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "people_id", fkey_tab_idx = 3)
        self.rel_Responsibles_ORDs = RelField(type = "OneTab-ManyBag", table_tab = "ORDs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Responsibles", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4)
        self.rel_Rooms_AttestatumRPs = RelField(type = "OneTab-ManyBag", table_tab = "AttestatumRPs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Rooms", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "attRP_id", fkey_tab_idx = 5)
        self.rel_Rooms_Assets = RelField(type = "ManyTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Rooms", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_rooms", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_room", pfkey_bag_idx = 1)
        self.rel_Serts_SZIs = RelField(type = "ManyTab-OneBag", table_tab = "SZIs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "sert_id", fkey_bag_idx = 4, table_bag = "Serts", pkey_bag = "id", pkey_bag_idx = 0)
        self.rel_Serts_Assets = RelField(type = "ManyTab-ManyBt-ManyBt-OneBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0, table_bt = "SZIs", pkey_bt = "id", pkey_bt_idx = 0, fkey_bag = "sert_id", fkey_bag_idx = 4, table_bag = "Serts", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_SZIs", pfkey_bt_tab = "id_SZI", pfkey_bt_tab_idx = 1, pfkey_tab = "id_asset", pfkey_tab_idx = 0)
        self.rel_SZIs_Serts = RelField(type = "OneTab-ManyBag", table_tab = "Serts", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "SZIs", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "sert_id", fkey_tab_idx = 4)
        self.rel_SZIs_Assets = RelField(type = "ManyTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "SZIs", pkey_bag = "id", pkey_bag_idx = 0, table_prom_tab = "asset_SZIs", pfkey_tab = "id_asset", pfkey_tab_idx = 0, pfkey_bag = "id_SZI", pfkey_bag_idx = 1)
        self.rel_Tehnos_Attdocs = RelField(type = "OneTab-ManyBag", table_tab = "Attdocs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Tehnos", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "attdoc_id", fkey_tab_idx = 6)
        self.rel_Tehnos_Assets = RelField(type = "OneTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Tehnos", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "asset_id", fkey_tab_idx = 7)
        self.rel_Users_Peoples = RelField(type = "OneTab-ManyBag", table_tab = "Peoples", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Users", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "people_id", fkey_tab_idx = 3)
        self.rel_Users_ORDs = RelField(type = "OneTab-ManyBag", table_tab = "ORDs", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Users", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "ord_id", fkey_tab_idx = 4)
        self.rel_Users_Assets = RelField(type = "OneTab-ManyBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  fkey_bag = "", fkey_bag_idx = "", table_bag = "Users", pkey_bag = "id", pkey_bag_idx = 0, fkey_tab = "asset_id", fkey_tab_idx = 5)

    def test_find_id_level1_Assets_Attestatums_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = []
        rez = self.rel_Assets_Attestatums.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Attestatums_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1]
        rez = self.rel_Assets_Attestatums.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Attestatums_chooseNULL(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = None
        assert_rez = []
        rez = self.rel_Assets_Attestatums.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_Attestatums_choose1(self):
        id_list = []
        assert_rez = f' Assets.id = 9999999 '
        rez = self.rel_Assets_Attestatums.find_str_level(id_list)

    def test_find_str_level_Assets_Attestatums_choose2(self):
        id_list = [1]
        assert_rez = f' Assets.id = 1 '
        rez = self.rel_Assets_Attestatums.find_str_level(id_list)

    def test_find_id_level1_Assets_Rooms_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = []
        rez = self.rel_Assets_Rooms.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Rooms_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1,2]
        rez = self.rel_Assets_Rooms.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Rooms_choose4(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 4
        assert_rez = []
        rez = self.rel_Assets_Rooms.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_Rooms_choose1(self):
        id_list = []
        assert_rez = f' Assets.id = 9999999 '
        rez = self.rel_Assets_Rooms.find_str_level(id_list)

    def test_find_str_level_Assets_Rooms_choose2(self):
        id_list = [1, 2]
        assert_rez = f' Assets.id = 1 OR Assets.id = 2 '
        rez = self.rel_Assets_Rooms.find_str_level(id_list)

    def test_find_id_level1_Assets_Attdocs_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1, 2, 3, 4, 5, 6]
        rez = self.rel_Assets_Attdocs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Attdocs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = []
        rez = self.rel_Assets_Attdocs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_Attdocs_choose2(self):
        id_list = [1, 2, 3, 4, 5, 6]
        assert_rez = f' Assets.id = 1 OR Assets.id = 2 OR Assets.id = 3 OR Assets.id = 4 OR Assets.id = 5 OR Assets.id = 6 '
        rez = self.rel_Assets_Attdocs.find_str_level(id_list)

    def test_find_id_level1_Assets_ORDs_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [1, 4, 5]
        rez = self.rel_Assets_ORDs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_ORDs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = []
        rez = self.rel_Assets_ORDs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_ORDs_choose3(self):
        id_list = [1, 4, 5]
        assert_rez = f' Assets.id = 1 OR Assets.id = 4 OR Assets.id = 5 '
        rez = self.rel_Assets_ORDs.find_str_level(id_list)

    def test_find_id_level1_Assets_SZIs_choose3 (self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [2, 4, 6]
        rez = self.rel_Assets_SZIs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_SZIs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = []
        rez = self.rel_Assets_SZIs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_SZIs_choose3(self):
        id_list = [2, 4, 6]
        assert_rez = f' Assets.id = 2 OR Assets.id = 4 OR Assets.id = 6 '
        rez = self.rel_Assets_SZIs.find_str_level(id_list)

    def test_find_id_level1_Assets_Responsibles_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [3, 4, 5, 7]
        rez = self.rel_Assets_Responsibles.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Responsibles_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [1, 2, 6, 8]
        rez = self.rel_Assets_Responsibles.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_Responsibles_choose3(self):
        id_list = [1, 2, 6, 8]
        assert_rez = f' Assets.id = 1 OR Assets.id = 2 OR Assets.id = 6 OR Assets.id = 8 '
        rez = self.rel_Assets_Responsibles.find_str_level(id_list)

    def test_find_id_level1_Assets_Users_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [0, 1]
        rez = self.rel_Assets_Users.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Assets_Users_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [2, 3]
        rez = self.rel_Assets_Users.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_Users_choose2(self):
        id_list = [2, 3]
        assert_rez = f' Assets.id = 2 OR Assets.id = 3 '
        rez = self.rel_Assets_Users.find_str_level(id_list)

    def test_find_id_level2_Assets_AttestatumRPs_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [2]
        rez = self.rel_Assets_AttestatumRPs.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Assets_AttestatumRPs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = []
        rez = self.rel_Assets_AttestatumRPs.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Assets_AttestatumRPs_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [1]
        rez = self.rel_Assets_AttestatumRPs.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_AttestatumRPs_choose3(self):
        id_list = [1]
        assert_rez = f' Assets.id = 1 '
        rez = self.rel_Assets_AttestatumRPs.find_str_level(id_list)

    def test_find_id_level2_Assets_Serts_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1, 2]
        rez = self.rel_Assets_Serts.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Assets_Serts_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [1, 2]
        rez = self.rel_Assets_Serts.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Assets_Serts_choose3(self):
        id_list = [1, 2]
        assert_rez = f' Assets.id = 1 OR Assets.id = 2 '
        rez = self.rel_Assets_AttestatumRPs.find_str_level(id_list)

    def test_find_id_level1_Attdocs_Assets_choose6(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 6
        assert_rez = [2]
        rez = self.rel_Attdocs_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Attdocs_Assets_choose10(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 10
        assert_rez = [3]
        rez = self.rel_Attdocs_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Attdocs_Assets_choose10(self):
        id_list = [3]
        assert_rez = f' Attdocs.id = 3 '
        rez = self.rel_Attdocs_Assets.find_str_level(id_list)

    def test_find_id_level1_AttestatumRPs_Rooms_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1, 2, 7]
        rez = self.rel_AttestatumRPs_Rooms.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_AttestatumRPs_Rooms_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [3, 4, 6]
        rez = self.rel_AttestatumRPs_Rooms.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_AttestatumRPs_Rooms_choose1(self):
        id_list = [3, 4, 6]
        assert_rez = f' AttestatumRPs.id = 3 OR AttestatumRPs.id = 4 OR AttestatumRPs.id = 6 '
        rez = self.rel_AttestatumRPs_Rooms.find_str_level(id_list)

    def test_find_id_level2_AttestatumRPs_Assets_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [3]
        rez = self.rel_AttestatumRPs_Assets.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_AttestatumRPs_Assets_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [2]
        rez = self.rel_AttestatumRPs_Assets.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_AttestatumRPs_Assets_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = []
        rez = self.rel_AttestatumRPs_Assets.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_AttestatumRPs_Assets_choose2(self):
        id_list = [2]
        assert_rez = f' AttestatumRPs.id = 2 '
        rez = self.rel_AttestatumRPs_Assets.find_str_level(id_list)

    def test_find_id_level1_Attestatums_Assets_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [2]
        rez = self.rel_Attestatums_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Attestatums_Assets_choose0(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 0
        assert_rez = []
        rez = self.rel_Attestatums_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Attestatums_Assets_choose2(self):
        id_list = [2]
        assert_rez = f' Attestatums.id = 2 '
        rez = self.rel_Attestatums_Assets.find_str_level(id_list)

    def test_find_id_level1_ORDs_Assets_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [3]
        rez = self.rel_ORDs_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_ORDs_Assets_choose6(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 6
        assert_rez = [2]
        rez = self.rel_ORDs_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_ORDs_Assets_choose6(self):
        id_list = [2]
        assert_rez = f' ORDs.id = 2 '
        rez = self.rel_ORDs_Assets.find_str_level(id_list)

    def test_find_id_level1_Peoples_Users_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1]
        rez = self.rel_Peoples_Users.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Peoples_Users_choose4(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 4
        assert_rez = [3]
        rez = self.rel_Peoples_Users.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Peoples_Users_choose2(self):
        id_list = [1]
        assert_rez = f' Peoples.id = 1 '
        rez = self.rel_Peoples_Users.find_str_level(id_list)

    def test_find_id_level1_Peoples_Responsibles_choose11(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 11
        assert_rez = [5]
        rez = self.rel_Peoples_Responsibles.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Peoples_Responsibles_choose10(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 10
        assert_rez = [7]
        rez = self.rel_Peoples_Responsibles.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Peoples_Responsibles_choose10(self):
        id_list = [7]
        assert_rez = f' Peoples.id = 7 '
        rez = self.rel_Peoples_Responsibles.find_str_level(id_list)

    def test_find_id_level2_Peoples_ORDs_user_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [2]
        rez = self.rel_Peoples_ORDs_user.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Peoples_ORDs_user_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1]
        rez = self.rel_Peoples_ORDs_user.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_str_level_Peoples_ORDs_user_choose2(self):
        id_list = [1]
        assert_rez = f' Peoples.id = 1 '
        rez = self.rel_Peoples_ORDs_user.find_str_level(id_list)

    def test_find_id_level2_Peoples_ORDs_resp_choose13(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 13
        assert_rez = [3, 4]
        rez = self.rel_Peoples_ORDs_resp.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Peoples_ORDs_resp_choose9(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 9
        assert_rez = [4]
        rez = self.rel_Peoples_ORDs_resp.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Responsibles_Peoples_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [13]
        rez = self.rel_Responsibles_Peoples.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Responsibles_Peoples_choose7(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 7
        assert_rez = [10]
        rez = self.rel_Responsibles_Peoples.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Responsibles_ORDs_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [4]
        rez = self.rel_Responsibles_ORDs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Responsibles_ORDs_choose4(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 4
        assert_rez = [3]
        rez = self.rel_Responsibles_ORDs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Rooms_AttestatumRPs_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [1]
        rez = self.rel_Rooms_AttestatumRPs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Rooms_AttestatumRPs_choose6(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 6
        assert_rez = [1]
        rez = self.rel_Rooms_AttestatumRPs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Rooms_Assets_choose4(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 4
        assert_rez = [3]
        rez = self.rel_Rooms_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Rooms_Assets_choose5(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 5
        assert_rez = [3]
        rez = self.rel_Rooms_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Serts_SZIs_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [5, 6]
        rez = self.rel_Serts_SZIs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Serts_SZIs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [1,2,3,4]
        rez = self.rel_Serts_SZIs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Serts_Assets_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [2, 3]
        rez = self.rel_Serts_Assets.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level2_Serts_Assets_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [2, 3]
        rez = self.rel_Serts_Assets.find_id_level2(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_SZIs_Serts_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [1]
        rez = self.rel_SZIs_Serts.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_SZIs_Serts_choose5(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 5
        assert_rez = [2]
        rez = self.rel_SZIs_Serts.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_SZIs_Assets_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [2]
        rez = self.rel_SZIs_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_SZIs_Assets_choose4(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 4
        assert_rez = [3]
        rez = self.rel_SZIs_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Tehnos_Attdocs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [13]
        rez = self.rel_Tehnos_Attdocs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Tehnos_Attdocs_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [14]
        rez = self.rel_Tehnos_Attdocs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Tehnos_Assets_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [2]
        rez = self.rel_Tehnos_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Users_Peoples_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [2]
        rez = self.rel_Users_Peoples.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Users_Peoples_choose2(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 2
        assert_rez = [3]
        rez = self.rel_Users_Peoples.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Users_ORDs_choose1(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [1]
        rez = self.rel_Users_ORDs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Users_ORDs_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [2]
        rez = self.rel_Users_ORDs.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Users_Assets_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 1
        assert_rez = [3]
        rez = self.rel_Users_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)

    def test_find_id_level1_Users_Assets_choose3(self):
        #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
        choose_id = 3
        assert_rez = [2]
        rez = self.rel_Users_Assets.find_id_level1(self.db, choose_id)
        self.assertEqual(rez, assert_rez)




# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
