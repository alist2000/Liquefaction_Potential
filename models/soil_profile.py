from dataclasses import dataclass
from typing import List
from PySide6.QtCore import QObject, Signal


@dataclass
class SoilLayer:
    name: str
    gamma: float
    thickness: float
    fine_content: float
    ll: float = None  # Liquid Limit (optional)
    pi: float = None  # Plasticity Index (optional)


class SoilProfile(QObject):
    layers_changed = Signal()
    parameters_changed = Signal()

    def __init__(self):
        super().__init__()
        self.layers: List[SoilLayer] = []
        self.groundwater_level: float = 0  # Set to 0 by default
        self.max_acceleration: float = None
        self.msf: float = None

    def add_layer(self, layer: SoilLayer):
        self.layers.append(layer)
        self.layers_changed.emit()

    def delete_layer(self, index: int):
        if 0 <= index < len(self.layers):
            del self.layers[index]
            self.layers_changed.emit()

    def copy_layer(self, index: int):
        if 0 <= index < len(self.layers):
            new_layer = SoilLayer(**self.layers[index].__dict__)
            new_layer.name += " (copy)"
            self.layers.insert(index + 1, new_layer)
            self.layers_changed.emit()

    def set_parameters(self, groundwater_level: float, max_acceleration: float):
        self.groundwater_level = groundwater_level
        self.max_acceleration = max_acceleration
        self.parameters_changed.emit()

    def set_msf(self, msf: float):
        self.msf = msf
        self.parameters_changed.emit()

    def calculate_total_stress(self, depth: float) -> float:
        cumulative_depth = 0
        total_stress = 0
        for layer in self.layers:
            if cumulative_depth + layer.thickness >= depth:
                total_stress += layer.gamma * (depth - cumulative_depth)
                break
            total_stress += layer.gamma * layer.thickness
            cumulative_depth += layer.thickness
        return total_stress

    def calculate_effective_stress(self, depth: float, total_stress: float) -> float:
        if depth <= self.groundwater_level:
            return total_stress
        else:
            water_depth = depth - self.groundwater_level
            effective_stress = total_stress - (10 * water_depth)
            return effective_stress

    def get_gamma_at_depth(self, depth: float) -> float:
        cumulative_thickness = 0
        for layer in self.layers:
            cumulative_thickness += layer.thickness
            if depth <= cumulative_thickness:
                return layer.gamma
        return self.layers[-1].gamma if self.layers else 0
