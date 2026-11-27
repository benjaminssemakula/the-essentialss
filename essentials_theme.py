"""Shared Essentials look for the extra pages. Keep this next to project.py."""
import base64
import os

import streamlit as st

APP_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(APP_DIR, "background.mp4")


@st.cache_data(show_spinner=False)
def _load_video(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except OSError:
        return None


CSS = """
<style>
:root {
    --font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
            "Helvetica Neue", "Segoe UI", Inter, system-ui, sans-serif;
    --label: #ffffff; --body: rgba(255,255,255,0.92); --muted: rgba(235,235,245,0.62);
    --blue: #0a84ff; --blue-hi: #3d9dff;
    --fill: rgba(28,28,30,0.52); --fill-deep: rgba(20,20,22,0.78);
    --hairline: rgba(255,255,255,0.10); --hairline-hi: rgba(255,255,255,0.22);
    --r-card: 20px; --r-ctl: 13px; --r-pill: 980px;
    --shadow: 0 10px 34px rgba(0,0,0,0.30);
    --spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
html, body { background: #0b0b0d; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stHeader"], [data-testid="stToolbar"], .main, .block-container {
    background: transparent !important;
}
.custom-background { position: fixed; inset: 0; z-index: -10; overflow: hidden; pointer-events: none; }
.custom-background.no-video {
    background: radial-gradient(120% 90% at 12% 0%, #24304d 0%, transparent 62%),
                radial-gradient(110% 90% at 88% 100%, #3a2a49 0%, transparent 62%), #0b0b0d;
}
.custom-background video {
    position: absolute; top: 50%; left: 50%; width: 100%; height: 100%; object-fit: cover;
    filter: blur(6px) saturate(1.08); transform: translate(-50%, -50%) scale(1.08);
}
.background-overlay {
    position: fixed; inset: 0; z-index: -9; pointer-events: none;
    background: linear-gradient(180deg, rgba(0,0,0,.42) 0%, rgba(0,0,0,.16) 38%, rgba(0,0,0,.18) 62%, rgba(0,0,0,.46) 100%);
}
html, body, .stApp, input, button, select, textarea { font-family: var(--font) !important; -webkit-font-smoothing: antialiased; }
h1 { color: var(--label) !important; font-weight: 700 !important; letter-spacing: -0.028em !important; line-height: 1.06 !important; margin: 0 0 6px 0 !important; }
h2, h3, h4 { color: var(--label) !important; font-weight: 600 !important; letter-spacing: -0.018em !important; }
p, label, li, .stMarkdown, .stText { color: var(--body) !important; }
.lede { color: var(--muted) !important; font-size: 1.05rem; margin: 0 0 24px 0 !important; max-width: 62ch; }
.block-container { width: min(94vw, 1000px) !important; max-width: 1000px !important; padding: 40px 28px 96px 28px !important; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { overflow-x: hidden !important; }
[data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] { gap: 16px; }

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--fill) !important;
    backdrop-filter: blur(32px) saturate(180%); -webkit-backdrop-filter: blur(32px) saturate(180%);
    border: 1px solid var(--hairline) !important; border-radius: var(--r-card) !important;
    padding: 24px !important; margin-bottom: 12px !important; box-shadow: var(--shadow);
}
.stTextInput input, .stNumberInput input, .stDateInput input,
.stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea {
    background: rgba(255,255,255,0.07) !important; color: #ffffff !important;
    border: 1px solid var(--hairline) !important; border-radius: var(--r-ctl) !important; font-size: 16px !important;
}
.stTextInput input, .stNumberInput input { padding: 13px 14px !important; min-height: 48px; }
.stTextInput input::placeholder { color: rgba(235,235,245,0.42) !important; }
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--blue) !important; box-shadow: 0 0 0 3.5px rgba(10,132,255,0.28) !important; outline: none !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label {
    color: var(--muted) !important; font-size: 0.86rem !important; font-weight: 500 !important;
}
.stNumberInput [data-baseweb="input"], .stNumberInput [data-baseweb="base-input"] { border-radius: var(--r-ctl) !important; }
.stNumberInput [data-baseweb="input"] { overflow: hidden; background: rgba(255,255,255,0.07) !important; border: 1px solid var(--hairline) !important; }
.stNumberInput [data-baseweb="base-input"], .stNumberInput [data-baseweb="input"] input {
    background: transparent !important; border: none !important; box-shadow: none !important; border-radius: 0 !important;
}
.stNumberInput button { background: rgba(255,255,255,0.05) !important; color: #fff !important; border: none !important; border-radius: 0 !important; }

.stButton > button, .stDownloadButton > button {
    background: rgba(255,255,255,0.09) !important; color: #ffffff !important;
    border: 1px solid var(--hairline) !important; border-radius: var(--r-pill) !important;
    min-height: 46px; font-size: 0.96rem !important; font-weight: 500 !important;
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.16), 0 2px 8px rgba(0,0,0,0.22);
    transition: transform 0.36s var(--spring), background 0.2s ease;
}
.stDownloadButton > button { width: 100%; }
.stButton > button:hover, .stDownloadButton > button:hover { background: rgba(255,255,255,0.16) !important; }
.stButton > button:active, .stDownloadButton > button:active { transform: scale(0.95) !important; }
.stButton > button:disabled, .stDownloadButton > button:disabled { opacity: 0.38 !important; }
.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, var(--blue-hi) 0%, var(--blue) 100%) !important;
    border-color: transparent !important; font-weight: 600 !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.32), 0 8px 24px rgba(10,132,255,0.42);
}
.stAlert { background: var(--fill) !important; border: 1px solid var(--hairline) !important; border-radius: var(--r-ctl) !important; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] { color: #fff !important; font-weight: 600 !important; letter-spacing: -0.03em !important; }

div[data-testid="stTable"] table { background: var(--fill-deep) !important; border-radius: var(--r-card) !important; overflow: hidden !important; border-collapse: separate !important; border-spacing: 0 !important; }
div[data-testid="stTable"] th { color: var(--muted) !important; background: rgba(255,255,255,0.06) !important; font-size: 0.85rem !important; font-weight: 600 !important; padding: 14px 16px !important; border: none !important; }
div[data-testid="stTable"] td { color: #fff !important; padding: 14px 16px !important; background: transparent !important; border: none !important; border-top: 1px solid var(--hairline) !important; }

.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--hairline); }
.stTabs [data-baseweb="tab"] { background: transparent; color: var(--muted); }
.stTabs [aria-selected="true"] { color: #ffffff; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--blue) !important; }
.stProgress [data-baseweb="progress-bar"] > div { background: rgba(255,255,255,0.12) !important; border-radius: 99px; }
.stProgress [data-baseweb="progress-bar"] > div > div { background: linear-gradient(90deg, var(--blue-hi), var(--blue)) !important; border-radius: 99px; }

[data-testid="stSidebar"] { background: var(--fill-deep) !important; backdrop-filter: blur(30px); border-right: 1px solid var(--hairline); }
[data-testid="stSidebarNav"] a { color: var(--body) !important; border-radius: var(--r-ctl); }
#MainMenu, footer { visibility: hidden; }

@media (max-width: 768px) {
    .block-container { padding: 20px 14px 72px 14px !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { padding: 16px !important; border-radius: 18px !important; }
    h1 { font-size: 2rem !important; }
    div[data-testid="stTable"] { overflow-x: auto !important; }
    div[data-testid="stTable"] table { min-width: 520px !important; }
}
</style>
"""


def apply_theme(title, icon):
    """Call first on every page: page config, video background, theme CSS."""
    st.set_page_config(page_title=title, page_icon=icon, layout="centered")
    video = _load_video(VIDEO_PATH)
    if video:
        st.markdown(
            f'<div class="custom-background"><video autoplay muted loop playsinline preload="auto">'
            f'<source src="data:video/mp4;base64,{video}" type="video/mp4"></video></div>'
            f'<div class="background-overlay"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="custom-background no-video"></div><div class="background-overlay"></div>',
            unsafe_allow_html=True,
        )
    st.markdown(CSS, unsafe_allow_html=True)


def require_profile():
    """Keep the same sign-in gate as the main app."""
    if not st.session_state.get("profile_complete"):
        st.title("Set up your profile first")
        st.markdown(
            '<p class="lede">Open the home page, fill in your profile, then come back here.</p>'
            '<a href="/" target="_self" style="color:#3d9dff">← Go to Essentials</a>',
            unsafe_allow_html=True,
        )
        st.stop()
