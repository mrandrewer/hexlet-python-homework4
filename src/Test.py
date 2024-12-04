from PyQt5.QtSql import (
    QSqlTableModel,
    QSqlQuery
)
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QTableView,
    QWidget,
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStyledItemDelegate,
    QStyleOptionViewItem
)


class TestModel(QSqlTableModel):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.setTable('tests')
        self.setHeaderData(1, Qt.Horizontal, "Автор")
        self.setHeaderData(2, Qt.Horizontal, "Название")
        self.setHeaderData(3, Qt.Horizontal, "Содержание")
        self.setEditStrategy(self.OnRowChange)
        self.select()

    def get(self, id):
        self.select()
        for i in range(0, self.rowCount()):
            rec = self.record(i)
            if rec.field('id').value() == id:
                return rec.field('name').value()
        return None

    def add(self, author, name, content):
        rec = self.record()
        rec.clearValues()
        print(author, name, content)
        rec.setGenerated("id", False)
        rec.setValue('teacher_id', author)
        rec.setValue('name', name)
        rec.setValue('content', content)
        self.insertRecord(-1, rec)
        self.submitAll()
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


class TestView(QTableView):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        model = TestModel(parent=self)
        self.setModel(model)
        self.setItemDelegateForColumn(1, TestAuthorDelegate(self))
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(3, hh.Stretch)

    def add(self):
        dialog = TestDialog(self.model().get_authors(), self)
        if dialog.exec():
            self.model().add(
                dialog.author,
                dialog.name,
                dialog.content
            )

    def delete(self):
        row = self.currentIndex().row()
        test_id = self.model().record(row).value('id')
        test_name = self.model().get(test_id)
        if not test_name:
            QMessageBox.warning(
                self,
                "Задача",
                "Задача не была найден в базе")
            return
        ans = QMessageBox.question(
            self,
            "Задача",
            f"Вы уверены что хотите удалить задачу {test_name}")
        if ans == QMessageBox.Yes:
            self.model().delete(test_id)


class TestDialog(QDialog):

    def __init__(self, authors, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.setWindowTitle("Задание")

        author_lbl = QLabel("&Автор", parent=self)
        self.__author_edit = QComboBox(parent=self)
        author_lbl.setBuddy(self.__author_edit)
        self.__author_edit.addItem("", None)
        for id, name in authors.items():
            self.__author_edit.addItem(name, id)

        name_lbl = QLabel("&Название", parent=self)
        self.__name_edit = QLineEdit(parent=self)
        name_lbl.setBuddy(self.__name_edit)

        content_lbl = QLabel("&Содержание", parent=self)
        self.__content_edit = QTextEdit(parent=self)
        content_lbl.setBuddy(self.__content_edit)

        ok_btn = QPushButton("ОК", parent=self)
        cancel_btn = QPushButton("Отмена", parent=self)

        layout = QVBoxLayout()
        layout.addWidget(author_lbl)
        layout.addWidget(self.__author_edit)
        layout.addWidget(name_lbl)
        layout.addWidget(self.__name_edit)
        layout.addWidget(content_lbl)
        layout.addWidget(self.__content_edit)

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
        if self.content is None:
            return
        self.accept()

    @property
    def author(self):
        return self.__author_edit.currentData()

    @property
    def name(self):
        result = self.__name_edit.text().strip()
        return None if result == '' else result

    @property
    def content(self):
        result = self.__content_edit.toPlainText().strip()
        return None if result == '' else result


class TestAuthorDelegate(QStyledItemDelegate):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)

    def createEditor(
            self,
            parent: QWidget | None,
            option: QStyleOptionViewItem,
            index: QModelIndex) -> QWidget | None:
        author_edit = QComboBox(parent)
        author_edit.addItem("", None)
        for id, name in index.model().get_authors().items():
            author_edit.addItem(name, id)
        return author_edit

    def setEditorData(
            self,
            editor: QWidget | None,
            index: QModelIndex) -> None:
        item_index = editor.findData(index.data())
        editor.setCurrentIndex(item_index)

    def setModelData(
            self,
            editor: QWidget | None,
            model: QAbstractItemModel | None,
            index: QModelIndex) -> None:
        model.setData(index, editor.currentData())
