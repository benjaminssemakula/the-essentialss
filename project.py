import base64
import math
import random
import textwrap
import os
from uuid import uuid4

import streamlit as st
import streamlit.components.v1 as components

# ==========================================================
# PAGE CONFIG  (first Streamlit call, only once)
# ==========================================================

st.set_page_config(
    page_title="Essentials",
    page_icon="🎓",
    layout="centered",
)


APP_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(APP_DIR, "background.mp4")

# Gates the Calculator, Grades, and Quiz sections until the profile form
# below is filled in and submitted — set to True only once, inside the
# Profile section itself.
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False


# ==========================================================
# LIVE VIDEO BACKGROUND
# ==========================================================

@st.cache_data(show_spinner=False)
def load_background_video(path):
    """Return background.mp4 as base64, or None if it can't be read."""
    try:
        with open(path, "rb") as video_file:
            return base64.b64encode(video_file.read()).decode()
    except OSError:
        return None


video_base64 = load_background_video(VIDEO_PATH)

if video_base64:
    st.markdown(
        f"""
        <div class="custom-background">
            <video autoplay muted loop playsinline preload="auto">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>
        <div class="background-overlay"></div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="custom-background no-video"></div>
        <div class="background-overlay"></div>
        """,
        unsafe_allow_html=True,
    )
    st.warning(
        f"background.mp4 wasn't found next to this script ({APP_DIR}). "
        "Showing a gradient instead."
    )


# ==========================================================
# THEME
# tokens → background → type → cards → controls → table
# → nav → motion → responsive
# ==========================================================

st.markdown(
    """
<style>

/* ---------- tokens ---------- */
:root {
    --font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
            "Helvetica Neue", "Segoe UI", Inter, system-ui, sans-serif;

    --label: #ffffff;
    --body: rgba(255, 255, 255, 0.92);
    --muted: rgba(235, 235, 245, 0.62);

    --blue: #0a84ff;
    --blue-hi: #3d9dff;
    --orange: #ff9f0a;
    --orange-hi: #ffb340;
