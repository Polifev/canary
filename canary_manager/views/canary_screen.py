from PyQt6.QtWidgets import QWidget, QFormLayout, QPushButton, QInputDialog,\
    QLabel, QHBoxLayout
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from canary_manager.model import Canary, Spawn
from canary_manager.views.spawn_table import SpawnTable


NO_SELECTION_DEFAULT = "Pas de canari sélectionné"


class CanaryScreen(QWidget):
    session: Session
    current_canary: "Canary|None"

    def __init__(self, session: Session, parent=None):
        super().__init__(parent)

        self.session = session
        self.current_canary = None

        self.btn_load = QPushButton("Chercher un canari")
        self.btn_load.move(20, 20)
        self.btn_load.clicked.connect(self.showDialog)

        self.lbl_canary_ring = QLabel(NO_SELECTION_DEFAULT)
        self.lbl_canary_origin = QLabel(NO_SELECTION_DEFAULT)
        self.lbl_canary_sex = QLabel(NO_SELECTION_DEFAULT)
        self.lbl_canary_color = QLabel(NO_SELECTION_DEFAULT)

        self.btn_load_father = QPushButton(NO_SELECTION_DEFAULT)
        self.btn_load_father.clicked.connect(self.load_father)
        self.btn_load_father.setEnabled(False)

        self.btn_load_mother = QPushButton(NO_SELECTION_DEFAULT)
        self.btn_load_mother.clicked.connect(self.load_mother)
        self.btn_load_mother.setEnabled(False)

        self.tbl_children = SpawnTable([])

        lay_parents = QHBoxLayout()
        lay_parents.addWidget(self.btn_load_father)
        lay_parents.addWidget(self.btn_load_mother)

        flo = QFormLayout()
        flo.addRow("Chercher un canari", self.btn_load)
        flo.addRow("Numéro de bague", self.lbl_canary_ring)
        flo.addRow("Origine", self.lbl_canary_origin)
        flo.addRow("Sexe", self.lbl_canary_sex)
        flo.addRow("Couleur", self.lbl_canary_color)
        flo.addRow("Parents", lay_parents)
        flo.addRow("Enfants", self.tbl_children)

        self.setLayout(flo)
        self.setWindowTitle("Gestionnaire d'élevage")

    def set_current_canary(self, canary: Canary):
        self.current_canary = canary
        self.lbl_canary_ring.setText(str(canary.ring))
        if (canary.egg is None):
            self.lbl_canary_origin.setText("Acheté")
        else:
            year = canary.egg.spawn.spawned_at.year
            self.lbl_canary_origin.setText(f"Élevé (né en {year})")
        self.lbl_canary_sex.setText(str(canary.sex))
        self.lbl_canary_color.setText(str(canary.color))

        self.btn_load_father.setEnabled(False)
        self.btn_load_father.setText("Père inconnu")
        self.btn_load_mother.setEnabled(False)
        self.btn_load_mother.setText("Mère inconnue")
        if canary.egg is not None:
            if canary.egg.spawn.father is not None:
                self.btn_load_father.setEnabled(True)
                self.btn_load_father.setText(
                    f"Voir son père (bague: {canary.egg.spawn.father.ring})")
            if canary.egg.spawn.mother is not None:
                self.btn_load_mother.setEnabled(True)
                self.btn_load_mother.setText(
                    f"Voir sa mère (bague: {canary.egg.spawn.mother.ring})")

        # get children
        stmt = select(Spawn).where(or_(Spawn.father_id == canary.id, Spawn.mother_id == canary.id))
        spawns = self.session.scalars(stmt).all()
        self.tbl_children.spawns = spawns
        self.tbl_children.setData()

    def load_father(self):
        self.set_current_canary(self.current_canary.egg.spawn.father)

    def load_mother(self):
        self.set_current_canary(self.current_canary.egg.spawn.mother)

    def showDialog(self):
        user_input, ok = QInputDialog.getText(
            self,
            "Recherche de canari",
            "Numéro de bague:")

        if ok:
            cleaned_input = str(user_input).strip()
            try:
                statement = select(Canary).where(Canary.ring == cleaned_input)
                canary = self.session.scalars(statement).first()
                self.set_current_canary(canary)
            except Exception as err:
                print(err)
