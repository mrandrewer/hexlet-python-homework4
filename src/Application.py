import sys
from typing import List
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase
import settings as settings


class Application(QApplication):

    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(settings.db_params['host'])
        db.setPort(settings.db_params['port'])
        db.setDatabaseName(settings.db_params['dbname'])
        db.setUserName(settings.db_params['user'])
        db.setPassword(settings.db_params['password'])
        ok = db.open()
        if ok:
            print('Connection successful', file=sys.stderr)
        else:
            print('Failed to connect to db', file=sys.stderr)
