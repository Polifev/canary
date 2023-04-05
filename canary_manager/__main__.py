import sys

from PyQt6.QtWidgets import QApplication
from canary_manager.model import Base
from canary_manager.views.main_screen import MainScreen
from sqlalchemy import create_engine


def main():
    engine = create_engine("sqlite:///canary_manager.db", echo=True)
    Base.metadata.create_all(engine)
    app = QApplication([])
    return_code = -1
    mainScreen = MainScreen(engine)
    mainScreen.show()
    return_code = app.exec()
    sys.exit(return_code)


if __name__ == "__main__":
    main()
