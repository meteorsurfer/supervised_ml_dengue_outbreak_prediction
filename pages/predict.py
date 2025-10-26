"""
Main entry point for the APD Dengue Outbreak Prediction interface (ML Predictions).

This module launches the Streamlit-based dashboard for interacting with the machine learning
model that forecasts dengue outbreak probabilities. It provides users with access to model
predictions based on recent environmental and epidemiological data, enabling exploration of
forecasted risk levels across different time horizons.

Disclaimer:
This tool is intended for educational and personal upskilling purposes only. It is not designed
for operational use or public health decision-making. Always consult official health authorities
for verified outbreak information and guidance.
"""

import warnings
import os
from utils.core import Prediction

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(__file__)
FAVICON = os.path.join(BASE_DIR, "input", "logo.svg")

app = Prediction(
    page_title = "APD | ML Predictions",
    page_icon=FAVICON
)

app.run()
