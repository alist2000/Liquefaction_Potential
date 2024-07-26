from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
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

        layout.addLayout(form_layout)

        self.soil_table = QTableWidget()
        self.soil_table.setColumnCount(3)
        self.soil_table.setHorizontalHeaderLabels(["Layer Name", "Gamma (kN/m³)", "Thickness (m)"])
        self.soil_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.soil_table.itemChanged.connect(self.update_soil_layer)
        layout.addWidget(self.soil_table)

        self.setLayout(layout)

    def add_soil_layer(self):
        try:
            layer_name = self.layer_name_input.text()
            gamma = float(self.gamma_input.text())
            thickness = float(self.thickness_input.text())

            layer = SoilLayer(layer_name, gamma, thickness)
            self.soil_profile.add_layer(layer)

            self.update_soil_table()

            self.layer_name_input.clear()
            self.gamma_input.clear()
            self.thickness_input.clear()
        except ValueError:
            # Handle input errors
            pass

    def update_soil_table(self):
        self.soil_table.setRowCount(len(self.soil_profile.layers))
        for i, layer in enumerate(self.soil_profile.layers):
            self.soil_table.setItem(i, 0, QTableWidgetItem(layer.name))
            self.soil_table.setItem(i, 1, QTableWidgetItem(str(layer.gamma)))
            self.soil_table.setItem(i, 2, QTableWidgetItem(str(layer.thickness)))

    def update_soil_layer(self, item):
        row = item.row()
        column = item.column()
        new_value = item.text()

        if column == 0:  # Layer Name
            self.soil_profile.layers[row].name = new_value
        elif column == 1:  # Gamma
            try:
                self.soil_profile.layers[row].gamma = float(new_value)
            except ValueError:
                # Handle invalid input
                self.update_soil_table()
        elif column == 2:  # Thickness
            try:
                self.soil_profile.layers[row].thickness = float(new_value)
            except ValueError:
                # Handle invalid input
                self.update_soil_table()
