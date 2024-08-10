from dataclasses import dataclass
from typing import List
from PySide6.QtCore import QObject, Signal
import copy

@dataclass
class SPTResult:
    depth: float
    n_value: int
    hammer_energy: float
    cb: float
    cs: float
    cr: float
    k_alpha: float
    k_sigma_or_dr: float


class SPTData(QObject):
    results_changed = Signal()

    def __init__(self):
        super().__init__()
        self.results: List[SPTResult] = []

    def add_result(self, result: SPTResult):
        self.results.append(result)
        self.results_changed.emit()

    def copy_result(self, index: int):
        if 0 <= index < len(self.results):
            new_result = copy.deepcopy(self.results[index])
            new_result.depth += 1  # Slightly modify the depth to differentiate
            self.results.insert(index + 1, new_result)
            self.results_changed.emit()

    def delete_result(self, index: int):
        if 0 <= index < len(self.results):
            del self.results[index]
            self.results_changed.emit()

    @staticmethod
    def calculate_rd(depth: float) -> float:
        if depth <= 9.15:
            rd = 1 - 0.00765 * depth
        else:
            rd = 1.174 - 0.0267 * depth
        return rd

    @staticmethod
    def calculate_rd_japanese(depth: float) -> float:
        rd = 1 - 0.015 * depth
        return rd
