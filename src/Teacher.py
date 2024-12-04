from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QTableView, QWidget, QMessageBox


class TeacherModel(QSqlQueryModel):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        sql = '''
            select id, full_name, phone, email, comment
            from teachers;
        '''
        self.setQuery(sql)


class TeacherView(QTableView):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        model = TeacherModel(self)
        self.setModel(model)

    @pyqtSlot()
    def add(self):
        QMessageBox.information(self, "Учитель", "Добавление")

    @pyqtSlot()
    def update(self):
        QMessageBox.information(self, "Учитель", "Редактироваие")

    @pyqtSlot()
    def delete(self):
        QMessageBox.information(self, "Учитель", "Удаление")
