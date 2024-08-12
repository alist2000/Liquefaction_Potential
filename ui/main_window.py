from PySide6.QtWidgets import QMainWindow, QTabWidget
from Liquefaction_Potential.ui.soil_layers_tab import SoilLayersTab
from Liquefaction_Potential.ui.spt_results_tab import SPTResultsTab, SPTResult
from Liquefaction_Potential.models.soil_profile import SoilProfile, SoilLayer
from Liquefaction_Potential.models.spt_data import SPTData
from Liquefaction_Potential.ui.results_display_tab import ResultsDisplayTab
import json
from PySide6.QtWidgets import (QMainWindow, QTabWidget, QToolBar, QFileDialog,
                               QStatusBar, QLabel, QHBoxLayout, QWidget)
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtCore import Qt, QUrl


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
        # Results Display Tab
        self.results_display_tab = ResultsDisplayTab()
        self.spt_results_tab = SPTResultsTab(soil_profile, spt_data, self.results_display_tab, self.tab_widget)
        self.results_display_tab.setEnabled(False)

        self.tab_widget.addTab(self.soil_layers_tab, "Soil Layers")
        self.tab_widget.addTab(self.spt_results_tab, "SPT Inputs")
        self.tab_widget.addTab(self.results_display_tab, "Results")
        self.create_status_bar()

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if file_name:
            data = {
                "soil_layers": [layer.__dict__ for layer in self.soil_profile.layers],
                "groundwater_level": self.soil_profile.groundwater_level,
                "max_acceleration": self.soil_profile.max_acceleration,
                "spt_results": [result.__dict__ for result in self.spt_data.results],
                "msf_option": "msf" if self.soil_layers_tab.MSF_ratio.isChecked() else "magnitude",
                "k_sigma_option": "k_sigma" if self.spt_results_tab.ksigma_ratio.isChecked() else "density",
                "msf_value": self.soil_layers_tab.MSF_input.value() if self.soil_layers_tab.MSF_ratio.isChecked() else self.soil_layers_tab.magnitude_input.value()
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

            # Load SPT results
            for spt_data in data["spt_results"]:
                self.spt_data.add_result(SPTResult(**spt_data))

            # Update UI
            self.soil_layers_tab.update_soil_table()
            self.soil_layers_tab.groundwater_level_input.setValue(data["groundwater_level"])
            self.soil_layers_tab.max_acceleration_input.setValue(data["max_acceleration"])

            # Handle MSF or magnitude option
            if data["msf_option"] == "msf":
                self.soil_layers_tab.MSF_ratio.setChecked(True)
                self.soil_layers_tab.MSF_input.setValue(data["msf_value"])
                self.soil_profile.set_msf(data["msf_value"])
            else:
                self.soil_layers_tab.magnitude_ratio.setChecked(True)
                self.soil_layers_tab.magnitude_input.setValue(data["msf_value"])
                msf = (7.5 / data["msf_value"]) ** 3.3  # Calculate MSF from magnitude
                self.soil_profile.set_msf(msf)

            # Handle K Sigma or Relative density option
            if data["k_sigma_option"] == "k_sigma":
                self.spt_results_tab.ksigma_ratio.setChecked(True)
            else:
                self.spt_results_tab.Dr_ratio.setChecked(True)

            self.soil_layers_tab.update_msf_ratio()  # Make sure UI is updated based on selected option
            self.spt_results_tab.update_spt_table()
            self.results_display_tab.setEnabled(False)

            # You may need to update other UI elements as well

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Create a widget to hold the status bar content
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(10, 0, 10, 0)

        # Add your signature
        signature_label = QLabel("Created by Ali Safari")
        status_layout.addWidget(signature_label)

        # Add spacer
        status_layout.addStretch()

        # Add contact link
        contact_label = QLabel('<a href="mailto:ali.safari.t@ut.ac.ir">Contact</a>')
        contact_label.setOpenExternalLinks(True)
        status_layout.addWidget(contact_label)

        # Add GitHub link
        github_label = QLabel('<a href="https://github.com/alist2000/Liquefaction_Potential">GitHub</a>')
        github_label.setOpenExternalLinks(True)
        status_layout.addWidget(github_label)

        # Set the custom widget as the status bar
        status_bar.addPermanentWidget(status_widget, 1)
