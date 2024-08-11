from Liquefaction_Potential.calculation.calculation_strategy import CalculationStrategy
from Liquefaction_Potential.models.spt_data import SPTData
from math import exp
import numpy as np
from scipy import interpolate


class JapaneseCalculation(CalculationStrategy):
    def calculate_fl(self, soil_profile, spt_data, k_sigma_status):
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
        CRR_main = []
        Fl = []
        depthList = []

        fine_content_index = 0
        fine_content_layer = fine_content[0]["fine_content"]
        for result in self.spt_data.results:
            depth = result.depth
            depthList.append(depth)
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
            # hammer_energy = result.hammer_energy / 60
            # cb, cs, cr = result.cb, result.cs, result.cr

            total_stress_depth = self.soil_profile.calculate_total_stress(depth)
            effective_stress_depth = self.soil_profile.calculate_effective_stress(depth, total_stress_depth)
            total_stress_depth = total_stress_depth / 100
            effective_stress_depth = effective_stress_depth / 100
            # cn = min((100 / min(effective_stress_depth, 200)) ** 0.5, 1.7)
            n_edited = n_value * 1.7 / (0.7 + effective_stress_depth)

            n_edited_cs = n_edited * alpha + beta

            total_stress.append(total_stress_depth)
            effective_stress.append(effective_stress_depth)
            rd = SPTData.calculate_rd_japanese(depth)

            csr = max_acceleration * (total_stress_depth / effective_stress_depth) * rd
            csr_values.append(csr)
            n_edited_values.append(n_edited)
            n_edited_values_cs.append(n_edited_cs)
            if n_edited_cs < 14:
                CRR = 0.0882 * ((n_edited_cs / 1.7) ** 0.5)
            else:
                CRR = 0.0882 * ((n_edited_cs / 1.7) ** 0.5) + (1.6 * (10 ** (-6)) * ((n_edited_cs - 14) ** 4.5))

            CRR_7_5.append(CRR)
            k_alpha = result.k_alpha
            if k_sigma_status:
                k_sigma = result.k_sigma_or_dr
            else:
                relative_density = result.k_sigma_or_dr
                # Given data
                dr_values = np.array([40, 60, 80])
                f_values = np.array([0.8, 0.7, 0.6])

                # Create a linear interpolation function
                linear_interp = interpolate.interp1d(dr_values, f_values, fill_value="extrapolate")
                f = linear_interp(relative_density)
                k_sigma = float((effective_stress_depth / 1) ** (f - 1))
            msf = soil_profile.msf
            CRR_final = msf * k_alpha * k_sigma * CRR
            fl = CRR_final / csr
            CRR_main.append(CRR_final)
            Fl.append(fl)

        return (depthList, total_stress, effective_stress, csr_values, n_edited_values,
                n_edited_values_cs, CRR_7_5, CRR_main, Fl)

    def calculate_alpha_beta(self, fine_content):
        if fine_content < 10:
            alpha, beta = 1, 0
        elif 10 <= fine_content < 60:
            alpha = (fine_content + 40) / 50
            beta = (fine_content - 10) / 18
        else:
            alpha, beta = (fine_content / 20) - 1, (fine_content - 10) / 18
        return alpha, beta
