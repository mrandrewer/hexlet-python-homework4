from PyQt5.QtSql import (
    QSqlRelationalTableModel,
    QSqlRelation,
    QSqlRelationalDelegate,
    QSqlQuery
)
from PyQt5.QtCore import (
    QObject,
    Qt,
    pyqtSlot
)
from PyQt5.QtWidgets import (
    QTableView,
    QWidget,
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class VariantModel(QSqlRelationalTableModel):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.setTable('variants')
        self.setRelation(1, QSqlRelation('teachers', 'id', 'full_name'))
        self.setHeaderData(1, Qt.Horizontal, "Автор")
        self.setHeaderData(2, Qt.Horizontal, "Название")
        self.setHeaderData(3, Qt.Horizontal, "Создан")
        self.setEditStrategy(self.OnRowChange)
        self.select()

    def get(self, id):
        self.select()
        for i in range(0, self.rowCount()):
            rec = self.record(i)
            if rec.field('id').value() == id:
                return rec.field('title').value()
        return None

    def add(self, author, title):
        print(author, title)
        self.submitAll()
        add_query = QSqlQuery()
        sql = '''
            insert into variants (teacher_id, title)
            values ( :teacher_id, :title);
        '''
        add_query.prepare(sql)
        add_query.bindValue(':teacher_id', author)
        add_query.bindValue(':title', title)
        add_query.exec_()
        self.select()

    def delete(self, id):
        self.select()
        for i in range(0, self.rowCount()):
            rec = self.record(i)
            if rec.field('id').value() == id:
                self.removeRow(i)
                self.submitAll()
                break
        self.select()

    def get_authors(self):
        sel_query = QSqlQuery()
        sql = '''
            select id, full_name
            from teachers;
        '''
        sel_query.exec_(sql)
        authors = {}
        if sel_query.isActive():
            sel_query.first()
            while sel_query.isValid():
                authors[sel_query.value('id')] = sel_query.value('full_name')
                sel_query.next()
        return authors


class VariantView(QTableView):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        model = VariantModel(parent=self)
        self.setModel(model)
        self.setItemDelegate(QSqlRelationalDelegate(self))
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(2, hh.Stretch)

    def add(self):
        dialog = VariantDialog(self.model().get_authors(), self)
        if dialog.exec():
            self.model().add(
                dialog.author,
                dialog.title
            )

    def delete(self):
        row = self.currentIndex().row()
        variant_id = self.model().record(row).value('id')
        variant_name = self.model().get(variant_id)
        if not variant_name:
            QMessageBox.warning(
                self,
                "Вариант",
                "Вариант не был найден в базе")
            return
        ans = QMessageBox.question(
            self,
            "Вариант",
            f"Вы уверены что хотите удалить вариант {variant_name}?")
        if ans == QMessageBox.Yes:
            self.model().delete(variant_id)


class VariantDialog(QDialog):

    def __init__(self, authors, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.setWindowTitle("Задание")

        author_lbl = QLabel("&Автор", parent=self)
        self.__author_edit = QComboBox(parent=self)
        author_lbl.setBuddy(self.__author_edit)
        for id, name in authors.items():
            self.__author_edit.addItem(name, id)

        title_lbl = QLabel("&Название", parent=self)
        self.__title_edit = QLineEdit(parent=self)
        title_lbl.setBuddy(self.__title_edit)

        ok_btn = QPushButton("ОК", parent=self)
        cancel_btn = QPushButton("Отмена", parent=self)

        layout = QVBoxLayout()
        layout.addWidget(author_lbl)
        layout.addWidget(self.__author_edit)
        layout.addWidget(title_lbl)
        layout.addWidget(self.__title_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        ok_btn.clicked.connect(self.finish)
        cancel_btn.clicked.connect(self.reject)

    @pyqtSlot()
    def finish(self):
        if self.author is None or self.title is None:
            return
        self.accept()

    @property
    def author(self):
        return self.__author_edit.currentData()

    @property
    def title(self):
        result = self.__title_edit.text().strip()
        return None if result == '' else result
