from Liquefaction_Potential.calculation.calculation_strategy import CalculationStrategy
from Liquefaction_Potential.models.spt_data import SPTData
from math import exp


class NCEERCalculation(CalculationStrategy):
    def calculate_fl(self, soil_profile, spt_data):
        self.set_value(soil_profile, spt_data)
        max_acceleration = self.soil_profile.max_acceleration
        fine_content = []
        depth = 0
        for layer in soil_profile.layers:
            fine_content_dict = {}
            fine_content_dict["depth"] = layer.thickness + depth
            fine_content_dict["fine_content"] = layer.fine_content
            fine_content.append(fine_content_dict)
            depth += layer.thickness
        print(fine_content)
        total_stress = []
        effective_stress = []
        csr_values = []
        n_edited_values = []
        n_edited_values_cs = []
        CRR_7_5 = []

        fine_content_index = 0
        fine_content_layer = fine_content[0]["fine_content"]
        for result in self.spt_data.results:
            depth = result.depth
            fine_content_not_find = True
            while fine_content_not_find:
                if depth <= fine_content[fine_content_index]["depth"]:
                    fine_content_not_find = False
                    fine_content_layer = fine_content[fine_content_index]["fine_content"]
                else:
                    if depth > fine_content[fine_content_index]["depth"] and fine_content_index == len(
                            fine_content) - 1:
                        fine_content_layer = fine_content[fine_content_index]["fine_content"]
                        fine_content_not_find = False
                    else:
                        fine_content_index += 1

            alpha, beta = self.calculate_alpha_beta(fine_content_layer)

            n_value = result.n_value
            hammer_energy = result.hammer_energy / 60
            cb, cs, cr = result.cb, result.cs, result.cr

            total_stress_depth = self.soil_profile.calculate_total_stress(depth)
            effective_stress_depth = self.soil_profile.calculate_effective_stress(depth, total_stress_depth)

            cn = min((100 / min(effective_stress_depth, 200)) ** 0.5, 1.7)
            n_edited = n_value * cb * cn * cs * cr * hammer_energy

            n_edited_cs = n_edited * beta + alpha

            total_stress.append(total_stress_depth)
            effective_stress.append(effective_stress_depth)
            rd = SPTData.calculate_rd(depth)

            csr = 0.65 * max_acceleration * (total_stress_depth / effective_stress_depth) * rd
            csr_values.append(csr)
            n_edited_values.append(n_edited)
            n_edited_values_cs.append(n_edited_cs)
            CRR = (1 / (34 - n_edited_cs)) + (n_edited_cs / 135) + (50 / ((10 * n_edited_cs + 45) ** 2)) - (1 / 200)
            CRR_7_5.append(CRR)
        return total_stress, effective_stress, csr_values, n_edited_values, n_edited_values_cs, CRR_7_5

    def calculate_alpha_beta(self, fine_content):
        if fine_content <= 5:
            alpha, beta = 0, 1
        elif 5 < fine_content <= 35:
            alpha = exp(1.76 - (190 / (fine_content ** 2)))
            beta = 0.99 + ((fine_content ** 1.5) / 1000)
        else:
            alpha, beta = 5, 1.2
        return alpha, beta
