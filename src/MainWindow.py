from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu
from Teacher import TeacherView


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        main_menu = MainMenu(self)
        self.setMenuBar(main_menu)
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)

        widget = QWidget(self)
        view = TeacherView(widget)
        layout = QVBoxLayout()
        layout.addWidget(view)
        add_btn = QPushButton("Добавить", parent=widget)
        add_btn.clicked.connect(view.add)
        update_btn = QPushButton("Редактировать", parent=widget)
        update_btn.clicked.connect(view.update)
        delete_btn = QPushButton("Удалить", parent=widget)
        delete_btn.clicked.connect(view.delete)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

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
