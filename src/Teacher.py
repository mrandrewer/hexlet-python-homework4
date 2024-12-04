from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
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


class TeacherModel(QSqlQueryModel):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.refresh_data()
        self.setHeaderData(1, Qt.Horizontal, "ФИО")
        self.setHeaderData(2, Qt.Horizontal, "Телефон")
        self.setHeaderData(3, Qt.Horizontal, "Email")
        self.setHeaderData(4, Qt.Horizontal, "Комментарий")

    def refresh_data(self):
        sql = '''
            select id, full_name, phone, email, comment
            from teachers;
        '''
        self.setQuery(sql)

    def get(self, id):
        sql = '''
            select full_name, phone, email, comment
            from teachers
            where id = :id;
        '''
        get_query = QSqlQuery()
        get_query.prepare(sql)
        get_query.bindValue(':id', id)
        get_query.exec_()
        if get_query.isActive():
            get_query.first()
            return (
                get_query.value('full_name'),
                get_query.value('phone'),
                get_query.value('email'),
                get_query.value('comment')
            )
        self.refresh_data()
        return ('', '', '', '')

    def add(self, full_name, phone, email, comment):
        add_query = QSqlQuery()
        sql = '''
            insert into teachers (full_name, phone, email, comment)
            values ( :full_name, :phone, :email, :comment);
        '''
        add_query.prepare(sql)
        add_query.bindValue(':full_name', full_name[:500])
        add_query.bindValue(':phone', phone[:12])
        add_query.bindValue(':email', email[:100])
        add_query.bindValue(':comment', comment)
        add_query.exec_()
        self.refresh_data()

    def update(self, id, full_name, phone, email, comment):
        upd_query = QSqlQuery()
        sql = '''
            update teachers set
                full_name = :full_name,
                phone = :phone,
                email = :email,
                comment = :comment
            where id = :id;
        '''
        upd_query.prepare(sql)
        upd_query.bindValue(':id', id)
        upd_query.bindValue(':full_name', full_name[:500])
        upd_query.bindValue(':phone', phone[:12])
        upd_query.bindValue(':email', email[:100])
        upd_query.bindValue(':comment', comment)
        upd_query.exec_()
        self.refresh_data()

    def delete(self, id):
        del_query = QSqlQuery()
        sql = '''
            delete from teachers
            where id = :id;
        '''
        del_query.prepare(sql)
        del_query.bindValue(':id', id)
        del_query.exec_()
        self.refresh_data()


class TeacherView(QTableView):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        model = TeacherModel(self)
        self.setModel(model)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(4, hh.Stretch)

    @pyqtSlot()
    def add(self):
        dialog = TeacherDialog(self)
        if dialog.exec():
            self.model().add(
                dialog.full_name,
                dialog.phone,
                dialog.email,
                dialog.comment
            )

    @pyqtSlot()
    def update(self):
        dialog = TeacherDialog(self)
        row = self.currentIndex().row()
        teacher_id = self.model().record(row).value(0)
        (full_name, phone, email, comment) = self.model().get(teacher_id)
        if not full_name:
            QMessageBox.warning(
                self,
                "Учитель",
                "Учитель не был найден в базе")
            return
        dialog.full_name = full_name
        dialog.phone = phone
        dialog.email = email
        dialog.comment = comment
        if dialog.exec():
            self.model().update(
                teacher_id,
                dialog.full_name,
                dialog.phone,
                dialog.email,
                dialog.comment
            )

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        teacher_id = self.model().record(row).value(0)
        (full_name, _, _, _) = self.model().get(teacher_id)
        if not full_name:
            QMessageBox.warning(
                self,
                "Учитель",
                "Учитель не был найден в базе")
            return
        ans = QMessageBox.question(
            self,
            "Учитель",
            f"Вы уверены что хотите удалить учителя {full_name}")
        if ans == QMessageBox.Yes:
            self.model().delete(teacher_id)


class TeacherDialog(QDialog):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.setWindowTitle("Учитель")

        full_name_lbl = QLabel("&ФИО", parent=self)
        self.__full_name_edit = QLineEdit(parent=self)
        full_name_lbl.setBuddy(self.__full_name_edit)

        phone_lbl = QLabel("&Телефон", parent=self)
        self.__phone_edit = QLineEdit(parent=self)
        phone_lbl.setBuddy(self.__phone_edit)

        email_lbl = QLabel("&Email", parent=self)
        self.__email_edit = QLineEdit(parent=self)
        email_lbl.setBuddy(self.__email_edit)

        comment_lbl = QLabel("&Примечание", parent=self)
        self.__comment_edit = QTextEdit(parent=self)
        comment_lbl.setBuddy(self.__comment_edit)

        ok_btn = QPushButton("ОК", parent=self)
        cancel_btn = QPushButton("Отмена", parent=self)

        layout = QVBoxLayout()
        layout.addWidget(full_name_lbl)
        layout.addWidget(self.__full_name_edit)
        layout.addWidget(phone_lbl)
        layout.addWidget(self.__phone_edit)
        layout.addWidget(email_lbl)
        layout.addWidget(self.__email_edit)
        layout.addWidget(comment_lbl)
        layout.addWidget(self.__comment_edit)

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
        if self.full_name is None:
            return
        self.accept()

    @property
    def full_name(self):
        result = self.__full_name_edit.text().strip()
        return None if result == '' else result

    @full_name.setter
    def full_name(self, value):
        self.__full_name_edit.setText(value)

    @property
    def phone(self):
        result = self.__phone_edit.text().strip()
        return None if result == '' else result

    @phone.setter
    def phone(self, value):
        self.__phone_edit.setText(value)

    @property
    def email(self):
        result = self.__email_edit.text().strip()
        return None if result == '' else result

    @email.setter
    def email(self, value):
        self.__email_edit.setText(value)

    @property
    def comment(self):
        result = self.__comment_edit.toPlainText().strip()
        return None if result == '' else result

    @comment.setter
    def comment(self, value):
        self.__comment_edit.setText(value)
