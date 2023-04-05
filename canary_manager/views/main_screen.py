from PyQt6.QtWidgets import QTabWidget, QWidget
from canary_manager.model import Spawn
from canary_manager.views.canary_screen import CanaryScreen
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from canary_manager.views.spawn_table import SpawnTable


class MainScreen(QWidget):
    session: Session

    def __init__(self, engine: Engine, parent=None):
        super().__init__(parent)
        self.session = Session(engine)

        # Window properties
        self.setWindowTitle("Gestionnaire d'élevage")
        self.setGeometry(0, 0, 800, 600)
        self.tabs = QTabWidget(parent=self)
        self.tabs.setGeometry(0, 0, 800, 600)

        # Canary tab
        self.tabs.addTab(CanaryScreen(self.session), "Canaris")

        # Spawns tab
        spawns = self.session.scalars(select(Spawn)).all()
        self.tabs.addTab(SpawnTable(spawns), "Nichées")
