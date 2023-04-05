from typing import List
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class ChildrenView(QTableWidget):
    # children: List[Canary]

    def __init__(self, children: List, *args):
        QTableWidget.__init__(self, *args)
        self.children = children
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        self.setColumnCount(5)
        self.setRowCount(len(self.children))
        for idx, child in enumerate(self.children):
            self.setItem(idx, 0, QTableWidgetItem(str(child.id)))
            self.setItem(idx, 1, QTableWidgetItem(child.color))
            self.setItem(idx, 2, QTableWidgetItem(child.sex))
            self.setItem(idx, 3, QTableWidgetItem(str(child.father_id)))
            self.setItem(idx, 4, QTableWidgetItem(str(child.mother_id)))
        self.setHorizontalHeaderLabels([
            "Bague",
            "Couleur",
            "Sexe",
            "Père",
            "Mère"])
