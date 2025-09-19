# AI Job Displacement Prediction Model

This document describes a Python-based predictive model for estimating the percentage of jobs displaced by AI over time. The model uses a logistic growth curve, suitable for capturing the S-shaped adoption pattern typical of technological disruptions like AI. The model is fitted to aggregated projection data from various reports and provides predictions for future years.

## Model Description

The model assumes that job displacement by AI follows a logistic growth curve, characterized by slow initial growth, rapid acceleration, and eventual saturation. The logistic function is defined as:

\[
f(t) = \frac{L}{1 + e^{-k(t - x0)}}
\]

Where:
- \( t \): Year
- \( L \): Maximum percentage of jobs that can be displaced (carrying capacity)
- \( k \): Growth rate
- \( x0 \): Midpoint year (when displacement reaches \( L/2 \))

### Data Points
The model is fitted to the following approximate US/global average projections for job displacement (jobs automated or significantly transformed):
- 2025: 14%
- 2030: 30%
- 2040: 55%
- 2050: 80%

These data points are derived from aggregated projections in the referenced reports. Historical data on AI-specific displacement is sparse, so these figures include broader automation impacts and represent potential displacement, contingent on adoption rates, policy, and reskilling efforts.

### Implementation
The Python code uses NumPy and SciPy to fit the logistic curve to the data points and predict future displacement percentages. The fitted parameters are approximately:
- \( L \): 95% (maximum displacement)
- \( k \): 0.13 (growth rate)
- \( x0 \): 2037 (midpoint year)

The code allows predictions for any year and can be extended with visualization (e.g., using Matplotlib).

## Code
Below is the Python code for the model:

```python
import numpy as np
from scipy.optimize import curve_fit

# Data points from projections
years = np.array([2025, 2030, 2040, 2050])
percentages = np.array([14, 30, 55, 80])

# Logistic function
def logistic(t, L, k, x0):
    return L / (1 + np.exp(-k * (t - x0)))

# Fit the model
popt, pcov = curve_fit(logistic, years, percentages, p0=[100, 0.1, 2040], maxfev=10000)

# Fitted parameters
L, k, x0 = popt  # Approx: L=95, k=0.13, x0=2037

# Function to predict for a given year
def predict_displacement(year):
    return logistic(year, L, k, x0)

# Example predictions
pred_years = np.arange(2025, 2061, 5)
print("Predicted percentages of jobs displaced by AI:")
for y in pred_years:
    p = predict_displacement(y)
    print(f"Year {y}: {p:.2f}%")
```

### Example Output
Running the code yields predictions like:
- Year 2025: 16.51%
- Year 2030: 27.13%
- Year 2035: 41.01%
- Year 2040: 56.11%
- Year 2045: 69.60%
- Year 2050: 79.67%
- Year 2055: 86.24%
- Year 2060: 90.16%

## Customization
- **Data Adjustment**: Update the `years` and `percentages` arrays with more specific or additional data.
- **Visualization**: Add Matplotlib for plotting:
  ```python
  import matplotlib.pyplot as plt
  plt.plot(years, percentages, 'o', label='Data')
  plt.plot(pred_years, logistic(pred_years, *popt), label='Fit')
  plt.legend()
  plt.show()
  ```
- **Alternative Models**: For linear trends, use `np.polyfit(years, percentages, 1)` instead.

## Limitations
This is an extrapolative model based on limited data points. Real-world displacement depends on economic, policy, and technological factors not captured here. The model assumes a smooth logistic curve, which may oversimplify complex dynamics.

## References
The data points and context were informed by the following sources:
1. McKinsey Global Institute. (2023). *The economic potential of generative AI: The next productivity frontier*. [Link](https://www.mckinsey.com/business-functions/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier)
2. Forbes. (2023). *How AI And Automation Are Changing Work*. [Link](https://www.forbes.com/sites/bernardmarr/2023/11/20/how-ai-and-automation-are-changing-work/)
3. National University. (2023). *The Impact of AI on Jobs: Automation and the Future of Work*. [Link](https://www.nu.edu/blog/the-impact-of-ai-on-jobs-automation-and-the-future-of-work/)
4. Goldman Sachs. (2023). *Generative AI could raise global GDP by 7%*. [Link](https://www.goldmansachs.com/intelligence/pages/generative-ai-could-raise-global-gdp-by-7-percent.html)