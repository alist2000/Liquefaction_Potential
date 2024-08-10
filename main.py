import sys
import os
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    # Step 1: Find the current directory
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    # Step 2: Add the current directory to the system PATH
    sys.path.append(current_directory)
    sys.path.append(parent_directory)

    from ui.main_window import MainWindow
    from models.soil_profile import SoilProfile
    from models.spt_data import SPTData

    app = QApplication(sys.argv)

    soil_profile = SoilProfile()
    spt_data = SPTData()
    main_window = MainWindow(soil_profile, spt_data)
    main_window.show()

    sys.exit(app.exec())
