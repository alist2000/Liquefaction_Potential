from dataclasses import dataclass
from typing import List
from PySide6.QtCore import QObject, Signal


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

    @staticmethod
    def calculate_rd(depth: float) -> float:
        if depth <= 9.15:
            rd = 1 - 0.00765 * depth
        else:
            rd = 1.174 - 0.0267 * depth
        return rd
