# Liquefaction Potential Analysis Application

## Introduction

This application is designed to assess the liquefaction potential of soil profiles using Standard Penetration Test (SPT) data. It implements two main calculation methods: the Japanese method and the NCEER (National Center for Earthquake Engineering Research) method. The application considers all soil as susceptible to liquefaction and does not currently control for gravel percentage, liquid limit, or plasticity index.

## Features

- Soil profile modeling with multiple layers
- SPT data input and management
- Calculation of liquefaction potential using Japanese and NCEER methods
- Visualization of results

## Installation

1. Clone the repository:
  https://github.com/alist2000/Liquefaction_Potential.git  
2. Install the required dependencies:
   pip install -r requirements.txt

## Usage

1. Run the main application:
   python main.py

2. Input soil profile data:
- Add layers with properties (name, unit weight, thickness, fine content)
- Set groundwater level, maximum ground acceleration, and magnitude scaling factor
3. Input SPT data:
- Add SPT results (depth, N-value, hammer energy, correction factors)
4. Run analysis
5. View and interpret results

## Calculation Methods

### Japanese Method

- Cyclic Stress Ratio (CSR): `CSR = (amax / g) * (σv / σv') * rd`
- Where:
    amax: Maximum ground acceleration
    σv: Total vertical stress
    σv': Effective vertical stress
    rd: Stress reduction coefficient (rd = 1 - 0.015 * depth)
  
- Corrected N-value: `N1 = N * 1.7 / (0.7 + σv')`, `N1,cs = a * N1 + b`
- Where:
    N: Measured SPT N-value
    σv': Effective vertical stress in kg/cm²
    a and b: Correction factors based on fine content
  
- Cyclic Resistance Ratio (CRR): 
- For N1,cs < 14: `CRR = 0.0882 * ((N1,cs / 1.7) ^ 0.5)`
- For N1,cs ≥ 14: `CRR = 0.0882 * ((N1,cs / 1.7) ^ 0.5) + 1.6 * 10^(-6) * (N1,cs - 14)^4.5`
- Factor of Safety: `FL = (CRR * MSF * Kσ * Kα) / CSR`

### NCEER Method

- Cyclic Stress Ratio (CSR): `CSR = 0.65 * (amax / g) * (σv / σv') * rd`
- Where rd is calculated as:
    For depth ≤ 9.15m: rd = 1 - 0.00765 * depth
    For 23 ≥ depth > 9.15m: rd = 1.174 - 0.0267 * depth
  
- Corrected N-value: `N1 60 = N * Cb * Cn * Cs * Cr * (ER/60)`, `N1,60,cs = α + N1 60 * β`
- Cyclic Resistance Ratio (CRR): `CRR = (1 / (34 - N1,60,cs)) + (N1,60,cs / 135) + (50 / ((10 * N1,60,cs + 45)^2)) - (1 / 200)`
- Factor of Safety: `FL = (CRR * MSF * Kσ * Kα) / CSR`

### Magnitude Scaling Factor (MSF)

When the user inputs the earthquake magnitude (M) instead of directly specifying the MSF, the application uses the following default function to calculate MSF:

`MSF = (7.5 / M)^3.3`

This equation is based on the work of Andrus and Stokoe (1997) and is used in practice. It accounts for the fact that larger magnitude earthquakes typically have longer durations and more cycles of strong shaking, which increases the likelihood of liquefaction.

The MSF is then used in the calculation of the Factor of Safety against liquefaction for both the Japanese and NCEER methods.

## Soil Profile Model

### Components:
- Soil layers with properties: name, unit weight (gamma), thickness, and fine content
- Groundwater level
- Maximum ground acceleration
- Magnitude scaling factor (MSF)

### Stress Calculations:
- Total stress: Calculated by summing the product of unit weight and thickness for each layer up to the depth of interest
- Effective stress: Calculated by subtracting pore water pressure from total stress

## SPT Data Model

### Components:
- Depth
- N-value
- Hammer energy ratio
- Correction factors: Cb (borehole diameter), Cs (sampler type), Cr (rod length)
- K_alpha (static shear stress correction factor)
- K_sigma or Dr (overburden stress correction factor or relative density)

## Correction Factors

### Fine Content Correction (α and β):
Japanese Method:
- For FC < 10%: a = 1, b = 0
- For 10% ≤ FC < 60%: a = (FC + 40) / 50, b = (FC - 10) / 18
- For FC ≥ 60%: a = (FC / 20) - 1, b = (FC - 10) / 18

NCEER Method:
- For FC ≤ 5%: α = 0, β = 1
- For 5% < FC ≤ 35%: α = exp(1.76 - (190 / FC^2)), β = 0.99 + (FC^1.5 / 1000)
- For FC > 35%: α = 5, β = 1.2

### Overburden Stress Correction Factor (Kσ):
Kσ = (σv' / 100)^(f - 1)
Where f is interpolated based on relative density (Dr):
- For Dr = 40%: f = 0.8
- For Dr = 60%: f = 0.7
- For Dr = 80%: f = 0.6

## Assumptions and Limitations

- The application assumes a layered soil profile with uniform properties within each layer.
- The groundwater table is assumed to be horizontal.
- The application does not account for dynamic pore pressure generation during shaking.
- The correction factors and empirical correlations used in the methods are based on historical data and may not be applicable to all soil types or conditions.
- The application does not consider the effects of soil aging, cementation, or other factors that may influence liquefaction resistance.
- The methods used are primarily developed for clean sands and may have limitations when applied to silty or clayey soils.
- Currently, the application does not control for gravel percentage, liquid limit, or plasticity index.

## Future Development

This application is open for further development. Some potential areas for improvement include:

1. Implementing controls for gravel percentage, liquid limit, and plasticity index
2. Enhancing the user interface for easier data input and result visualization
3. Adding more calculation methods or variations of existing methods
4. Implementing sensitivity analysis features
5. Adding report generation functionality

Contributions to the development of this application are welcome and encouraged. If you're interested in contributing, please feel free to fork the repository and submit pull requests.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under a Modified MIT License - see the [LICENSE.md](LICENSE.md) file for details. Key points:

1. The software is free for academic, scientific, and personal use.
2. Commercial use is prohibited without explicit permission from Ali Safari.
3. Any academic or scientific publication using this software must cite:
   Ali Safari, 2024, Liquefaction Potential Analysis Application

For full terms and conditions, please refer to the LICENSE.md file in this repository.

## Acknowledgments

- Japanese Geotechnical Society for the Japanese method
- National Center for Earthquake Engineering Research (NCEER) for the NCEER method

## Contact

If you have any questions or suggestions, please open an issue in the GitHub repository.

Thank you for your interest in this Liquefaction Potential Analysis Application. Your contributions and feedback are valuable in improving and expanding the capabilities of this tool.
