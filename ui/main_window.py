from PySide6.QtWidgets import QMainWindow, QTabWidget
from Liquefaction_Potential.ui.soil_layers_tab import SoilLayersTab
from Liquefaction_Potential.ui.spt_results_tab import SPTResultsTab, SPTResult
from Liquefaction_Potential.models.soil_profile import SoilProfile, SoilLayer
from Liquefaction_Potential.models.spt_data import SPTData

from PySide6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QFileDialog
from PySide6.QtGui import QAction
import json


class MainWindow(QMainWindow):
    def __init__(self, soil_profile: SoilProfile, spt_data: SPTData):
        super().__init__()

        self.soil_profile = soil_profile
        self.spt_data = spt_data

        self.setWindowTitle("Soil and Earthquake Properties")
        self.setGeometry(100, 100, 800, 600)

        # Create toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add Save action
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_data)
        toolbar.addAction(save_action)

        # Add Load action
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_data)
        toolbar.addAction(load_action)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.soil_layers_tab = SoilLayersTab(soil_profile)
        self.spt_results_tab = SPTResultsTab(soil_profile, spt_data)

        self.tab_widget.addTab(self.soil_layers_tab, "Soil Layers")
        self.tab_widget.addTab(self.spt_results_tab, "SPT Results")

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if file_name:
            data = {
                "soil_layers": [layer.__dict__ for layer in self.soil_profile.layers],
                "groundwater_level": self.soil_profile.groundwater_level,
                "max_acceleration": self.soil_profile.max_acceleration,
                "msf": self.soil_profile.msf,
                "spt_results": [result.__dict__ for result in self.spt_data.results]
            }
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as f:
                data = json.load(f)

            # Clear existing data
            self.soil_profile.layers.clear()
            self.spt_data.results.clear()

            # Load soil layers
            for layer_data in data["soil_layers"]:
                self.soil_profile.add_layer(SoilLayer(**layer_data))

            # Load soil profile parameters
            self.soil_profile.set_parameters(data["groundwater_level"], data["max_acceleration"])
            self.soil_profile.set_msf(data["msf"])

            # Load SPT results
            for spt_data in data["spt_results"]:
                self.spt_data.add_result(SPTResult(**spt_data))

            # Update UI
            self.soil_layers_tab.update_soil_table()
            self.soil_layers_tab.groundwater_level_input.setValue(data["groundwater_level"])
            self.soil_layers_tab.max_acceleration_input.setValue(data["max_acceleration"])
            self.spt_results_tab.update_spt_table()

            # You may need to update other UI elements as well
