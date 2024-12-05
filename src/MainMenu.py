from PyQt5.QtWidgets import QWidget, QMenuBar


class MainMenu(QMenuBar):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        teacher_menu = self.addMenu('Учитель')
        self.__teacher_add = teacher_menu.addAction('Добавить')
        self.__teacher_update = teacher_menu.addAction('Редактировать')
        self.__teacher_delete = teacher_menu.addAction('Удалить')

        test_menu = self.addMenu('Задача')
        self.__test_add = test_menu.addAction('Добавить')
        self.__test_delete = test_menu.addAction('Удалить')

        variant_menu = self.addMenu('Вариант')
        self.__variant_add = variant_menu.addAction('Добавить')
        self.__variant_delete = variant_menu.addAction('Удалить')

        help_menu = self.addMenu('Справка')
        self.__about = help_menu.addAction('О программе...')
        self.__about_qt = help_menu.addAction('О библиотеке Qt...')

    @property
    def about(self):
        return self.__about

    @property
    def about_qt(self):
        return self.__about_qt

    @property
    def teacher_add(self):
        return self.__teacher_add

    @property
    def teacher_update(self):
        return self.__teacher_update

    @property
    def teacher_delete(self):
        return self.__teacher_delete

    @property
    def test_add(self):
        return self.__test_add

    @property
    def test_delete(self):
        return self.__test_delete

    @property
    def variant_add(self):
        return self.__variant_add

    @property
    def variant_delete(self):
        return self.__variant_delete
