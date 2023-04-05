from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from typing import List

from canary_manager.model import Spawn


class SpawnTable(QTableWidget):
    spawns = "List[Spawn]"

    def __init__(self, spawns: List[Spawn], *args):
        QTableWidget.__init__(self, *args)
        self.spawns = spawns
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        self.setColumnCount(4)
        self.setRowCount(len(self.spawns))

        for idx, spawn in enumerate(self.spawns):
            self.setItem(idx, 0, QTableWidgetItem(str(spawn.spawned_at)))
            self.setItem(idx, 1, QTableWidgetItem(str(spawn.father.ring)))
            self.setItem(idx, 2, QTableWidgetItem(str(spawn.mother.ring)))
            self.setItem(idx, 3, QTableWidgetItem(str(len(spawn.eggs))))
        self.setHorizontalHeaderLabels([
            "Date",
            "Père",
            "Mère",
            "Nombre d'oeufs"
        ])
