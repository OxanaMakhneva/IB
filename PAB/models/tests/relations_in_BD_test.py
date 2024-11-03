#Test cases to test MainWinModel methods
import unittest
from ..BD.models.relations_in_BD_qt import RelField, find_choose_name, find_item_row_MM, find_add_item_id

class RelationsTest(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
  DB_TYPE = "QSQLITE"
  DB_NAME = "test1.db"
  choose_id = 1

  def setUp(self):
    #Подключаемся к БД
    self.db = QSqlDatabase(DB_TYPE)
    self.db.setDatabaseName(DB_NAME)
    self.db.open()

  def test_find_id_level1_ManyTab_OneBag_null(self):
      #Ищем список id из таблицы "Attestatums" ("table_tab"), связанных с выбранной записью в таблице "Assets" ("table_bag")
      #Создаем тестируемый объект
      kwargs = {"type":       "ManyTab-OneBag",
                 "table_tab":  "Attestatums",
                 "pkey_tab":   "id",
                 "pkey_tab_idx": 0,
                 "fkey_bag": "asset_id",
                 "fkey_bag_idx": 7,
                 "table_bag": "Assets",
                 "pkey_bag":  "id",
                 "pkey_bag_idx": 0}
      rel = RelField(type = "OneTab-NoBag", table_tab = "Assets", pkey_tab = "id", pkey_tab_idx = 0,  table_bag = "Assets", pkey_bag = "id", pkey_bag_idx = 0)
      choose_id = 1
      assert_rez = []
      rez = self.find_id_level1(self.db, choose_id)
      self.assertEqual(rez, assert_rez)

# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
