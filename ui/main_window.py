from PySide6.QtWidgets import QMainWindow, QTabWidget
from Liquefaction_Potential.ui.soil_layers_tab import SoilLayersTab
from Liquefaction_Potential.ui.spt_results_tab import SPTResultsTab
from Liquefaction_Potential.models.soil_profile import SoilProfile
from Liquefaction_Potential.models.spt_data import SPTData


class MainWindow(QMainWindow):
    def __init__(self, soil_profile: SoilProfile, spt_data: SPTData):
        super().__init__()

        self.setWindowTitle("Soil and Earthquake Properties")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.soil_layers_tab = SoilLayersTab(soil_profile)
        self.spt_results_tab = SPTResultsTab(soil_profile, spt_data)

        self.tab_widget.addTab(self.soil_layers_tab, "Soil Layers")
        self.tab_widget.addTab(self.spt_results_tab, "SPT Results")
