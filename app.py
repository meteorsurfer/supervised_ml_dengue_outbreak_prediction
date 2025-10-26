"""
APD Dengue Outbreak Prediction Dashboard

Streamlit interface for visualizing ML-driven dengue outbreak forecasts up to 3 months ahead,
based on environmental and epidemiological data.

Disclaimer:
This tool is intended for educational and personal upskilling purposes only. It is not designed
for operational use or public health decision-making. Always consult official health authorities
for verified outbreak information and guidance.
"""

import os
import warnings
from utils.wrangling import load_eda_data
from utils.core import Homepage

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(__file__)
FAVICON = os.path.join(BASE_DIR, "input", "logo.svg")

eda_data = load_eda_data()

app = Homepage(
    page_title="APD | Exploratory Data Analysis",
    page_icon=FAVICON,
    eda_data=eda_data
)

app.run()
