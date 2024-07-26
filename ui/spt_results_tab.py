from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel)
from PySide6.QtCore import Qt
from Liquefaction_Potential.models.soil_profile import SoilProfile
from Liquefaction_Potential.models.spt_data import SPTData, SPTResult


class SPTResultsTab(QWidget):
    def __init__(self, soil_profile: SoilProfile, spt_data: SPTData):
        super().__init__()
        self.soil_profile = soil_profile
        self.spt_data = spt_data
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.spt_depth_input = QLineEdit()
        self.spt_n_value_input = QLineEdit()
        self.hammer_energy_input = QLineEdit()
        self.cb_input = QLineEdit()
        self.cb_input.setText("1")
        self.cs_input = QLineEdit()
        self.cs_input.setText("1")
        self.cr_input = QLineEdit()
        self.cr_input.setText("1")

        form_layout.addRow("Depth (m):", self.spt_depth_input)
        form_layout.addRow("SPT N-Value:", self.spt_n_value_input)
        form_layout.addRow("Hammer Energy (%):", self.hammer_energy_input)
        form_layout.addRow("Cb:", self.cb_input)
        form_layout.addRow("Cs:", self.cs_input)
        form_layout.addRow("Cr:", self.cr_input)

        self.add_spt_result_button = QPushButton("Add SPT Result")
        self.add_spt_result_button.clicked.connect(self.add_spt_result)
        form_layout.addRow(self.add_spt_result_button)

        layout.addLayout(form_layout)

        self.spt_table = QTableWidget()
        self.spt_table.setColumnCount(6)
        self.spt_table.setHorizontalHeaderLabels(["Depth (m)", "SPT N-Value", "Hammer Energy (%)", "Cb", "Cs", "Cr"])
        self.spt_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.spt_table.itemChanged.connect(self.update_spt_result)
        layout.addWidget(self.spt_table)

        self.groundwater_level_input = QLineEdit()
        self.max_acceleration_input = QLineEdit()
        form_layout.addRow("Groundwater Level (m):", self.groundwater_level_input)
        form_layout.addRow("Max Acceleration (g):", self.max_acceleration_input)

        self.calculate_button = QPushButton("Calculate Stresses and CSR")
        self.calculate_button.clicked.connect(self.calculate_stresses_and_csr)
        layout.addWidget(self.calculate_button)

        self.results_label = QLabel()
        layout.addWidget(self.results_label)

        self.setLayout(layout)

    def add_spt_result(self):
        try:
            depth = float(self.spt_depth_input.text())
            n_value = int(self.spt_n_value_input.text())
            hammer_energy = float(self.hammer_energy_input.text())
            cb = float(self.cb_input.text())
            cs = float(self.cs_input.text())
            cr = float(self.cr_input.text())

            result = SPTResult(depth, n_value, hammer_energy, cb, cs, cr)
            self.spt_data.add_result(result)

            self.update_spt_table()

            self.spt_depth_input.clear()
            self.spt_n_value_input.clear()
            self.hammer_energy_input.clear()
            self.cb_input.setText("1")
            self.cs_input.setText("1")
            self.cr_input.setText("1")
        except ValueError:
            # Handle input errors
            pass

    def update_spt_table(self):
        self.spt_table.setRowCount(len(self.spt_data.results))
        for i, result in enumerate(self.spt_data.results):
            self.spt_table.setItem(i, 0, QTableWidgetItem(str(result.depth)))
            self.spt_table.setItem(i, 1, QTableWidgetItem(str(result.n_value)))
            self.spt_table.setItem(i, 2, QTableWidgetItem(str(result.hammer_energy)))
            self.spt_table.setItem(i, 3, QTableWidgetItem(str(result.cb)))
            self.spt_table.setItem(i, 4, QTableWidgetItem(str(result.cs)))
            self.spt_table.setItem(i, 5, QTableWidgetItem(str(result.cr)))

    def update_spt_result(self, item):
        row = item.row()
        column = item.column()
        new_value = item.text()

        try:
            if column == 0:
                self.spt_data.results[row].depth = float(new_value)
            elif column == 1:
                self.spt_data.results[row].n_value = int(new_value)
            elif column == 2:
                self.spt_data.results[row].hammer_energy = float(new_value)
            elif column == 3:
                self.spt_data.results[row].cb = float(new_value)
            elif column == 4:
                self.spt_data.results[row].cs = float(new_value)
            elif column == 5:
                self.spt_data.results[row].cr = float(new_value)
        except ValueError:
            # If the input is invalid, revert to the original value
            self.update_spt_table()

    def calculate_stresses_and_csr(self):
        if self.groundwater_level_input.text():
            try:
                groundwater_level = float(self.groundwater_level_input.text())
            except ValueError:
                self.results_label.setText("Please enter valid ground water level.")
                return
        else:
            groundwater_level = float('inf')
        try:
            max_acceleration = float(self.max_acceleration_input.text())
        except ValueError:
            self.results_label.setText("Please enter valid max acceleration.")
            return

        self.soil_profile.set_parameters(groundwater_level, max_acceleration)

        total_stress = []
        effective_stress = []
        csr_values = []
        n_edited_values = []

        for result in self.spt_data.results:
            depth = result.depth
            n_value = result.n_value
            hammer_energy = result.hammer_energy / 60
            cb, cs, cr = result.cb, result.cs, result.cr

            total_stress_depth = self.soil_profile.calculate_total_stress(depth)
            effective_stress_depth = self.soil_profile.calculate_effective_stress(depth, total_stress_depth)

            cn = min((100 / effective_stress_depth) ** 0.5, 1.7)
            n_edited = n_value * cb * cn * cs * cr * hammer_energy

            total_stress.append(total_stress_depth)
            effective_stress.append(effective_stress_depth)
            rd = SPTData.calculate_rd(depth)

            csr = 0.65 * max_acceleration * (total_stress_depth / effective_stress_depth) * rd
            csr_values.append(csr)
            n_edited_values.append(n_edited)

        self.results_label.setText(
            f"Total Stress: {total_stress}\nEffective Stress: {effective_stress}\nCSR: {csr_values}\nN1 60: {n_edited_values}")
