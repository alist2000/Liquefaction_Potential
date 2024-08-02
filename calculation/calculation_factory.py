# calculation_factory.py
from Liquefaction_Potential.calculation.NCEER import NCEERCalculation
from Liquefaction_Potential.calculation.Japanese import JapaneseCalculation


class CalculationFactory:
    @staticmethod
    def get_calculation(method):
        if method == "NCEER":
            return NCEERCalculation()
        elif method == "Japanese":
            return JapaneseCalculation()
        else:
            raise ValueError("Invalid calculation method")
