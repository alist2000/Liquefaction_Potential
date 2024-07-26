import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from models.soil_profile import SoilProfile
from models.spt_data import SPTData

if __name__ == "__main__":
    app = QApplication(sys.argv)

    soil_profile = SoilProfile()
    spt_data = SPTData()
    main_window = MainWindow(soil_profile, spt_data)
    main_window.show()

    sys.exit(app.exec())
