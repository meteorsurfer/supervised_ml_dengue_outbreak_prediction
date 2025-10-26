import streamlit as st

UI_CLEAN = st.secrets["UI_CLEAN"]

def clean_sb():
    st.markdown(UI_CLEAN, unsafe_allow_html=True)
    return

def nav_menu(current_page):
    pages = {
        "Exploratory Data Analysis": "/",
        "ML Prediction": "/predict",
    }

    if current_page and current_page in pages.values():
        current_pair = next((k, v) for k, v in pages.items() if v == current_page)
        other_pages = {k: v for k, v in pages.items() if v != current_page}
        pages = {current_pair[0]: current_pair[1], **other_pages}

    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))

    if pages[selected_page] != current_page:
        st.session_state['last_page'] = selected_page
        st.markdown(
            f"""
            <meta http-equiv="refresh" content="0; url={pages[selected_page]}">
            """,
            unsafe_allow_html=True
        )
        st.stop()