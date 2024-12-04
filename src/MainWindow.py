from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QMessageBox,
    QVBoxLayout
)
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu
from Teacher import TeacherView
from Test import TestView


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        widget = QWidget(self)
        teacher_view = TeacherView(widget)
        test_view = TestView(widget)
        layout = QVBoxLayout()
        layout.addWidget(teacher_view)
        layout.addWidget(test_view)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        main_menu = MainMenu(self)
        self.setMenuBar(main_menu)
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.teacher_add.triggered.connect(teacher_view.add)
        main_menu.teacher_update.triggered.connect(teacher_view.update)
        main_menu.teacher_delete.triggered.connect(teacher_view.delete)
        main_menu.test_add.triggered.connect(test_view.add)
        main_menu.test_update.triggered.connect(test_view.update)
        main_menu.test_delete.triggered.connect(test_view.delete)

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
