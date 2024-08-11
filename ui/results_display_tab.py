from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen


class ResultsDisplayTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.nceer_tab = QWidget()
        self.japanese_tab = QWidget()
        self.tab_widget.addTab(self.nceer_tab, "NCEER Results")
        self.tab_widget.addTab(self.japanese_tab, "Japanese Results")

        self.setup_nceer_tab()
        self.setup_japanese_tab()

    def setup_nceer_tab(self):
        layout = QHBoxLayout(self.nceer_tab)
        self.nceer_table = QTableWidget()
        self.nceer_chart_view = QChartView()
        layout.addWidget(self.nceer_table)
        layout.addWidget(self.nceer_chart_view)

    def setup_japanese_tab(self):
        layout = QHBoxLayout(self.japanese_tab)
        self.japanese_table = QTableWidget()
        self.japanese_chart_view = QChartView()
        layout.addWidget(self.japanese_table)
        layout.addWidget(self.japanese_chart_view)

    def update_results(self, nceer_params, japanese_params):
        self.update_nceer_results(nceer_params)
        self.update_japanese_results(japanese_params)

    def update_nceer_results(self, params):
        self.nceer_table.setColumnCount(9)
        self.nceer_table.setHorizontalHeaderLabels([
            "Depth", "Total Stress", "Effective Stress", "CSR", "N1 60", "N1 60 cs", "CRR 7.5", "CRR", "Fl"
        ])
        self.nceer_table.setRowCount(len(params[0]))

        for row, (depth, total_stress, effective_stress, csr, n1_60, n1_60_cs, crr_7_5, crr, fl) in enumerate(
                zip(*params)):
            items = [
                QTableWidgetItem(f"{depth:.2f}"),
                QTableWidgetItem(f"{total_stress:.2f}"),
                QTableWidgetItem(f"{effective_stress:.2f}"),
                QTableWidgetItem(f"{csr:.3f}"),
                QTableWidgetItem(f"{n1_60:.2f}"),
                QTableWidgetItem(f"{n1_60_cs:.2f}"),
                QTableWidgetItem(f"{crr_7_5:.3f}"),
                QTableWidgetItem(f"{crr:.3f}"),
                QTableWidgetItem(f"{fl:.4f}")
            ]

            for item in items:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item uneditable

            for col, item in enumerate(items):
                self.nceer_table.setItem(row, col, item)

        self.update_chart(self.nceer_chart_view, params[0], params[8], "Fl vs Depth")

    def update_japanese_results(self, params):
        self.japanese_table.setColumnCount(9)
        self.japanese_table.setHorizontalHeaderLabels([
            "Depth", "Total Stress", "Effective Stress", "CSR", "N1", "Na", "Rl 7.5", "Rl", "Fl"
        ])
        self.japanese_table.setRowCount(len(params[0]))

        for row, (depth, total_stress, effective_stress, csr, n1_60, n1_60_cs, crr_7_5, rl, fl) in enumerate(
                zip(*params)):
            items = [
                QTableWidgetItem(f"{depth:.2f}"),
                QTableWidgetItem(f"{total_stress:.2f}"),
                QTableWidgetItem(f"{effective_stress:.2f}"),
                QTableWidgetItem(f"{csr:.2f}"),
                QTableWidgetItem(f"{n1_60:.2f}"),
                QTableWidgetItem(f"{n1_60_cs:.2f}"),
                QTableWidgetItem(f"{crr_7_5:.2f}"),
                QTableWidgetItem(f"{rl:.2f}"),
                QTableWidgetItem(f"{fl:.2f}")
            ]

            for item in items:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item uneditable

            for col, item in enumerate(items):
                self.japanese_table.setItem(row, col, item)

        self.update_chart(self.japanese_chart_view, params[0], params[8], "Fl vs Depth")

    def update_chart(self, chart_view, depths, fls, title):
        line_series = QLineSeries()
        scatter_series = QScatterSeries()
        scatter_series2 = QScatterSeries()

        for depth, fl in zip(depths, fls):
            if fl < 1:
                scatter_series.append(fl, -depth)
            else:
                scatter_series2.append(fl, -depth)

            line_series.append(fl, -depth)  # Negative depth to show increasing depth downwards

        chart = QChart()
        chart.addSeries(line_series)
        chart.addSeries(scatter_series)
        chart.addSeries(scatter_series2)
        chart.setTitle(title)

        # Customize appearance
        line_color = QColor(Qt.black)
        scatter_color = QColor(Qt.red)
        scatter_color2 = QColor(Qt.green)

        line_series.setColor(line_color)
        line_series.setPen(QPen(line_color, 2))

        scatter_series.setColor(scatter_color)
        scatter_series.setMarkerSize(10)
        scatter_series.setBorderColor(scatter_color)
        scatter_series.setBrush(Qt.red)  # This makes the points "clear" (white fill)

        scatter_series2.setColor(scatter_color2)
        scatter_series2.setMarkerSize(10)
        scatter_series2.setBorderColor(scatter_color2)
        scatter_series2.setBrush(Qt.green)  # This makes the points "clear" (white fill)

        axis_x = QValueAxis()
        axis_x.setTitleText("Fl")
        chart.addAxis(axis_x, Qt.AlignBottom)
        line_series.attachAxis(axis_x)
        scatter_series.attachAxis(axis_x)
        scatter_series2.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Depth (m)")
        chart.addAxis(axis_y, Qt.AlignLeft)
        line_series.attachAxis(axis_y)
        scatter_series.attachAxis(axis_y)
        scatter_series2.attachAxis(axis_y)
        # Adjust the range to show all points
        min_fl = min(fls)
        max_fl = max(fls)
        min_depth = min(depths)
        max_depth = max(depths)

        axis_x.setRange(min_fl * 0.9, max_fl * 1.1)
        axis_y.setRange(-max_depth * 1.1, -min_depth * 0.9)

        chart_view.setChart(chart)
