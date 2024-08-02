from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout,
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QDoubleSpinBox,
                               QRadioButton, QHBoxLayout)
from Liquefaction_Potential.models.soil_profile import SoilProfile
from Liquefaction_Potential.models.spt_data import SPTData, SPTResult
from Liquefaction_Potential.calculation.calculation_factory import CalculationFactory


class SPTResultsTab(QWidget):
    def __init__(self, soil_profile: SoilProfile, spt_data: SPTData):
        super().__init__()
        self.soil_profile = soil_profile
        self.spt_data = spt_data
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.spt_depth_input = QDoubleSpinBox()
        self.spt_n_value_input = QDoubleSpinBox()
        self.hammer_energy_input = QDoubleSpinBox()
        self.cb_input = QDoubleSpinBox()
        self.cb_input.setValue(1)
        self.cs_input = QDoubleSpinBox()
        self.cs_input.setValue(1)
        self.cr_input = QDoubleSpinBox()
        self.cr_input.setValue(1)
        self.kalpha = QDoubleSpinBox()
        self.kalpha.setValue(1)

        self.ksigma_ratio = QRadioButton()
        self.ksigma_ratio.setChecked(True)
        self.ksigma = QDoubleSpinBox()
        self.ksigma.setValue(1)
        self.Dr_ratio = QRadioButton()
        self.Dr = QDoubleSpinBox()
        self.Dr.setEnabled(False)
        self.Dr_ratio.toggled.connect(self.k_sigma_toggled)
        self.ksigma_ratio.toggled.connect(self.k_sigma_toggled)

        self.hLayout = QHBoxLayout()
        for i in [self.ksigma_ratio, QLabel("Kσ: "), self.ksigma, self.Dr_ratio, QLabel("Dr (Relative Density %): "),
                  self.Dr]:
            self.hLayout.addWidget(i)

        form_layout.addRow("Depth (m):", self.spt_depth_input)
        form_layout.addRow("SPT N-Value:", self.spt_n_value_input)
        form_layout.addRow("Hammer Energy (%):", self.hammer_energy_input)
        form_layout.addRow("Cb:", self.cb_input)
        form_layout.addRow("Cs:", self.cs_input)
        form_layout.addRow("Cr:", self.cr_input)
        form_layout.addRow("Kα:", self.kalpha)
        form_layout.addRow(self.hLayout)

        self.add_spt_result_button = QPushButton("Add SPT Result")
        self.add_spt_result_button.clicked.connect(self.add_spt_result)
        form_layout.addRow(self.add_spt_result_button)

        layout.addLayout(form_layout)

        self.spt_table = QTableWidget()
        self.spt_table.setColumnCount(8)
        self.spt_table.setHorizontalHeaderLabels([
            "Depth (m)",
            "SPT N-Value",
            "Hammer Energy (%)",
            "Cb",
            "Cs",
            "Cr",
            "Kα",
            "Kσ"
        ])
        self.spt_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.spt_table.itemChanged.connect(self.update_spt_result)
        layout.addWidget(self.spt_table)

        self.calculate_button = QPushButton("Calculate Stresses and CSR")
        self.calculate_button.clicked.connect(self.calculate_stresses_and_csr)
        layout.addWidget(self.calculate_button)

        self.results_label = QLabel()
        layout.addWidget(self.results_label)

        self.setLayout(layout)

    def add_spt_result(self):
        try:
            depth = float(self.spt_depth_input.value())
            n_value = int(self.spt_n_value_input.value())
            hammer_energy = float(self.hammer_energy_input.value())
            cb = float(self.cb_input.value())
            cs = float(self.cs_input.value())
            cr = float(self.cr_input.value())
            k_alpha = float(self.ksigma.value())
            if self.ksigma_ratio.isChecked():
                k_sigma_or_dr = float(self.ksigma.value())
            else:
                k_sigma_or_dr = float(self.Dr.value())

            result = SPTResult(depth, n_value, hammer_energy, cb, cs, cr, k_alpha, k_sigma_or_dr)
            self.spt_data.add_result(result)

            self.update_spt_table()

            self.spt_depth_input.clear()
            self.spt_n_value_input.clear()
            self.hammer_energy_input.clear()
            self.cb_input.setValue(1)
            self.cs_input.setValue(1)
            self.cr_input.setValue(1)
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
            self.spt_table.setItem(i, 6, QTableWidgetItem(str(result.k_alpha)))
            self.spt_table.setItem(i, 7, QTableWidgetItem(str(result.k_sigma_or_dr)))

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
            elif column == 6:
                self.spt_data.results[row].k_alpha = float(new_value)
            elif column == 7:
                self.spt_data.results[row].k_sigma_or_dr = float(new_value)
        except ValueError:
            # If the input is invalid, revert to the original value
            self.update_spt_table()

    def k_sigma_toggled(self):
        if self.ksigma_ratio.isChecked():
            self.ksigma.setEnabled(True)
            self.Dr_ratio.setChecked(False)
            self.Dr.setEnabled(False)
            self.spt_table.setHorizontalHeaderLabels([
                "Depth (m)",
                "SPT N-Value",
                "Hammer Energy (%)",
                "Cb",
                "Cs",
                "Cr",
                "Kα",
                "Kσ"
            ])
        else:
            self.Dr.setEnabled(True)
            self.ksigma_ratio.setChecked(False)
            self.ksigma.setEnabled(False)
            self.spt_table.setHorizontalHeaderLabels([
                "Depth (m)",
                "SPT N-Value",
                "Hammer Energy (%)",
                "Cb",
                "Cs",
                "Cr",
                "Kα",
                "Dr"
            ])

    def calculate_stresses_and_csr(self):
        if not self.soil_profile.max_acceleration:
            self.results_label.setText("Please enter valid max acceleration.")
            return
        if not self.soil_profile.msf:
            self.results_label.setText("Please enter valid MSF or Earthquake Magnitude.")
            return

        nceer_calculation = CalculationFactory.get_calculation("NCEER")
        japanese_calculation = CalculationFactory.get_calculation("Japanese")

        nceer_parameters = nceer_calculation.calculate_fl(self.soil_profile, self.spt_data)

        japanese_parameters = japanese_calculation.calculate_fl(self.soil_profile, self.spt_data)
        self.results_label.setText(
            f"Total Stress: {nceer_parameters[0]}\nEffective Stress: {nceer_parameters[1]}\nCSR: {nceer_parameters[2]}\nN1 60: {nceer_parameters[3]}\nN1 60 cs : {nceer_parameters[4]}")

        self.display_results(nceer_parameters, japanese_parameters)

    def display_results(self, nceer_params, japanese_params):
        # Implement result display logic
        pass
