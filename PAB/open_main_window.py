from models.model_MainWin import MainWindow
import app_logger
import sys
#Классы из QT
from PyQt5.QtWidgets import QApplication

logger = app_logger.get_logger(__name__)
logger.info("Запуск приложения")

#Запуск приложения
app = QApplication(sys.argv)
app.setStyle('Fusion')
module_name = "assets"
max_width = app.screens()[0].availableSize().width()
window = MainWindow.open_main_window(window = None, config_module_name = module_name, max_width = max_width)
window.show()
app.exec_()
