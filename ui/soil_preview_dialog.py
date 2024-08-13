from PySide6.QtWidgets import QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtCore import Qt


class SoilPreviewDialog(QDialog):
    def __init__(self, soil_profile):
        super().__init__()
        self.soil_profile = soil_profile
        self.setWindowTitle("Soil Preview")
        self.setGeometry(100, 100, 400, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        layout.addWidget(self.view)
        self.setLayout(layout)

    def update_preview(self):
        self.scene.clear()
        total_depth = sum(layer.thickness for layer in self.soil_profile.layers)
        scale_factor = 500 / total_depth if total_depth > 0 else 1

        base_color = QColor("#ECB176")

        y = 0
        for i, layer in enumerate(self.soil_profile.layers):
            height = layer.thickness * scale_factor

            # Calculate darker color for deeper layers
            darkness_factor = 1 - (i * 0.1)  # Decrease by 10% for each layer
            layer_color = QColor(
                int(base_color.red() * darkness_factor),
                int(base_color.green() * darkness_factor),
                int(base_color.blue() * darkness_factor)
            )

            rect = self.scene.addRect(0, y, 350, height)
            rect.setBrush(QBrush(layer_color))
            rect.setPen(QPen(Qt.black))

            # Add layer information
            info_text = f"{layer.name} ({layer.thickness}m)\nγ: {layer.gamma} kN/m³\nFC: {layer.fine_content}%"
            text = self.scene.addText(info_text)
            text.setPos(10, y + 5)

            y += height

        # Add groundwater level (default to surface if not set)
        gw_level = self.soil_profile.groundwater_level if self.soil_profile.groundwater_level is not None else 0
        gw_y = gw_level * scale_factor
        gw_line = self.scene.addLine(0, gw_y, 350, gw_y, QPen(Qt.blue, 2))
        gw_text = self.scene.addText("Groundwater Level")
        gw_text.setPos(200, gw_y - 20)
        gw_text.setDefaultTextColor(Qt.blue)

        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.view.scale(0.95, 0.95)  # Slight zoom out to show everything
