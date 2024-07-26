from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from Liquefaction_Potential.models.soil_profile import SoilProfile, SoilLayer


class SoilLayersTab(QWidget):
    def __init__(self, soil_profile: SoilProfile):
        super().__init__()
        self.soil_profile = soil_profile
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.layer_name_input = QLineEdit()
        self.gamma_input = QLineEdit()
        self.thickness_input = QLineEdit()

        form_layout.addRow("Layer Name:", self.layer_name_input)
        form_layout.addRow("Gamma (kN/m³):", self.gamma_input)
        form_layout.addRow("Thickness (m):", self.thickness_input)

        self.add_layer_button = QPushButton("Add Soil Layer")
        self.add_layer_button.clicked.connect(self.add_soil_layer)
        form_layout.addRow(self.add_layer_button)

        self.groundwater_level_input = QLineEdit()
        self.max_acceleration_input = QLineEdit()

        form_layout.addRow("Groundwater Level (m):", self.groundwater_level_input)
        form_layout.addRow("Max Acceleration (g):", self.max_acceleration_input)

        self.set_parameters_button = QPushButton("Set Parameters")
        self.set_parameters_button.clicked.connect(self.set_parameters)
        form_layout.addRow(self.set_parameters_button)

        layout.addLayout(form_layout)

        self.soil_table = QTableWidget()
        self.soil_table.setColumnCount(3)
        self.soil_table.setHorizontalHeaderLabels(["Layer Name", "Gamma (kN/m³)", "Thickness (m)"])
        self.soil_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.soil_table)

        self.setLayout(layout)

        self.soil_profile.layers_changed.connect(self.update_soil_table)

    def add_soil_layer(self):
        try:
            layer_name = self.layer_name_input.text()
            gamma = float(self.gamma_input.text())
            thickness = float(self.thickness_input.text())

            layer = SoilLayer(layer_name, gamma, thickness)
            self.soil_profile.add_layer(layer)

            self.layer_name_input.clear()
            self.gamma_input.clear()
            self.thickness_input.clear()
        except ValueError:
            # Handle input errors
            pass

    def set_parameters(self):
        try:
            groundwater_level = float(self.groundwater_level_input.text())
            max_acceleration = float(self.max_acceleration_input.text())

            self.soil_profile.set_parameters(groundwater_level, max_acceleration)

            self.groundwater_level_input.clear()
            self.max_acceleration_input.clear()
        except ValueError:
            # Handle input errors
            pass

    def update_soil_table(self):
        self.soil_table.setRowCount(len(self.soil_profile.layers))
        for i, layer in enumerate(self.soil_profile.layers):
            self.soil_table.setItem(i, 0, QTableWidgetItem(layer.name))
            self.soil_table.setItem(i, 1, QTableWidgetItem(str(layer.gamma)))
            self.soil_table.setItem(i, 2, QTableWidgetItem(str(layer.thickness)))
