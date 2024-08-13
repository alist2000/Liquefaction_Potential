from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout, QDoubleSpinBox, QRadioButton, QLabel)
from Liquefaction_Potential.models.soil_profile import SoilProfile, SoilLayer
from Liquefaction_Potential.ui.soil_preview_dialog import SoilPreviewDialog


class SoilLayersTab(QWidget):
    def __init__(self, soil_profile: SoilProfile):
        super().__init__()
        self.soil_profile = soil_profile
        self.setup_ui()
        self.preview_button = None
        self.preview_dialog = None

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.layer_name_input = QLineEdit()
        self.gamma_input = QLineEdit()
        self.thickness_input = QLineEdit()
        self.fine_content_input = QLineEdit()

        form_layout.addRow("Layer Name:", self.layer_name_input)
        form_layout.addRow("Gamma (kN/m³):", self.gamma_input)
        form_layout.addRow("Thickness (m):", self.thickness_input)
        form_layout.addRow("Fine Content (%):", self.fine_content_input)

        button_layout = QHBoxLayout()
        self.add_layer_button = QPushButton("Add Soil Layer")
        self.add_layer_button.clicked.connect(self.add_soil_layer)
        self.copy_layer_button = QPushButton("Copy Selected Layer")
        self.copy_layer_button.clicked.connect(self.copy_selected_layer)
        self.delete_layer_button = QPushButton("Delete Selected Layer")
        self.delete_layer_button.clicked.connect(self.delete_selected_layer)

        button_layout.addWidget(self.add_layer_button)
        button_layout.addWidget(self.copy_layer_button)
        button_layout.addWidget(self.delete_layer_button)

        form_layout.addRow(button_layout)

        self.groundwater_level_input = QDoubleSpinBox()
        self.max_acceleration_input = QDoubleSpinBox()
        self.groundwater_level_input.setDecimals(1)
        self.max_acceleration_input.setDecimals(3)
        self.max_acceleration_input.setRange(0, 10)
        form_layout.addRow("Groundwater Level (m):", self.groundwater_level_input)
        form_layout.addRow("Max Acceleration (g):", self.max_acceleration_input)

        self.magnitude_input = QDoubleSpinBox()
        self.magnitude_input.setDecimals(1)
        self.magnitude_input.setRange(0, 10)
        self.magnitude_ratio = QRadioButton()
        self.magnitude_ratio.setChecked(True)
        self.MSF_input = QDoubleSpinBox()
        self.MSF_input.setEnabled(False)
        self.MSF_input.setDecimals(3)
        self.MSF_ratio = QRadioButton()
        self.hlayout = QHBoxLayout()
        self.MSF_ratio.toggled.connect(self.update_msf_ratio)
        self.magnitude_ratio.toggled.connect(self.update_msf_ratio)
        self.MSF_input.valueChanged.connect(self.update_msf)
        self.magnitude_input.valueChanged.connect(self.update_msf)
        for i in [self.magnitude_ratio, QLabel("Earthquake Magnitude:"), self.magnitude_input, self.MSF_ratio,
                  QLabel("MSF:"),
                  self.MSF_input]:
            self.hlayout.addWidget(i)
        form_layout.addRow(self.hlayout)

        layout.addLayout(form_layout)

        self.soil_table = QTableWidget()
        self.soil_table.setColumnCount(4)
        self.soil_table.setHorizontalHeaderLabels(["Layer Name", "Gamma (kN/m³)", "Thickness (m)",
                                                   "Fine Content (%)"])
        self.soil_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.soil_table.itemChanged.connect(self.update_soil_layer)
        self.groundwater_level_input.valueChanged.connect(self.ground_water_or_acceleration)
        self.max_acceleration_input.valueChanged.connect(self.ground_water_or_acceleration)
        layout.addWidget(self.soil_table)

        self.setLayout(layout)
        # In the setup_ui method of SoilLayersTab class
        self.preview_button = QPushButton("Show Soil Preview")
        self.preview_button.clicked.connect(self.show_soil_preview)
        layout.addWidget(self.preview_button)

    def show_soil_preview(self):
        if not self.preview_dialog:
            self.preview_dialog = SoilPreviewDialog(self.soil_profile)
        self.preview_dialog.update_preview()
        self.preview_dialog.show()

    def add_soil_layer(self):
        try:
            layer_name = self.layer_name_input.text()
            gamma = float(self.gamma_input.text())
            thickness = float(self.thickness_input.text())
            fine_content = float(self.fine_content_input.text())

            layer = SoilLayer(layer_name, gamma, thickness, fine_content)
            self.soil_profile.add_layer(layer)

            self.update_soil_table()

            self.layer_name_input.clear()
            self.gamma_input.clear()
            self.thickness_input.clear()
            self.fine_content_input.clear()
        except ValueError:
            # Handle input errors
            pass
        if self.preview_dialog:
            self.preview_dialog.update_preview()

    def update_soil_table(self):
        self.soil_table.setColumnCount(6)  # Remove the Actions column
        self.soil_table.setHorizontalHeaderLabels(["Layer Name", "Gamma (kN/m³)", "Thickness (m)",
                                                   "Fine Content (%)"])
        self.soil_table.setRowCount(len(self.soil_profile.layers))
        for i, layer in enumerate(self.soil_profile.layers):
            self.soil_table.setItem(i, 0, QTableWidgetItem(layer.name))
            self.soil_table.setItem(i, 1, QTableWidgetItem(str(layer.gamma)))
            self.soil_table.setItem(i, 2, QTableWidgetItem(str(layer.thickness)))
            self.soil_table.setItem(i, 3, QTableWidgetItem(str(layer.fine_content)))
        if self.preview_dialog:
            self.preview_dialog.update_preview()

    def update_soil_layer(self, item):
        row = item.row()
        column = item.column()
        new_value = item.text()
        try:
            if column == 0:
                self.soil_profile.layers[row].name = new_value
            elif column == 1:
                self.soil_profile.layers[row].gamma = float(new_value)
            elif column == 2:
                self.soil_profile.layers[row].thickness = float(new_value)
            elif column == 3:
                self.soil_profile.layers[row].fine_content = float(new_value)
        except ValueError:
            # If the input is invalid, revert to the original value
            self.update_soil_table()
        if self.preview_dialog:
            self.preview_dialog.update_preview()

    def copy_selected_layer(self):
        selected_rows = self.soil_table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            self.soil_profile.copy_layer(row)
            self.update_soil_table()
        if self.preview_dialog:
            self.preview_dialog.update_preview()

    def delete_selected_layer(self):
        selected_rows = self.soil_table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            self.soil_profile.delete_layer(row)
            self.update_soil_table()
        if self.preview_dialog:
            self.preview_dialog.update_preview()

    def ground_water_or_acceleration(self):
        ground_water = self.groundwater_level_input.value()
        max_acceleration = self.max_acceleration_input.value()
        self.soil_profile.set_parameters(ground_water, max_acceleration)
        if self.preview_dialog:
            self.preview_dialog.update_preview()

    def update_msf_ratio(self):
        if self.MSF_ratio.isChecked():
            self.MSF_input.setEnabled(True)
            self.magnitude_input.setEnabled(False)
            self.magnitude_ratio.setChecked(False)
        else:
            self.magnitude_input.setEnabled(True)
            self.MSF_input.setEnabled(False)
            self.MSF_ratio.setChecked(False)

    def update_msf(self):
        if self.MSF_ratio.isChecked():
            msf = self.MSF_input.value()
        else:
            magnitude = self.magnitude_input.value()
            msf = (7.5 / magnitude) ** 3.3

        self.soil_profile.set_msf(msf)
