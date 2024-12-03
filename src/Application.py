from typing import List
from PyQt5.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
