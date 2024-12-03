from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        main_menu = MainMenu(self)
        self.setMenuBar(main_menu)
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)

    @pyqtSlot()
    def about(self):
        title = "Программа для управления заданиями для учащихся"
        text = (
            "Программа для управления задачами и заданиями " +
            "для учащихся школы"
        )
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(
            self,
            "Программа для управления заданиями для учащихся")
