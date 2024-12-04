from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QTableView,
    QWidget,
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)


class TestModel(QSqlTableModel):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.setTable('tests')
        self.setHeaderData(1, Qt.Horizontal, "Автор")
        self.setHeaderData(2, Qt.Horizontal, "Название")
        self.setHeaderData(3, Qt.Horizontal, "Содержание")
        self.select()


class TestView(QTableView):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        model = TestModel(parent=self)
        self.setModel(model)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(3, hh.Stretch)

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class TestDialog(QDialog):
    pass
