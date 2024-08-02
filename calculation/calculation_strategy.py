# calculation_strategy.py
from abc import ABC, abstractmethod


class CalculationStrategy(ABC):
    def __init__(self):
        self.soil_profile = None
        self.spt_data = None

    @abstractmethod
    def calculate_fl(self, soil_profile, spt_data):
        pass

    @abstractmethod
    def calculate_alpha_beta(self, fine_content):
        pass

    def set_value(self, soil_profile, spt_data):
        self.soil_profile = soil_profile
        self.spt_data = spt_data
