from abc import ABC, abstractmethod
import streamlit as st
import pandas as pd
from utils.interface import clean_sb, nav_menu
from utils.wrangling import dataset_info
from utils.markup import (
    display_headline,
    display_metadata,
    visualize_denv_per_categories,
    visualize_geographic_cases,
    visualize_trend,
    region_month_cases_density,
    display_footer,
    display_disclaimer,
    predict_dengue_risk_3_months,
    display_sample_outbreak_news
)


class App(ABC):
    """Abstract base class for Streamlit app pages."""

    MAIN_LAYOUT = "wide"
    MAIN_SIDEBAR_STATE = "expanded"

    def __init__(self, page_title: str, page_icon: str, eda_data: pd.DataFrame = None):
        self.page_title = page_title
        self.page_icon = page_icon
        self.eda_data = eda_data

    def configure_page(self):
        """Configure Streamlit page layout and sidebar state."""
        st.set_page_config(
            page_title=self.page_title,
            page_icon=self.page_icon,
            layout=self.MAIN_LAYOUT,
            initial_sidebar_state=self.MAIN_SIDEBAR_STATE,
        )

        clean_sb()

    @abstractmethod
    def run(self):
        """Render the Streamlit page."""
        pass

class Homepage(App):
    """Homepage for exploratory dengue case analysis."""

    def __init__(self, page_title: str, page_icon: str, eda_data: pd.DataFrame):
        super().__init__(page_title, page_icon, eda_data)

    def _section_title(self, title: str):
        st.markdown(
            f"<div style='text-align: center; color: white;'>{title}</div>",
            unsafe_allow_html=True,
        )

    def run(self):
        self.configure_page()

        nav_menu("/")

        display_headline("""
        Exploratory Analysis of Dengue Cases Across Philippine Regions (2016–2023)
        """)

        cleaned_eda = dataset_info(self.eda_data)
        display_metadata(cleaned_eda)

        col1, col2 = st.columns(2)

        with col1:
            self._section_title("Median Dengue Cases Per Location (2016–2023)")
            visualize_geographic_cases(self.eda_data)
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            self._section_title("Density Map for Dengue Cases Per Region and Month (2016–2023)")
            region_month_cases_density(self.eda_data)

        with col2:
            self._section_title("Median Dengue Cases Per Category (2016–2023)")
            visualize_denv_per_categories(self.eda_data)
            self._section_title("Median Dengue Cases Per Region Trend (2016–2023)")
            visualize_trend(self.eda_data)

        display_footer()

class Prediction(App):

    def __init__(self, page_title, page_icon, eda_data = None):
        super().__init__(page_title, page_icon, eda_data)

    def run(self):

        self.configure_page()

        nav_menu("/predict")

        display_headline("Predicting 3-Month Dengue Outbreak Risk from Current Weather Patterns")

        display_disclaimer()
        st.write("")

        col1, col2 = st.columns([1, 1])

        with col2:
            predict_dengue_risk_3_months()

        with col1:
            display_sample_outbreak_news("input/")

        with st.expander("End-to-End ML Lifecycle Tech Stack"):
            st.markdown("""
                <div style="font-family: 'Segoe UI', sans-serif; line-height: 1.6; font-size: 15px;">
                <h3>🧠 Modeling Framework</h3>
                <p><strong>Microsoft LightGBM</strong> (optimized for imbalanced WHO-backed outbreak thresholding)</p>

                <h3>📦 Language & IDEs</h3>
                <ul>
                    <li><code>Python</code></li>
                    <li><code>Jupyter Notebook</code></li>
                    <li><code>VS Code</code></li>
                </ul>

                <h3>🌐 Data Gathering & Preparation</h3>
                <ul>
                    <li><code>pandas</code>, <code>GeoPandas</code>, <code>requests</code>, <code>concurrent.futures</code></li>
                    <li><code>QGIS</code></li>
                </ul>

                <h3>📊 Exploratory Data Analysis</h3>
                <ul>
                    <li><code>matplotlib</code>, <code>seaborn</code>, <code>pandas</code>, <code>Streamlit</code></li>
                </ul>

                <h3>🔍 Modeling & Optimization</h3>
                <ul>
                    <li><code>scikit-learn</code>, <code>NumPy</code>, <code>LightGBM</code>, <code>XGBoost</code>, <code>CatBoost</code>, <code>Optuna</code></li>
                </ul>

                <h3>🚀 Deployment & Version Control</h3>
                <ul>
                    <li><code>Flask</code>, <code>Streamlit</code>, <code>Git</code>, <code>GitHub</code></li>
                </ul>
                </div>
            """, unsafe_allow_html=True)

        display_footer()
