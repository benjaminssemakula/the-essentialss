import base64
import math
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

    /* macOS vibrancy: low-opacity fill + heavy blur + saturation */
    --fill: rgba(28, 28, 30, 0.52);
    --fill-hi: rgba(58, 58, 62, 0.62);
    --fill-deep: rgba(20, 20, 22, 0.78);
    --hairline: rgba(255, 255, 255, 0.10);
    --hairline-hi: rgba(255, 255, 255, 0.22);

    --r-card: 20px;
    --r-ctl: 13px;
    --r-pill: 980px;

    --shadow: 0 10px 34px rgba(0, 0, 0, 0.30);
    --nav-offset: 104px;
}

/* ---------- background ---------- */
html, body { background: #0b0b0d; }

/* Everything above the video must stay see-through, or the video is hidden. */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
.main,
.block-container {
    background: transparent !important;
}

.custom-background {
    position: fixed;
    inset: 0;
    z-index: -10;
    overflow: hidden;
    pointer-events: none;
}

.custom-background.no-video {
    background:
        radial-gradient(120% 90% at 12% 0%, #24304d 0%, transparent 62%),
        radial-gradient(110% 90% at 88% 100%, #3a2a49 0%, transparent 62%),
        #0b0b0d;
}

.custom-background video {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Light touch: the frosted panels do most of the separation work,
       so the footage still reads as live video. */
    filter: blur(6px) saturate(1.08);
    transform: translate(-50%, -50%) scale(1.08);
}

/* Gentle scrim — darker where text sits, clear through the middle. */
.background-overlay {
    position: fixed;
    inset: 0;
    z-index: -9;
    pointer-events: none;
    background: linear-gradient(
        180deg,
        rgba(0, 0, 0, 0.42) 0%,
        rgba(0, 0, 0, 0.16) 38%,
        rgba(0, 0, 0, 0.18) 62%,
        rgba(0, 0, 0, 0.46) 100%
    );
}

/* ---------- typography ---------- */
html, body, .stApp, input, button, select, textarea {
    font-family: var(--font) !important;
    -webkit-font-smoothing: antialiased;
}

h1 {
    color: var(--label) !important;
    font-weight: 700 !important;
    letter-spacing: -0.028em !important;
    line-height: 1.06 !important;
}

h2, h3, h4 {
    color: var(--label) !important;
    font-weight: 600 !important;
    letter-spacing: -0.018em !important;
}

p, label, li, .stMarkdown, .stText {
    color: var(--body) !important;
    letter-spacing: -0.005em;
}

[data-testid="stCaptionContainer"], .stCaption {
    color: var(--muted) !important;
}

/* A quiet subtitle directly under a page title. */
.lede {
    color: var(--muted) !important;
    font-size: 1.05rem;
    margin: -4px 0 26px 0;
    max-width: 62ch;
}

/* ---------- layout ---------- */
.block-container {
    width: min(94vw, 1000px) !important;
    max-width: 1000px !important;
    margin: 0 auto !important;
    padding: 34px 26px 96px 26px !important;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    overflow-x: hidden !important;
}

/* ---------- vibrancy panels ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--fill) !important;
    backdrop-filter: blur(32px) saturate(180%);
    -webkit-backdrop-filter: blur(32px) saturate(180%);
    border: 1px solid var(--hairline) !important;
    border-radius: var(--r-card) !important;
    padding: 18px !important;
    margin-bottom: 14px !important;
    box-shadow: var(--shadow);
}

/* Layout-only containers stay invisible. */
.st-key-calc_keys [data-testid="stVerticalBlockBorderWrapper"],
.st-key-sci_keys [data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    padding: 0 !important;
}

/* ---------- inputs ---------- */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.07) !important;
    color: #ffffff !important;
    border: 1px solid var(--hairline) !important;
    border-radius: var(--r-ctl) !important;
    font-size: 16px !important;
    transition: border-color 0.18s ease, background 0.18s ease;
}

.stTextInput input,
.stNumberInput input {
    padding: 13px 14px !important;
}

.stTextInput input::placeholder { color: rgba(235, 235, 245, 0.42) !important; }

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--blue) !important;
    background: rgba(255, 255, 255, 0.10) !important;
    box-shadow: 0 0 0 3.5px rgba(10, 132, 255, 0.28) !important;
    outline: none !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stRadio label {
    color: var(--muted) !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
}

/* ---------- login card (profile) ---------- */

/* The status card and the form sit in a two-column row; without this the
   row's cross-axis defaults to flex-start, so the shorter card (the status
   card) just hugs the top and leaves empty space instead of matching the
   taller form's height — making the pair look staggered rather than a
   clean, even split. Stretching both, then centering the shorter card's
   own content inside it, is what makes them line up as one unit. */
div[data-testid="stHorizontalBlock"]:has(.st-key-profile_gate) {
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"]:has(.st-key-profile_gate) > div[data-testid="column"] {
    display: flex;
}

div[data-testid="stHorizontalBlock"]:has(.st-key-profile_gate) > div[data-testid="column"] > div {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.st-key-profile_gate,
.st-key-profile_login {
    display: flex;
    flex: 1;
}

/* profile_login now holds two stacked children (the fields card, then the
   Continue button) instead of just the card, so it needs an explicit
   column direction — plain `display:flex` defaults to row, which would
   place the button beside the card instead of under it. */
.st-key-profile_login {
    flex-direction: column;
    gap: 14px;
}

.st-key-profile_gate [data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.st-key-profile_login [data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1;
}

.st-key-profile_login {
    max-width: 380px;
    margin: 0 auto !important;
}

.login-avatar-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    margin: 6px 0 26px 0;
}

.login-avatar {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(120% 120% at 30% 22%, var(--blue-hi) 0%, var(--blue) 55%, #1f4fa8 100%);
    border: 1px solid var(--hairline-hi);
    box-shadow: 0 10px 28px rgba(10, 132, 255, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.22);
    color: #ffffff;
    font-size: 2.1rem;
    font-weight: 600;
    letter-spacing: -0.02em;
}

.login-avatar.login-avatar-empty {
    background: rgba(255, 255, 255, 0.08);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.10);
    color: rgba(235, 235, 245, 0.55);
}

.login-avatar svg { width: 40px; height: 40px; }

.login-greeting {
    color: var(--label);
    font-size: 1.12rem;
    font-weight: 600;
    letter-spacing: -0.015em;
    text-align: center;
}

.login-subtext {
    color: var(--muted);
    font-size: 0.88rem;
    text-align: center;
    margin-top: -8px;
}

/* The name field reads as the primary "username" row: bigger, centered. */
.st-key-profile_login .stTextInput:first-of-type input {
    text-align: center;
    font-size: 1.08rem;
    font-weight: 500;
}

.login-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--muted);
    font-size: 0.78rem;
    margin: 4px 0 14px 0;
}

.login-divider::before,
.login-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--hairline);
}

/* ---------- profile gate ---------- */
.st-key-profile_gate {
    height: 100%;
    text-align: center;
}

.profile-gate-icon {
    width: 68px;
    height: 68px;
    margin: 2px auto 18px auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid var(--hairline);
    color: rgba(235, 235, 245, 0.72);
}

.profile-gate-icon svg { width: 28px; height: 28px; }

.profile-gate-title {
    color: var(--label);
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: -0.018em;
    margin-bottom: 8px;
}

.profile-gate-subtext {
    color: var(--muted) !important;
    font-size: 0.92rem;
    max-width: 34ch;
    margin: 0 auto 22px auto;
}

.profile-gate-checklist {
    display: inline-flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 11px;
    text-align: left;
}

.profile-gate-row {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--muted);
    font-size: 0.94rem;
}

.profile-gate-row svg { width: 18px; height: 18px; flex-shrink: 0; }

.profile-gate-row.done span {
    color: var(--body);
    font-weight: 500;
}

/* ---------- buttons ---------- */
.stButton > button {
    background: rgba(255, 255, 255, 0.09) !important;
    color: #ffffff !important;
    border: 1px solid var(--hairline) !important;
    border-radius: var(--r-pill) !important;
    min-height: 46px;
    font-size: 0.96rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    transition: background 0.18s ease, transform 0.12s ease, box-shadow 0.18s ease;
}

.stButton > button:hover {
    background: rgba(255, 255, 255, 0.16) !important;
    border-color: var(--hairline-hi) !important;
}

.stButton > button:active { transform: scale(0.975); }

.stButton > button:focus-visible {
    outline: none !important;
    box-shadow: 0 0 0 3.5px rgba(10, 132, 255, 0.45) !important;
}

.stButton > button:disabled {
    opacity: 0.38 !important;
    transform: none !important;
}

/* Primary actions in Apple blue. */
.stButton > button[kind="primary"] {
    background: var(--blue) !important;
    border-color: transparent !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(10, 132, 255, 0.34);
}

.stButton > button[kind="primary"]:hover {
    background: var(--blue-hi) !important;
}

/* Calculator: a compact, centred keypad instead of one that fills the page. */
.st-key-calc_keys,
.st-key-sci_keys,
.calc-shell {
    max-width: 392px;
    margin-left: auto !important;
    margin-right: auto !important;
}

.st-key-calc_keys .stButton > button,
.st-key-sci_keys .stButton > button {
    height: 56px;
    min-height: 56px;
    padding: 0 !important;
    border-radius: var(--r-pill) !important;
    font-size: 1.08rem !important;
    font-weight: 400 !important;
    background: rgba(255, 255, 255, 0.11) !important;
}

.st-key-sci_keys .stButton > button {
    height: 44px;
    min-height: 44px;
    font-size: 0.94rem !important;
}

.st-key-divide .stButton > button,
.st-key-multiply .stButton > button,
.st-key-minus .stButton > button,
.st-key-plus .stButton > button,
.st-key-equals .stButton > button {
    background: var(--orange) !important;
    border-color: transparent !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

.st-key-divide .stButton > button:hover,
.st-key-multiply .stButton > button:hover,
.st-key-minus .stButton > button:hover,
.st-key-plus .stButton > button:hover,
.st-key-equals .stButton > button:hover {
    background: var(--orange-hi) !important;
}

.st-key-clear .stButton > button,
.st-key-backspace .stButton > button {
    background: rgba(255, 255, 255, 0.26) !important;
    color: #ffffff !important;
}

/* Calculator readout */
.calc-readout {
    text-align: right;
    font-size: 2.15rem;
    font-weight: 300;
    letter-spacing: -0.03em;
    color: #ffffff;
    padding: 16px 18px 18px 18px;
    min-height: 76px;
    word-break: break-all;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--hairline);
    border-radius: var(--r-card);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    margin-bottom: 16px;
}

.calc-readout .placeholder { color: rgba(235, 235, 245, 0.35); }

/* ---------- alerts, metrics, radios ---------- */
.stAlert {
    background: var(--fill) !important;
    border: 1px solid var(--hairline) !important;
    border-radius: var(--r-ctl) !important;
    backdrop-filter: blur(24px) saturate(170%);
    -webkit-backdrop-filter: blur(24px) saturate(170%);
}

[data-testid="stMetricLabel"] { color: var(--muted) !important; }

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 600 !important;
    letter-spacing: -0.03em !important;
}

.stRadio [role="radiogroup"] label {
    color: var(--body) !important;
    font-size: 0.98rem !important;
}

/* ---------- grading table ---------- */
div[data-testid="stTable"] table {
    background: var(--fill-deep) !important;
    border-radius: var(--r-card) !important;
    overflow: hidden !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
}

div[data-testid="stTable"] th {
    color: var(--muted) !important;
    background: rgba(255, 255, 255, 0.06) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 14px 16px !important;
    border: none !important;
}

div[data-testid="stTable"] td {
    color: #ffffff !important;
    font-size: 0.97rem !important;
    font-weight: 400 !important;
    padding: 14px 16px !important;
    background: transparent !important;
    border: none !important;
    border-top: 1px solid var(--hairline) !important;
}

/* ---------- rhythm ---------- */
hr {
    border: none !important;
    border-top: 1px solid var(--hairline) !important;
    margin: 30px 0 !important;
}

.section-gap { height: 74px; }

/* ---------- scroll anchors ---------- */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container {
    scroll-behavior: smooth;
    scroll-padding-top: var(--nav-offset);
}

.section-anchor {
    display: block;
    height: 1px;
    scroll-margin-top: var(--nav-offset);
}

/* ---------- brand mark ---------- */
.brand-mark {
    text-align: center;
    color: var(--label);
    font-weight: 600;
    font-size: 1.05rem;
    letter-spacing: -0.02em;
    margin: 4px 0 14px 0;
}

/* ---------- navigation (segmented control) ---------- */
.navigation-bar {
    position: sticky;
    top: 10px;
    z-index: 999;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
    padding: 5px;
    margin-bottom: 30px;
    background: rgba(28, 28, 30, 0.46);
    backdrop-filter: blur(34px) saturate(180%);
    -webkit-backdrop-filter: blur(34px) saturate(180%);
    border: 1px solid var(--hairline);
    border-radius: var(--r-pill);
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.34);
}

.navigation-link {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    text-decoration: none !important;
    color: var(--body) !important;
    background: transparent;
    border-radius: var(--r-pill);
    padding: 10px 6px;
    min-height: 40px;
    font-size: 0.88rem;
    font-weight: 500;
    letter-spacing: -0.01em;
    transition: background 0.2s ease, color 0.2s ease;
}

.navigation-link:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #ffffff !important;
}

.navigation-link:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(10, 132, 255, 0.5);
}

.navigation-link-locked {
    color: rgba(235, 235, 245, 0.34) !important;
    cursor: not-allowed;
}

/* ---------- dialogs + motion ---------- */
@keyframes sheetIn {
    from { opacity: 0; transform: scale(0.94) translateY(16px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes resultPop {
    0%   { opacity: 0; transform: scale(0.88); }
    60%  { opacity: 1; transform: scale(1.03); }
    100% { opacity: 1; transform: scale(1); }
}

[data-testid="stDialog"] {
    animation: sheetIn 0.34s cubic-bezier(0.32, 0.72, 0, 1);
}

[data-testid="stDialog"] > div {
    background: rgba(30, 30, 32, 0.82) !important;
    backdrop-filter: blur(44px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(44px) saturate(180%) !important;
    border: 1px solid var(--hairline-hi) !important;
    border-radius: 26px !important;
    box-shadow: 0 32px 80px rgba(0, 0, 0, 0.64) !important;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* ---------- profile success popup ---------- */
@keyframes profileSuccessIn {
    0% { opacity: 0; transform: translateY(18px) scale(.94); }
    55% { opacity: 1; transform: translateY(-3px) scale(1.015); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes profileRing {
    0% { transform: scale(.45); opacity: 0; }
    55% { transform: scale(1.08); opacity: .35; }
    100% { transform: scale(1); opacity: 0; }
}

@keyframes profileCheck {
    0% { stroke-dashoffset: 80; opacity: 0; }
    45% { opacity: 1; }
    100% { stroke-dashoffset: 0; opacity: 1; }
}

@keyframes profileFloat {
    0%, 100% { transform: translateY(0) rotate(-1deg); }
    50% { transform: translateY(-7px) rotate(1deg); }
}

.profile-success-card {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 8px 4px 4px;
    animation: profileSuccessIn .55s cubic-bezier(.22,1,.36,1) both;
}

.profile-success-card::before {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    left: 50%;
    top: 22px;
    transform: translateX(-50%);
    border-radius: 50%;
    background: radial-gradient(circle, rgba(10,132,255,.18), transparent 68%);
    pointer-events: none;
}

.profile-success-art {
    position: relative;
    width: 150px;
    height: 120px;
    margin: 0 auto 2px;
    animation: profileFloat 3.8s ease-in-out infinite;
}

.profile-success-art img {
    width: 150px;
    height: 120px;
    object-fit: contain;
    filter: drop-shadow(0 18px 24px rgba(0,0,0,.28));
}

.profile-success-check {
    position: absolute;
    right: 2px;
    bottom: 0;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: linear-gradient(145deg, #34c759, #20a94b);
    border: 4px solid rgba(30,30,32,.92);
    box-shadow: 0 10px 26px rgba(52,199,89,.28);
}

.profile-success-check::before {
    content: "";
    position: absolute;
    inset: -8px;
    border: 2px solid rgba(52,199,89,.4);
    border-radius: 50%;
    animation: profileRing 1.1s ease-out .2s both;
}

.profile-success-check svg {
    width: 22px;
    height: 22px;
}

.profile-success-check path {
    fill: none;
    stroke: #fff;
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 80;
    stroke-dashoffset: 80;
    animation: profileCheck .65s cubic-bezier(.65,0,.35,1) .28s forwards;
}

.profile-success-kicker {
    color: #3d9dff;
    font-size: .74rem;
    font-weight: 800;
    letter-spacing: .13em;
    text-transform: uppercase;
    margin: 2px 0 8px;
}

.profile-success-title {
    color: #fff;
    font-size: 1.8rem;
    font-weight: 760;
    letter-spacing: -.04em;
    line-height: 1.05;
    margin-bottom: 8px;
}

.profile-success-text {
    color: rgba(235,235,245,.58);
    font-size: .88rem;
    line-height: 1.45;
    max-width: 320px;
    margin: 0 auto 18px;
}

.profile-success-details {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 0 auto 6px;
    max-width: 360px;
}

.profile-success-detail {
    padding: 10px 12px;
    text-align: left;
    border-radius: 13px;
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.045);
}

.profile-success-detail span {
    display: block;
    color: rgba(235,235,245,.38);
    font-size: .65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 3px;
}

.profile-success-detail strong {
    display: block;
    color: rgba(255,255,255,.92);
    font-size: .8rem;
    font-weight: 650;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

[data-testid="stDialog"] [data-testid="stDialogContent"] {
    padding-top: 0 !important;
}

@media (max-width: 520px) {
    .profile-success-title { font-size: 1.55rem; }
    .profile-success-details { grid-template-columns: 1fr; }
}

/* ---------- chrome ---------- */
#MainMenu, footer { visibility: hidden; }

/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (min-width: 1100px) {
    .block-container { padding-top: 44px !important; padding-bottom: 110px !important; }
    h1 { font-size: 3rem !important; }
    h2 { font-size: 1.9rem !important; }
    h3 { font-size: 1.28rem !important; }
}

@media (min-width: 769px) and (max-width: 1099px) {
    .block-container { width: min(94vw, 880px) !important; }
}

@media (max-width: 768px) {
    :root { --nav-offset: 88px; }

    .block-container { width: 100% !important; max-width: 100% !important; padding: 16px 14px 64px 14px !important; }

    .custom-background video { filter: blur(5px) saturate(1.08); }

    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.42rem !important; }
    h3 { font-size: 1.1rem !important; }
    .lede { font-size: 0.98rem; margin-bottom: 20px; }

    [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 18px !important; padding: 14px !important; margin-bottom: 10px !important; }

    /* Keep keypad rows 4-across instead of wrapping. */
    .stHorizontalBlock:has(.stButton) { flex-wrap: nowrap !important; gap: 8px !important; }
    .stHorizontalBlock:has(.stButton) > div { min-width: 0 !important; flex: 1 1 0 !important; }
    .stHorizontalBlock:has(.stButton) .stButton,
    .stHorizontalBlock:has(.stButton) .stButton > button { width: 100% !important; }

    .stButton > button { min-height: 44px !important; font-size: 0.92rem !important; padding: 8px 6px !important; }

    .st-key-calc_keys, .st-key-sci_keys, .calc-shell { max-width: 100%; }
    .st-key-calc_keys .stButton > button { height: 52px; min-height: 52px; font-size: 1.05rem !important; }
    .st-key-sci_keys .stButton > button { height: 42px; min-height: 42px; font-size: 0.88rem !important; }

    .calc-readout { font-size: 1.9rem; min-height: 68px; padding: 14px 16px; }

    .stTextInput input, .stNumberInput input { min-height: 44px !important; font-size: 16px !important; }

    .brand-mark { font-size: 0.95rem; margin-bottom: 10px; }
    .navigation-bar { top: 6px; padding: 4px; gap: 3px; margin-bottom: 22px; }
    .navigation-link { font-size: 0.74rem; padding: 9px 2px; min-height: 36px; }

    div[data-testid="stTable"] { overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; }
    div[data-testid="stTable"] table { min-width: 520px !important; }
    div[data-testid="stTable"] th, div[data-testid="stTable"] td { padding: 12px !important; font-size: 0.9rem !important; }

    .section-gap { height: 44px; }

    [data-testid="stDialog"] > div {
        width: calc(100vw - 22px) !important;
        max-width: calc(100vw - 22px) !important;
        border-radius: 22px !important;
    }
}

@media (max-width: 420px) {
    .block-container { padding-left: 10px !important; padding-right: 10px !important; }
    .navigation-link { font-size: 0.68rem; }
    .stButton > button { font-size: 0.86rem !important; }
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# SPACING, BUTTON FEEL, NAV, HOME  (Apple-style additions)
# ==========================================================

from html import escape as _escape

st.markdown(
    """
<style>

/* ---------- spacing scale ---------- */
:root {
    --s-1: 8px;  --s-2: 12px; --s-3: 16px;
    --s-4: 24px; --s-5: 40px; --s-6: 64px;
    --spring: cubic-bezier(0.34, 1.56, 0.64, 1);
    --spring-soft: cubic-bezier(0.22, 1.25, 0.36, 1);
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

.block-container { padding: 40px 28px 96px 28px !important; }

[data-testid="stVerticalBlock"]   { gap: var(--s-3); }
[data-testid="stHorizontalBlock"] { gap: var(--s-3); }

[data-testid="stVerticalBlockBorderWrapper"] {
    padding: var(--s-4) !important;
    margin-bottom: var(--s-2) !important;
}

/* Tighter, even keypad rhythm. */
.st-key-calc_keys, .st-key-calc_keys [data-testid="stVerticalBlock"],
.st-key-sci_keys,  .st-key-sci_keys  [data-testid="stVerticalBlock"] { gap: 10px; }
.st-key-calc_keys [data-testid="stHorizontalBlock"],
.st-key-sci_keys  [data-testid="stHorizontalBlock"] { gap: 10px; }

.stApp h1 { margin: 0 0 6px 0 !important; padding: 0 !important; }
.stApp h2, .stApp h3 { margin: 0 !important; padding: 0 0 4px 0 !important; }
.lede { margin: 0 0 var(--s-4) 0 !important; }
hr { margin: var(--s-5) 0 !important; }
.section-gap { height: var(--s-6); }

.stTextInput input, .stNumberInput input { min-height: 48px; }
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stRadio label { margin-bottom: 6px !important; }
.stRadio [role="radiogroup"] { gap: var(--s-2); }

/* ---------- buttons: springy, tactile ---------- */
.stButton > button {
    position: relative;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
    will-change: transform;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.16), 0 2px 8px rgba(0,0,0,0.22);
    transition:
        transform 0.36s var(--spring),
        background 0.2s ease,
        box-shadow 0.28s ease,
        filter 0.2s ease;
}

@media (hover: hover) {
    .stButton > button:hover {
        transform: translateY(-1px) scale(1.018);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.22), 0 8px 22px rgba(0,0,0,0.32);
    }
}

/* Press: sinks in fast, then springs back slowly on release. */
.stButton > button:active {
    transform: scale(0.93) !important;
    filter: brightness(0.9);
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.3), 0 0 0 rgba(0,0,0,0) !important;
    transition-duration: 0.07s, 0.07s, 0.07s, 0.07s;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, var(--blue-hi) 0%, var(--blue) 100%) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.32), 0 8px 24px rgba(10,132,255,0.42);
}
@media (hover: hover) {
    .stButton > button[kind="primary"]:hover {
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.36), 0 12px 32px rgba(10,132,255,0.56);
    }
}

/* Calculator keys: chunkier press. */
.st-key-calc_keys .stButton > button:active,
.st-key-sci_keys  .stButton > button:active {
    transform: scale(0.88) !important;
    background: rgba(255,255,255,0.3) !important;
}
.st-key-divide .stButton > button:active, .st-key-multiply .stButton > button:active,
.st-key-minus  .stButton > button:active, .st-key-plus     .stButton > button:active,
.st-key-equals .stButton > button:active {
    background: var(--orange-hi) !important;
}
.st-key-equals .stButton > button {
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.3), 0 6px 20px rgba(255,159,10,0.4);
}

/* ---------- navigation: five items ---------- */
.navigation-bar { grid-template-columns: repeat(var(--nav-cols, 5), 1fr) !important; }
.navigation-link { transition: background 0.25s ease, transform 0.3s var(--spring), color 0.2s ease; }
.navigation-link:active { transform: scale(0.93); }

/* ---------- home ---------- */
.home-hero { margin: 0 0 var(--s-4) 0; }
.home-title {
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.032em;
    line-height: 1.08;
    color: var(--label);
    max-width: 22ch;
}
.home-title span { color: var(--muted); }

.portals {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    padding: 14px 0 22px 0;
}

.portal {
    --fg: #ffffff;
    --fg-soft: rgba(255,255,255,0.72);
    --accent: var(--blue-hi);
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 500px;
    padding: 28px 26px 0 26px;
    border-radius: 28px;
    overflow: hidden;
    background: #000000;
    border: 1px solid var(--hairline);
    color: var(--fg) !important;
    text-decoration: none !important;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    will-change: transform;
    transition:
        transform 0.55s var(--spring-soft),
        box-shadow 0.5s ease,
        opacity 0.4s ease,
        filter 0.4s ease;
    animation: portalIn 0.8s var(--ease-out) backwards;
    animation-delay: calc(var(--i) * 110ms);
}

.portal.light {
    --fg: #1d1d1f;
    --fg-soft: rgba(29,29,31,0.66);
    --accent: #0071e3;
    background: #f5f5f7;
}

.portal-eyebrow {
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: var(--orange);
}
.portal.light .portal-eyebrow { color: #b64400; }

.portal-title {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.08;
    margin: 8px 0 12px 0;
    color: var(--fg);
}

.portal-copy {
    font-size: 0.98rem;
    font-weight: 600;
    line-height: 1.38;
    color: var(--fg);
}
.portal-sub {
    margin-top: 6px;
    font-size: 0.95rem;
    line-height: 1.38;
    color: var(--fg-soft);
}

.portal-cta {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin-top: 16px;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--accent);
}
.portal-cta i {
    font-style: normal;
    display: inline-block;
    transition: transform 0.4s var(--spring);
}

.portal-art {
    margin-top: auto;
    padding-top: 24px;
    display: flex;
    justify-content: center;
    transition: transform 0.6s var(--spring-soft);
}

/* Calculator art */
.art-calc {
    width: 84%;
    height: 236px;
    padding: 16px 16px 0 16px;
    overflow: hidden;
    background: #1c1c1e;
    border: 1px solid var(--hairline-hi);
    border-bottom: none;
    border-radius: 28px 28px 0 0;
    box-shadow: 0 -10px 40px rgba(10,132,255,0.16);
}
.art-calc .read {
    text-align: right;
    font-size: 1.9rem;
    font-weight: 300;
    letter-spacing: -0.03em;
    padding-bottom: 12px;
}
.art-calc .keys { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.art-calc .keys i {
    font-style: normal;
    aspect-ratio: 1;
    display: grid;
    place-items: center;
    border-radius: 50%;
    font-size: 0.92rem;
    background: rgba(255,255,255,0.14);
}
.art-calc .keys i.op { background: var(--orange); }

/* Grades art */
.art-grades {
    width: 100%;
    height: 236px;
    margin-bottom: 26px;
    flex-direction: column;
    justify-content: flex-end;
}
.art-grades .gpa { font-size: 3.6rem; font-weight: 700; letter-spacing: -0.045em; line-height: 1; }
.art-grades .gpa-label { font-size: 0.86rem; color: var(--fg-soft); margin: 4px 0 16px 0; }
.art-grades .bars { display: flex; align-items: flex-end; gap: 10px; height: 104px; }
.art-grades .bars b {
    flex: 1;
    border-radius: 10px 10px 4px 4px;
    background: linear-gradient(180deg, #3d9dff, #0a84ff);
}

/* Quiz art */
.art-quiz {
    width: 100%;
    height: 236px;
    margin-bottom: 26px;
    flex-direction: column;
    justify-content: flex-end;
    gap: 10px;
}
.art-quiz .q { font-size: 1.02rem; font-weight: 600; margin-bottom: 4px; }
.art-quiz .a {
    padding: 13px 16px;
    border-radius: 14px;
    font-size: 0.92rem;
    background: rgba(255,255,255,0.11);
}
.art-quiz .a.on { background: var(--blue); }

/* The bubble: hovered card grows, its neighbours quietly step back. */
@media (hover: hover) {
    .portals:hover .portal:not(:hover) {
        opacity: 0.72;
        transform: scale(0.972);
        filter: saturate(0.8);
    }
    .portals .portal:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 34px 80px rgba(0,0,0,0.55), 0 0 0 1px var(--hairline-hi);
        z-index: 3;
    }
    .portal:hover .portal-art { transform: translateY(-8px); }
    .portal:hover .portal-cta i { transform: translateX(5px); }
}
.portal:active { transform: scale(0.975) !important; transition-duration: 0.12s; }
.portal:focus-visible { outline: none; box-shadow: 0 0 0 4px rgba(10,132,255,0.55); }

@keyframes portalIn {
    from { opacity: 0; transform: translateY(32px) scale(0.95); }
    to   { opacity: 1; transform: none; }
}

/* ---------- profile: refined login card ---------- */

.login-section-label {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 500;
    margin: 6px 0 14px 0;
}
.login-section-label::before,
.login-section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--hairline);
}

/* Age slider: recolor Streamlit's default red/orange thumb + track to blue. */
div[data-testid="stSlider"] [role="slider"] {
    background-color: var(--blue) !important;
    border-color: var(--blue) !important;
    box-shadow: 0 2px 10px rgba(10, 132, 255, 0.5) !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: var(--blue) !important;
}
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: var(--muted) !important;
}
div[data-testid="stThumbValue"] {
    color: var(--label) !important;
    background: rgba(10, 132, 255, 0.22) !important;
}
div[data-testid="stSlider"] label { color: var(--muted) !important; }

.login-avatar-wrap { position: relative; }

.login-avatar {
    width: 96px;
    height: 96px;
    font-size: 2.3rem;
    animation: avatarPop 0.5s var(--spring-soft);
}

.login-avatar-ring {
    position: absolute;
    inset: -6px;
    border-radius: 50%;
    border: 1.5px solid rgba(10, 132, 255, 0.45);
    animation: ringPulse 2.6s ease-in-out infinite;
    pointer-events: none;
}

.login-subtext.login-hint {
    margin-top: 2px;
    max-width: 26ch;
}

@keyframes avatarPop {
    from { opacity: 0; transform: scale(0.7); }
    to   { opacity: 1; transform: scale(1); }
}

@keyframes ringPulse {
    0%, 100% { opacity: 0.55; transform: scale(1); }
    50%      { opacity: 0.15; transform: scale(1.08); }
}

/* Progress ring replacing the static lock icon on the status card. */
.profile-progress-ring {
    position: relative;
    width: 72px;
    height: 72px;
    margin: 2px auto 18px auto;
    border-radius: 50%;
    background: conic-gradient(var(--blue) calc(var(--pct) * 1%), rgba(255,255,255,0.09) 0);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.5s var(--ease-out);
}
.profile-progress-ring::before {
    content: "";
    position: absolute;
    inset: 6px;
    border-radius: 50%;
    background: rgba(20, 20, 22, 0.92);
}
.profile-progress-ring span {
    position: relative;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--label);
}
.profile-progress-ring.done {
    background: var(--blue);
}
.profile-progress-ring.done svg {
    position: relative;
    width: 26px;
    height: 26px;
    color: #ffffff;
}

.profile-gate-checklist { width: 100%; max-width: 230px; margin: 0 auto; }

.profile-gate-row svg { transition: transform 0.2s ease; }
.profile-gate-row.done svg { animation: checkPop 0.4s var(--spring); }

@keyframes checkPop {
    from { transform: scale(0.4); }
    to   { transform: scale(1); }
}

/* ---------- tablet ---------- */
@media (min-width: 769px) and (max-width: 1099px) {
    .home-title { font-size: 2.2rem; }
    .portal { min-height: 470px; padding: 24px 20px 0 20px; }
    .portal-title { font-size: 1.6rem; }
}

/* ---------- mobile ---------- */
@media (max-width: 768px) {
    :root { --s-4: 18px; --s-5: 28px; --s-6: 44px; }

    .block-container { padding: 20px 14px 72px 14px !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { padding: var(--s-3) !important; }

    .navigation-link { font-size: 0.66rem !important; padding: 9px 1px !important; }

    .home-title { font-size: 1.9rem; }

    /* Swipeable carousel, like the App Store. */
    .portals {
        display: flex;
        gap: 14px;
        margin: 0 -14px;
        padding: 10px 14px 24px 14px;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }
    .portals::-webkit-scrollbar { display: none; }
    .portal { flex: 0 0 80%; min-height: 450px; scroll-snap-align: center; }
    .portal-title { font-size: 1.75rem; }
}

@media (max-width: 420px) {
    .navigation-link { font-size: 0.6rem !important; }
    .portal { flex-basis: 84%; }
}

</style>
""",
    unsafe_allow_html=True,
)

# Haptic tick on every button / portal press (Android; iOS ignores vibrate).
components.html(
    """
<script>
(function () {
    const doc = window.parent.document;
    if (doc.__feelV1) return;
    doc.__feelV1 = true;
    doc.addEventListener('pointerdown', function (e) {
        const hit = e.target && e.target.closest ? e.target.closest('button, a.portal') : null;
        const nav = window.parent.navigator;
        if (hit && !hit.disabled && nav.vibrate) nav.vibrate(hit.matches('a.portal') ? 12 : 8);
    }, true);
})();
</script>
""",
    height=0,
)


# ==========================================================
# NAVIGATION
# ==========================================================


def nav_link(anchor_id, label):
    """A normal scroll link once unlocked; a plain, unclickable label until then."""
    if st.session_state.profile_complete:
        return f'<a class="navigation-link" href="#{anchor_id}" data-smooth="{anchor_id}">{label}</a>'
    return f'<span class="navigation-link navigation-link-locked">{label}</span>'


# Once signed in, the Profile section is gone from the page entirely, so
# its nav item goes with it — the segmented control just shifts to 4 items.
profile_nav_item = (
    ""
    if st.session_state.profile_complete
    else '<a class="navigation-link" href="#profile" data-smooth="profile">Profile</a>'
)
nav_column_count = 4 if st.session_state.profile_complete else 5

nav_items = "".join(
    item
    for item in (
        profile_nav_item,
        nav_link("home", "Home"),
        nav_link("calculator", "Calculator"),
        nav_link("grading", "Grades"),
        nav_link("quiz-maker", "Quiz"),
    )
    if item
)

# Built as one unindented line on purpose: Streamlit's markdown renderer
# treats a run of lines indented 4+ spaces as a preformatted code block,
# and an empty (whitespace-only) line — which profile_nav_item produces
# once signed in — is exactly what triggers that. A single flat line of
# HTML never qualifies, so it always renders as markup, not literal text.
st.markdown(
    f'<div class="brand-mark">Essentials</div>'
    f'<div class="navigation-bar" style="--nav-cols:{nav_column_count}">{nav_items}</div>',
    unsafe_allow_html=True,
)



# Streamlit scrolls a different element depending on browser and screen size:
# sometimes the window, sometimes an inner <section>. Rather than guessing,
# this probes each ancestor to find the one that actually moves the target,
# then animates scrollTop itself — so the easing is identical everywhere.
components.html(
    """
<script>
(function () {
    const doc = window.parent.document;
    const win = window.parent;

    if (doc.__smoothNavVersion === 5) return;
    doc.__smoothNavVersion = 5;

    const OFFSET = 100;
    const DURATION = 620;

    /* Deliberate motion, not ambient motion: a clicked nav link is a
       direct request for this specific transition, which is a different
       thing from the auto-playing effects reduce-motion is meant to
       suppress. So this always animates, unaffected by that OS setting. */
    const easeInOutCubic = (t) =>
        t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

    /* Temporarily disable CSS smooth scrolling so our own easing isn't fought. */
    function withInstantScroll(element, work) {
        const previous = element.style.scrollBehavior;
        element.style.setProperty('scroll-behavior', 'auto', 'important');
        const outcome = work();
        element.style.scrollBehavior = previous;
        return outcome;
    }

    /* Probe every ancestor: whichever one actually moves the target is the
       real scroll container. Streamlit uses different ones on desktop,
       mobile, and inside embeds, so guessing by CSS overflow is unreliable.
       If nothing in the ancestor chain qualifies, the page-level scroller
       is always returned as a guaranteed fallback — better to attempt a
       scroll on the wrong element than to silently do nothing. */
    function findScroller(target) {
        let node = target.parentElement;

        while (node) {
            if (node.scrollHeight - node.clientHeight > 4) {
                const moved = withInstantScroll(node, function () {
                    const startTop = node.scrollTop;
                    const before = target.getBoundingClientRect().top;
                    node.scrollTop = startTop + 2;
                    const shifted = Math.abs(target.getBoundingClientRect().top - before) > 0.5;
                    node.scrollTop = startTop;
                    return shifted;
                });

                if (moved) return node;
            }
            node = node.parentElement;
        }

        return doc.scrollingElement || doc.documentElement || doc.body;
    }

    function tween(read, write, distance, done) {
        const start = read();
        const startTime = win.performance.now();

        function frame(now) {
            const progress = Math.min((now - startTime) / DURATION, 1);
            write(start + distance * easeInOutCubic(progress));
            if (progress < 1) {
                win.requestAnimationFrame(frame);
            } else if (done) {
                done();
            }
        }

        win.requestAnimationFrame(frame);
    }

    /* Always drive the scroll by hand rather than delegating to the browser's
       own smooth-scroll (via CSS or scrollIntoView): when the OS has reduce
       motion turned on, browsers silently clamp *any* author-requested smooth
       scroll to an instant jump, no matter what behavior is passed in JS. A
       manual rAF tween that sets scrollTop directly isn't subject to that
       clamp, so it's the only way to guarantee an animation when asked for. */
    function manualScroll(target) {
        const scroller = findScroller(target);
        const root = doc.scrollingElement || doc.documentElement;
        const usesWindow = scroller === root || scroller === doc.documentElement || scroller === doc.body;

        const distance = usesWindow
            ? target.getBoundingClientRect().top - OFFSET
            : target.getBoundingClientRect().top - scroller.getBoundingClientRect().top - OFFSET;

        if (Math.abs(distance) < 1) return;

        const previous = scroller.style.scrollBehavior;
        scroller.style.setProperty('scroll-behavior', 'auto', 'important');
        const restore = () => { scroller.style.scrollBehavior = previous; };

        if (usesWindow) {
            tween(() => win.scrollY, (value) => win.scrollTo(0, value), distance, restore);
        } else {
            tween(
                () => scroller.scrollTop,
                (value) => { scroller.scrollTop = value; },
                distance,
                restore
            );
        }
    }

    function scrollToTarget(target) {
        manualScroll(target);
    }

    doc.addEventListener('click', function (event) {
        const link = event.target && event.target.closest
            ? event.target.closest('a[data-smooth]')
            : null;

        if (!link) return;

        const target = doc.getElementById(link.getAttribute('data-smooth'));
        if (!target) return;

        event.preventDefault();
        scrollToTarget(target);
    }, true);
})();
</script>
""",
    height=0,
)


st.markdown(
    """
<style>
.profile-login-shell{width:min(920px,94vw);height:calc(100vh - 105px);min-height:560px;max-height:720px;margin:0 auto;display:grid;grid-template-columns:48% 52%;overflow:hidden;border-radius:28px;border:1px solid rgba(255,255,255,.14);background:rgba(13,16,23,.86);box-shadow:0 28px 80px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,255,255,.08);backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px)}
.profile-brand-panel{position:relative;display:flex;flex-direction:column;min-width:0;padding:30px 32px 25px;overflow:hidden;background:radial-gradient(circle at 20% 15%,rgba(61,157,255,.25),transparent 45%),radial-gradient(circle at 80% 85%,rgba(10,132,255,.13),transparent 50%),rgba(255,255,255,.025);border-right:1px solid rgba(255,255,255,.10)}
.profile-brand{display:flex;align-items:center;gap:10px;color:#fff;font-size:1.08rem;font-weight:700;position:relative;z-index:2}.profile-brand-mark{width:34px;height:34px;display:grid;place-items:center;border-radius:10px;background:linear-gradient(145deg,#3d9dff,#0a84ff);box-shadow:0 8px 24px rgba(10,132,255,.35)}
.profile-brand-copy{position:relative;z-index:2;margin:auto 0 0;max-width:355px}.profile-brand-kicker{color:#64b1ff;font-size:.68rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;margin-bottom:9px}.profile-brand-title{color:#fff;font-size:clamp(2rem,3.4vw,3rem);font-weight:750;letter-spacing:-.045em;line-height:.98;margin-bottom:12px}.profile-brand-text{color:rgba(235,235,245,.64);font-size:.88rem;line-height:1.45;max-width:34ch}
.profile-picture{width:100%;max-width:360px;height:245px;object-fit:contain;display:block;margin:8px auto -3px;filter:drop-shadow(0 18px 28px rgba(0,0,0,.28))}
.profile-brand-footer{position:relative;z-index:2;color:rgba(235,235,245,.36);font-size:.68rem;margin-top:auto}
.profile-form-panel{display:flex;flex-direction:column;justify-content:center;padding:36px 46px;min-width:0}.profile-form-heading{margin-bottom:18px}.profile-form-heading h2{color:#fff!important;font-size:1.9rem!important;font-weight:700!important;letter-spacing:-.035em!important;margin:0 0 5px!important}.profile-form-heading p{color:rgba(235,235,245,.52)!important;font-size:.82rem;margin:0}
.profile-form-panel .stTextInput{margin-bottom:7px}.profile-form-panel .stTextInput label,.profile-form-panel .stSlider label{color:rgba(235,235,245,.58)!important;font-size:.72rem!important;font-weight:600!important}.profile-form-panel .stTextInput input{height:43px;background:rgba(255,255,255,.055)!important;border:1px solid rgba(255,255,255,.14)!important;border-radius:11px!important;color:#fff!important;font-size:.86rem!important}.profile-form-panel .stTextInput input::placeholder{color:rgba(235,235,245,.30)!important}.profile-form-panel .stSlider{margin:1px 0 3px}.profile-form-panel .stButton>button{min-height:45px!important;border-radius:12px!important;margin-top:5px}.profile-form-panel .stButton>button[kind="primary"]{background:linear-gradient(180deg,#3d9dff,#0a84ff)!important;border:0!important}.profile-progress-mini{display:flex;align-items:center;gap:9px;margin:5px 0 13px;color:rgba(235,235,245,.38);font-size:.68rem}.profile-progress-line{flex:1;height:3px;overflow:hidden;border-radius:99px;background:rgba(255,255,255,.08)}.profile-progress-line span{display:block;height:100%;border-radius:inherit;background:linear-gradient(90deg,#0a84ff,#64b1ff)}
@media(max-width:768px){.profile-login-shell{width:94vw;height:calc(100vh - 82px);min-height:560px;max-height:none;grid-template-columns:1fr;grid-template-rows:39% 61%;border-radius:22px}.profile-brand-panel{padding:19px 21px 15px;border-right:0;border-bottom:1px solid rgba(255,255,255,.1)}.profile-brand-copy{margin:auto 0 0}.profile-brand-title{font-size:1.65rem}.profile-brand-text{font-size:.76rem;max-width:30ch}.profile-picture{position:absolute;width:190px;height:150px;right:-15px;bottom:-8px;margin:0;opacity:.9}.profile-brand-footer{display:none}.profile-form-panel{padding:20px 21px;justify-content:center}.profile-form-heading{margin-bottom:10px}.profile-form-heading h2{font-size:1.55rem!important}.profile-form-panel .stTextInput input{height:40px}.profile-progress-mini{margin-bottom:7px}}
@media(max-width:420px){.profile-login-shell{grid-template-rows:36% 64%;height:calc(100vh - 72px)}.profile-brand-panel{padding:17px 17px 12px}.profile-brand-kicker{font-size:.6rem}.profile-brand-title{font-size:1.42rem}.profile-brand-text{font-size:.69rem}.profile-picture{width:155px;height:125px;right:-10px}.profile-form-panel{padding:16px 17px}.profile-form-heading h2{font-size:1.35rem!important}.profile-form-panel .stTextInput{margin-bottom:3px}.profile-form-panel .stTextInput input{height:37px;font-size:.8rem!important}.profile-form-panel .stTextInput label,.profile-form-panel .stSlider label{font-size:.65rem!important}.profile-form-panel .stButton>button{min-height:40px!important}}
</style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# PROFILE
# (only shown before sign-in — hidden from view once complete)
# ==========================================================

if "profile_name" not in st.session_state:
    st.session_state.profile_name = ""

if not st.session_state.profile_complete:
    st.markdown('<div id="profile" class="section-anchor"></div>', unsafe_allow_html=True)

    profile_picture = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MjAgNDIwIj4KPGRlZnM+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJiZyIgeDE9IjAiIHkxPSIwIiB4Mj0iMSIgeTI9IjEiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzE3MzY1ZiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzBiMTQyNCIvPjwvbGluZWFyR3JhZGllbnQ+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJzaGlydCIgeDE9IjAiIHkxPSIwIiB4Mj0iMSIgeTI9IjEiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVmYjJmZiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzBhODRmZiIvPjwvbGluZWFyR3JhZGllbnQ+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJkZXNrIiB4MT0iMCIgeTE9IjAiIHgyPSIxIiB5Mj0iMCI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMjQ0NzZlIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMTAyNDNjIi8+PC9saW5lYXJHcmFkaWVudD4KICA8ZmlsdGVyIGlkPSJzaGFkb3ciPjxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjEwIi8+PC9maWx0ZXI+CjwvZGVmcz4KPGVsbGlwc2UgY3g9IjI2MCIgY3k9IjM4MCIgcng9IjE5MCIgcnk9IjI0IiBmaWxsPSIjMDAwIiBvcGFjaXR5PSIuMjgiIGZpbHRlcj0idXJsKCNzaGFkb3cpIi8+CjxjaXJjbGUgY3g9IjI2NSIgY3k9IjE4NCIgcj0iMTUwIiBmaWxsPSJ1cmwoI2JnKSIgb3BhY2l0eT0iLjk1Ii8+CjxjaXJjbGUgY3g9IjM1NSIgY3k9IjEwNSIgcj0iNDYiIGZpbGw9IiMzZDlkZmYiIG9wYWNpdHk9Ii4xMiIvPgo8Y2lyY2xlIGN4PSIxMjUiIGN5PSIyNzUiIHI9IjM0IiBmaWxsPSIjMGE4NGZmIiBvcGFjaXR5PSIuMTIiLz4KPCEtLSBmbG9hdGluZyBjYXJkcyAtLT4KPHJlY3QgeD0iNjAiIHk9IjkyIiB3aWR0aD0iMTA0IiBoZWlnaHQ9IjY2IiByeD0iMTQiIGZpbGw9IiNmZmYiIG9wYWNpdHk9Ii4wOSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utb3BhY2l0eT0iLjEyIi8+CjxyZWN0IHg9Ijc2IiB5PSIxMTAiIHdpZHRoPSI1MCIgaGVpZ2h0PSI3IiByeD0iNCIgZmlsbD0iIzY0YjFmZiIgb3BhY2l0eT0iLjkiLz4KPHJlY3QgeD0iNzYiIHk9IjEyNiIgd2lkdGg9IjcyIiBoZWlnaHQ9IjYiIHJ4PSIzIiBmaWxsPSIjZmZmIiBvcGFjaXR5PSIuMjUiLz4KPHJlY3QgeD0iNzYiIHk9IjE0MSIgd2lkdGg9IjQzIiBoZWlnaHQ9IjYiIHJ4PSIzIiBmaWxsPSIjZmZmIiBvcGFjaXR5PSIuMTYiLz4KPHJlY3QgeD0iMzYwIiB5PSIyMTUiIHdpZHRoPSIxMDIiIGhlaWdodD0iNzQiIHJ4PSIxNiIgZmlsbD0iI2ZmZiIgb3BhY2l0eT0iLjA4IiBzdHJva2U9IiNmZmYiIHN0cm9rZS1vcGFjaXR5PSIuMTIiLz4KPHBhdGggZD0iTTM3OCAyNjYgTDM3OCAyNDcgTDM5NSAyNTcgTDQxMCAyMzUgTDQyNSAyNDkgTDQ0NiAyMjUiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzY0YjFmZiIgc3Ryb2tlLXdpZHRoPSI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPCEtLSBwZXJzb24gLS0+CjxjaXJjbGUgY3g9IjI1NyIgY3k9IjEyMiIgcj0iMzkiIGZpbGw9IiNmMWIxOGQiLz4KPHBhdGggZD0iTTIxOCAxMTkgUTIyMCA3NyAyNjEgNzYgUTI5NiA3OSAyOTggMTEzIFEyODAgOTggMjYxIDEwMCBRMjQwIDEwMyAyMTggMTE5WiIgZmlsbD0iIzIwMjczNSIvPgo8cGF0aCBkPSJNMjE5IDExOSBRMjEwIDEyNSAyMTEgMTQ0IFEyMzAgMTMyIDI0MiAxMjVaIiBmaWxsPSIjMjAyNzM1Ii8+CjxjaXJjbGUgY3g9IjI0MiIgY3k9IjEyNSIgcj0iNCIgZmlsbD0iIzFiMjMzMCIvPjxjaXJjbGUgY3g9IjI3NSIgY3k9IjEyNSIgcj0iNCIgZmlsbD0iIzFiMjMzMCIvPgo8cGF0aCBkPSJNMjUwIDE0MyBRMjYwIDE1MCAyNzAgMTQzIiBmaWxsPSJub25lIiBzdHJva2U9IiNiNjZmNjIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjwhLS0gYm9keSAtLT4KPHBhdGggZD0iTTE5NiAyMTkgUTIwNyAxNzUgMjU0IDE3NCBRMzAxIDE3NSAzMTkgMjE5IEwzMDAgMjgzIEwyMTQgMjgzWiIgZmlsbD0idXJsKCNzaGlydCkiLz4KPHBhdGggZD0iTTIzMCAxODEgUTI1NyAyMDUgMjgzIDE4MSBMMjg5IDIyMSBRMjU4IDIzNiAyMjQgMjIxWiIgZmlsbD0iI2Q5ZWZmZiIgb3BhY2l0eT0iLjkiLz4KPCEtLSBhcm1zIHR5cGluZyAtLT4KPHBhdGggZD0iTTIxNSAyMTcgUTE4OCAyMzEgMTc3IDI2MyBRMTc2IDI3MiAxODYgMjc2IFExOTUgMjc5IDIwMSAyNjkgTDIyOSAyNDIiIGZpbGw9IiNmMWIxOGQiLz4KPHBhdGggZD0iTTMwMiAyMTcgUTMyOCAyMzIgMzQwIDI2MCBRMzQzIDI2OSAzMzQgMjc0IFEzMjQgMjc4IDMxNyAyNjggTDI4OCAyNDEiIGZpbGw9IiNmMWIxOGQiLz4KPCEtLSBsYXB0b3AgLS0+CjxwYXRoIGQ9Ik0yMDIgMjQ4IEwzMTggMjQ4IEwzMzMgMzA0IEwxODggMzA0WiIgZmlsbD0iI2JjZDlmNSIgb3BhY2l0eT0iLjk1Ii8+CjxyZWN0IHg9IjIxNCIgeT0iMjU3IiB3aWR0aD0iOTIiIGhlaWdodD0iMzQiIHJ4PSI0IiBmaWxsPSIjMGQxZDMxIi8+CjxjaXJjbGUgY3g9IjI2MCIgY3k9IjI3NCIgcj0iOCIgZmlsbD0iIzNkOWRmZiIgb3BhY2l0eT0iLjgiLz4KPHBhdGggZD0iTTE3NyAzMDQgTDM0MiAzMDQgTDM2NSAzMjIgTDE1NSAzMjJaIiBmaWxsPSJ1cmwoI2Rlc2spIi8+CjwhLS0gYm9va3MgLS0+CjxyZWN0IHg9IjkxIiB5PSIzMTMiIHdpZHRoPSI5NCIgaGVpZ2h0PSIxNiIgcng9IjUiIGZpbGw9IiMwYTg0ZmYiIG9wYWNpdHk9Ii44IiB0cmFuc2Zvcm09InJvdGF0ZSgtNyA5MSAzMTMpIi8+CjxyZWN0IHg9IjEwNSIgeT0iMzI5IiB3aWR0aD0iODQiIGhlaWdodD0iMTMiIHJ4PSI1IiBmaWxsPSIjNjRiMWZmIiBvcGFjaXR5PSIuNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTcgMTA1IDMyOSkiLz4KPCEtLSBsaXR0bGUgc3BhcmtsZXMgLS0+CjxwYXRoIGQ9Ik0zOTAgODggdjI0IE0zNzggMTAwIGgyNCIgc3Ryb2tlPSIjNjRiMWZmIiBzdHJva2Utd2lkdGg9IjQiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNMTE2IDIwMSB2MTYgTTEwOCAyMDkgaDE2IiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBvcGFjaXR5PSIuNSIvPgo8L3N2Zz4="

    st.markdown(
        textwrap.dedent(f"""
        <div class="profile-login-shell">
            <div class="profile-brand-panel">
                <div class="profile-brand">
                    <div class="profile-brand-mark">✦</div>
                    <span>Essentials</span>
                </div>
                <div class="profile-brand-copy">
                    <div class="profile-brand-kicker">Student workspace</div>
                    <div class="profile-brand-title">Everything you need, in one place.</div>
                    <div class="profile-brand-text">
                        Set up your profile to unlock your calculator, grades, and quiz tools.
                    </div>
                    <img class="profile-picture" src="{profile_picture}" alt="Student using Essentials" />
                </div>
                <div class="profile-brand-footer">Your information stays in this session.</div>
            </div>
            <div class="profile-form-panel">
                <div class="profile-form-heading">
                    <h2>Welcome to Essentials</h2>
                    <p>Complete your student profile to continue.</p>
                </div>
        """),
        unsafe_allow_html=True,
    )

    # Compact two-column fields keep the whole login/profile experience on one screen.
    c1, c2 = st.columns(2, gap="small")
    with c1:
        name = st.text_input("Name", placeholder="Your name")
    with c2:
        school = st.text_input("School", placeholder="Your school")

    c3, c4 = st.columns(2, gap="small")
    with c3:
        age = st.slider("Age", min_value=5, max_value=100, value=16)
    with c4:
        favorite_subject = st.text_input("Favorite subject", placeholder="e.g. Science")

    hobby = st.text_input("Favorite hobby", placeholder="e.g. Chess")
    trimmed_name = name.strip()

    required_fields = [
        bool(trimmed_name),
        bool(school.strip()),
        bool(favorite_subject.strip()),
        bool(hobby.strip()),
    ]
    done_count = sum(required_fields)
    all_filled = done_count == 4
    pct = round(done_count / 4 * 100)

    st.markdown(
        textwrap.dedent(f"""
        <div class="profile-progress-mini">
            <span>Profile setup</span>
            <div class="profile-progress-line"><span style="width:{pct}%"></span></div>
            <span>{done_count}/4</span>
        </div>
        """),
        unsafe_allow_html=True,
    )

    continue_clicked = st.button("Continue", use_container_width=True, type="primary", disabled=not all_filled)

    st.markdown('</div></div>', unsafe_allow_html=True)

    @st.dialog("Profile ready")
    def show_profile_popup():
        safe_name = _escape(name.strip())
        safe_school = _escape(school.strip())
        safe_subject = _escape(favorite_subject.strip())
        safe_hobby = _escape(hobby.strip())

        st.markdown(
            textwrap.dedent(f"""
            <div class="profile-success-card">
                <div class="profile-success-art">
                    <img src="{profile_picture}" alt="Essentials student illustration" />
                    <div class="profile-success-check" aria-hidden="true">
                        <svg viewBox="0 0 24 24">
                            <path d="M5 12.5 9.5 17 19 7.5" />
                        </svg>
                    </div>
                </div>

                <div class="profile-success-kicker">Essentials • Profile ready</div>
                <div class="profile-success-title">Welcome, {safe_name}!</div>
                <div class="profile-success-text">
                    Your student workspace is ready. Everything is set up and waiting for you.
                </div>

                <div class="profile-success-details">
                    <div class="profile-success-detail">
                        <span>School</span>
                        <strong>{safe_school}</strong>
                    </div>
                    <div class="profile-success-detail">
                        <span>Age</span>
                        <strong>{age} years old</strong>
                    </div>
                    <div class="profile-success-detail">
                        <span>Favorite subject</span>
                        <strong>{safe_subject}</strong>
                    </div>
                    <div class="profile-success-detail">
                        <span>Favorite hobby</span>
                        <strong>{safe_hobby}</strong>
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        if st.button("Enter Essentials", use_container_width=True, type="primary"):
            st.rerun()

    if continue_clicked:
        st.session_state.profile_name = trimmed_name
        st.session_state.profile_complete = True
        show_profile_popup()

    st.stop()

trimmed_name = st.session_state.profile_name


# ==========================================================
# HOME  (Apple-style portal grid, shown right after login)
# ==========================================================

st.markdown('<div id="home" class="section-anchor"></div>', unsafe_allow_html=True)

_who = _escape(trimmed_name) if trimmed_name else "there"

_calc_keys = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−"]
_calc_art = (
    '<div class="portal-art"><div class="art-calc"><div class="read">1,024</div><div class="keys">'
    + "".join(f'<i class="{"op" if n % 4 == 3 else ""}">{k}</i>' for n, k in enumerate(_calc_keys))
    + "</div></div></div>"
)
_grades_art = (
    '<div class="portal-art art-grades"><div class="gpa">3.82</div>'
    '<div class="gpa-label">Overall GPA</div><div class="bars">'
    + "".join(f'<b style="height:{h}%"></b>' for h in (44, 62, 52, 78, 94))
    + "</div></div>"
)
_quiz_art = (
    '<div class="portal-art art-quiz"><div class="q">Which planet is closest to the Sun?</div>'
    '<div class="a">A. Venus</div><div class="a on">B. Mercury</div><div class="a">C. Mars</div></div>'
)


def _portal(i, href, eyebrow, title, copy, sub, art, light=False):
    return (
        f'<a class="portal{" light" if light else ""}" href="#{href}" data-smooth="{href}" style="--i:{i}">'
        f'<div class="portal-eyebrow">{eyebrow}</div>'
        f'<div class="portal-title">{title}</div>'
        f'<div class="portal-copy">{copy}</div>'
        f'<div class="portal-sub">{sub}</div>'
        f'<div class="portal-cta">Open <i>›</i></div>'
        f"{art}</a>"
    )


st.markdown(
    f'<div class="home-hero"><div class="home-title">Welcome, {_who}. '
    f"<span>Pick where to go next.</span></div></div>"
    '<div class="portals">'
    + _portal(0, "calculator", "Scientific", "Calculator",
              "Sums, roots, sin, cos and log in one keypad.",
              "Results pop up in a clean sheet.", _calc_art)
    + _portal(1, "grading", "Weighted GPA", "Grades",
              "Turn scores and attendance into your GPA.",
              "70% score, 30% attendance.", _grades_art, light=True)
    + _portal(2, "quiz-maker", "Your questions", "Quiz",
              "Write your own questions, then take the test.",
              "Instant score when you finish.", _quiz_art)
    + "</div>",
    unsafe_allow_html=True,
)

if not st.session_state.get("home_seen"):
    st.session_state.home_seen = True
    components.html(
        """
<script>
setTimeout(function () {
    const el = window.parent.document.getElementById('home');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}, 350);
</script>
""",
        height=0,
    )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)


# ==========================================================
# CALCULATOR
# ==========================================================

st.markdown('<div id="calculator" class="section-anchor"></div>', unsafe_allow_html=True)
st.markdown("---")

st.title("Calculator")
st.markdown(
    '<p class="lede">Build an expression with the keypad, then press equals.</p>',
    unsafe_allow_html=True,
)

if "calc_display" not in st.session_state:
    st.session_state.calc_display = ""

if "calc_result" not in st.session_state:
    st.session_state.calc_result = ""


def add_to_calculator(value):
    st.session_state.calc_display += value
    st.session_state.calc_result = ""


def clear_calculator():
    st.session_state.calc_display = ""
    st.session_state.calc_result = ""


def backspace_calculator():
    st.session_state.calc_display = st.session_state.calc_display[:-1]
    st.session_state.calc_result = ""


def calculate_result():
    expression = st.session_state.calc_display

    if not expression:
        return

    allowed = {
        "sqrt": math.sqrt,
        "sin": lambda degrees: math.sin(math.radians(degrees)),
        "cos": lambda degrees: math.cos(math.radians(degrees)),
        "tan": lambda degrees: math.tan(math.radians(degrees)),
        "log": math.log10,
        "ln": math.log,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        result = eval(expression, {"__builtins__": {}}, allowed)

        if isinstance(result, float):
            result = str(int(result)) if result.is_integer() else str(round(result, 10))
        else:
            result = str(result)

        st.session_state.calc_result = result

    except ZeroDivisionError:
        st.session_state.calc_result = "Can't divide by zero"

    except Exception:
        st.session_state.calc_result = "Check the expression"


@st.dialog("Result")
def show_calculator_result():
    st.markdown(
        f'<p class="lede" style="margin-bottom:10px">{st.session_state.calc_display}</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:26px 18px;
            font-size:44px;
            font-weight:300;
            letter-spacing:-0.03em;
            color:#ffffff;
            background:rgba(255,255,255,0.06);
            border:1px solid rgba(255,255,255,0.12);
            border-radius:20px;
            margin:0 0 22px 0;
            word-break:break-all;
            animation:resultPop 0.4s cubic-bezier(0.32,0.72,0,1);
        ">{st.session_state.calc_result}</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Done", use_container_width=True, type="primary"):
        st.session_state.calc_result = ""
        st.rerun()


readout = st.session_state.calc_display or '<span class="placeholder">0</span>'
st.markdown(
    f'<div class="calc-readout calc-shell">{readout}</div>',
    unsafe_allow_html=True,
)


calculator_rows = [
    [("7", "seven", "7"), ("8", "eight", "8"), ("9", "nine", "9"), ("÷", "divide", "/")],
    [("4", "four", "4"), ("5", "five", "5"), ("6", "six", "6"), ("×", "multiply", "*")],
    [("1", "one", "1"), ("2", "two", "2"), ("3", "three", "3"), ("−", "minus", "-")],
    [("0", "zero", "0"), (".", "decimal", "."), ("(", "left_paren", "("), ("+", "plus", "+")],
    [(")", "right_paren", ")"), ("⌫", "backspace", None), ("C", "clear", None), ("=", "equals", None)],
]

with st.container(key="calc_keys"):
    for row_index, row in enumerate(calculator_rows):
        columns = st.columns(4, gap="small")

        for column, (label, key, value) in zip(columns, row):
            with column:
                if key == "backspace":
                    st.button(label, key=key, use_container_width=True, on_click=backspace_calculator)
                elif key == "clear":
                    st.button(label, key=key, use_container_width=True, on_click=clear_calculator)
                elif key == "equals":
                    st.button(label, key=key, use_container_width=True, on_click=calculate_result)
                else:
                    st.button(
                        label,
                        key=key,
                        use_container_width=True,
                        on_click=add_to_calculator,
                        args=(value,),
                    )

st.markdown("---")
st.subheader("Scientific functions")

scientific_rows = [
    [("√", "sqrt", "sqrt("), ("sin", "sin", "sin("), ("cos", "cos", "cos("), ("tan", "tan", "tan(")],
    [("log", "log", "log("), ("ln", "ln", "ln("), ("π", "pi", "pi"), ("e", "e", "e")],
]

with st.container(key="sci_keys"):
    for row in scientific_rows:
        columns = st.columns(4, gap="small")

        for column, (label, key, value) in zip(columns, row):
            with column:
                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=add_to_calculator,
                    args=(value,),
                )

if st.session_state.calc_result:
    show_calculator_result()


st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)


# ==========================================================
# GRADE CALCULATOR
# ==========================================================

st.markdown('<div id="grading" class="section-anchor"></div>', unsafe_allow_html=True)
st.markdown("---")

st.title("Grades")
st.markdown(
    '<p class="lede">Your GPA from subject scores, weights, and attendance. '
    'Each subject counts as 70% score and 30% attendance.</p>',
    unsafe_allow_html=True,
)

DEFAULT_SUBJECTS = ["Mathematics", "Science", "English"]
DEFAULT_WEIGHTS = {"Mathematics": 6, "Science": 4, "English": 5}

if "grade_subjects" not in st.session_state:
    st.session_state.grade_subjects = list(DEFAULT_SUBJECTS)

if "subject_weights" not in st.session_state:
    st.session_state.subject_weights = dict(DEFAULT_WEIGHTS)

# Holds the last computed GPA/breakdown so it survives reruns triggered by
# *other* widgets on the page (typing in the quiz section, etc). It is the
# single source of truth for what gets rendered below, and Reset clears it
# explicitly so a stale result can never linger after a reset.
if "grade_results" not in st.session_state:
    st.session_state.grade_results = None


def get_letter_grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def get_grade_points(letter):
    return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}[letter]


def get_gpa_message(gpa):
    if gpa >= 3.5:
        return "success", "Outstanding work. Keep it up."
    if gpa >= 3.0:
        return "success", "Great results. Keep pushing."
    if gpa >= 2.0:
        return "info", "Solid effort. There's room to climb."
    if gpa >= 1.0:
        return "warning", "Keep studying — steady progress adds up."
    return "error", "Plenty of room to improve. Start with one subject."


scores = {}
weights = {}
attendance = {}

for subject_name in st.session_state.grade_subjects:
    with st.container(border=True):
        st.subheader(subject_name)

        col1, col2, col3 = st.columns(3)

        with col1:
            scores[subject_name] = st.number_input(
                "Score out of 100",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                key=f"grade_score_{subject_name}",
            )

        with col2:
            attendance[subject_name] = st.number_input(
                "Classes attended of 10",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key=f"attendance_{subject_name}",
            )

        with col3:
            weights[subject_name] = st.number_input(
                "Subject weight",
                min_value=1,
                max_value=20,
                value=st.session_state.subject_weights.get(subject_name, 1),
                step=1,
                key=f"weight_{subject_name}",
            )

            st.session_state.subject_weights[subject_name] = weights[subject_name]


col1, col2 = st.columns([3, 1])

with col1:
    new_subject = st.text_input(
        "Subject name",
        placeholder="Add a subject, for example History",
        label_visibility="collapsed",
    )

with col2:
    add_subject = st.button("Add subject", use_container_width=True)

if add_subject:
    cleaned_subject = new_subject.strip()

    if not cleaned_subject:
        st.warning("Enter a subject name first.")
    elif cleaned_subject in st.session_state.grade_subjects:
        st.warning("That subject is already on the list.")
    else:
        st.session_state.grade_subjects.append(cleaned_subject)
        st.session_state.subject_weights[cleaned_subject] = 1
        st.rerun()


# Calculate / Reset

st.markdown("---")


def reset_grade_calculator():
    st.session_state.grade_subjects = list(DEFAULT_SUBJECTS)
    st.session_state.subject_weights = dict(DEFAULT_WEIGHTS)

    # Clear every per-subject widget's stored value (scores, attendance,
    # weights for both default AND any custom subjects that were added),
    # so the widgets fall back to their `value=` defaults on the next run
    # instead of keeping whatever the user last typed.
    keys_to_remove = [
        key
        for key in list(st.session_state.keys())
        if key.startswith("grade_score_")
        or key.startswith("attendance_")
        or key.startswith("weight_")
    ]

    for key in keys_to_remove:
        del st.session_state[key]

    # Wipe the last calculated GPA/breakdown too, so nothing stale is left
    # showing once the reset completes.
    st.session_state.grade_results = None


col1, col2 = st.columns(2)

with col1:
    calculate = st.button(
        "🧮 Calculate GPA",
        use_container_width=True,
    )

with col2:
    st.button(
        "↻ Reset Everything",
        use_container_width=True,
        on_click=reset_grade_calculator,
    )

if calculate:
    total_weighted_gpa = 0
    total_weights = 0
    results = []

    for subject_name in st.session_state.grade_subjects:
        score = scores[subject_name]
        classes_attended = attendance[subject_name]
        weight = weights[subject_name]

        attendance_percentage = (classes_attended / 10) * 100
        final_subject_score = (score * 0.70) + (attendance_percentage * 0.30)

        letter = get_letter_grade(final_subject_score)
        points = get_grade_points(letter)

        total_weighted_gpa += points * weight
        total_weights += weight

        results.append(
            {
                "subject": subject_name,
                "score": score,
                "classes_attended": classes_attended,
                "attendance_percentage": attendance_percentage,
                "final_score": final_subject_score,
                "letter": letter,
                "points": points,
                "weight": weight,
            }
        )

    final_gpa = total_weighted_gpa / total_weights if total_weights else 0.0

    # Store the whole computed result in session_state (instead of using it
    # straight from local variables) so it renders consistently below and
    # keeps showing across unrelated reruns, until Reset explicitly clears it.
    st.session_state.grade_results = {
        "final_gpa": final_gpa,
        "results": results,
    }

if st.session_state.grade_results:
    final_gpa = st.session_state.grade_results["final_gpa"]
    results = st.session_state.grade_results["results"]

    st.markdown("---")

    with st.container(border=True):
        st.metric(label="Overall GPA", value=f"{final_gpa:.2f}", delta=None)
        st.markdown(
            '<p class="lede" style="margin:0">out of 4.00</p>',
            unsafe_allow_html=True,
        )

    st.subheader("Subject breakdown")

    for index, result in enumerate(results):
        with st.container(key=f"result_{index}", border=True):
            st.subheader(f"{result['subject']} — {result['letter']}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"Score — **{result['score']}/100**")
                st.write(f"Classes attended — **{result['classes_attended']}/10**")
                st.write(f"Attendance — **{result['attendance_percentage']:.0f}%**")

            with col2:
                st.write(f"Final score — **{result['final_score']:.2f}%**")
                st.write(f"Subject weight — **{result['weight']}**")
                st.write(f"GPA points — **{result['points']:.1f}**")

    message_kind, message_text = get_gpa_message(final_gpa)
    getattr(st, message_kind)(message_text)


st.markdown("---")
st.subheader("Grading scale")

st.table(
    {
        "Grade": ["A", "B", "C", "D", "F"],
        "Range": ["90–100%", "80–89%", "70–79%", "60–69%", "0–59%"],
        "Meaning": [
            "Outstanding",
            "Above average",
            "Satisfactory",
            "Minimum passing",
            "Failing",
        ],
        "Points": ["4.0", "3.0", "2.0", "1.0", "0.0"],
    }
)


st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)


# ==========================================================
# QUIZ
# ==========================================================

st.markdown('<div id="quiz-maker" class="section-anchor"></div>', unsafe_allow_html=True)
st.markdown("---")

st.title("Quiz")
st.markdown(
    '<p class="lede">Write your own questions, then take the quiz.</p>',
    unsafe_allow_html=True,
)

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}


if st.button("Add question", use_container_width=True):
    # A stable id keeps each widget tied to its own question, so removing
    # one in the middle no longer shifts text into the wrong boxes.
    st.session_state.quiz_questions.append(
        {"id": uuid4().hex[:8], "question": "", "A": "", "B": "", "C": "", "D": "", "correct": "A"}
    )
    st.rerun()


if not st.session_state.quiz_questions:
    st.markdown(
        '<p class="lede">No questions yet. Add one to get started.</p>',
        unsafe_allow_html=True,
    )

remove_index = None

for i, question in enumerate(st.session_state.quiz_questions):
    qid = question["id"]

    with st.container(border=True):
        st.subheader(f"Question {i + 1}")

        question["question"] = st.text_input(
            "Question",
            value=question["question"],
            placeholder="What would you like to ask?",
            key=f"quiz_question_{qid}",
        )

        col1, col2 = st.columns(2)

        for offset, letter in enumerate(["A", "B", "C", "D"]):
            with col1 if offset < 2 else col2:
                question[letter] = st.text_input(
                    f"Choice {letter}",
                    value=question[letter],
                    placeholder=f"Choice {letter}",
                    key=f"quiz_choice_{letter}_{qid}",
                )

        question["correct"] = st.selectbox(
            "Correct answer",
            ["A", "B", "C", "D"],
            index=["A", "B", "C", "D"].index(question["correct"]),
            key=f"quiz_correct_{qid}",
        )

        if st.button("Remove question", key=f"remove_quiz_{qid}", use_container_width=True):
            remove_index = i

if remove_index is not None:
    st.session_state.quiz_questions.pop(remove_index)
    st.rerun()


if st.session_state.quiz_questions:
    st.markdown("---")

    quiz_ready = all(
        question["question"].strip()
        and all(question[letter].strip() for letter in ["A", "B", "C", "D"])
        for question in st.session_state.quiz_questions
    )

    if not quiz_ready:
        st.warning("Every question needs a title and all four choices filled in.")

    if st.button(
        f"Start quiz — {len(st.session_state.quiz_questions)} question(s)",
        use_container_width=True,
        type="primary",
        disabled=not quiz_ready,
    ):
        st.session_state.quiz_started = True
        st.session_state.quiz_finished = False
        st.session_state.quiz_answers = {}
        st.rerun()


if st.session_state.quiz_started and st.session_state.quiz_questions:
    st.markdown("---")
    st.subheader("Take the quiz")

    for i, question in enumerate(st.session_state.quiz_questions):
        with st.container(border=True):
            st.subheader(f"{i + 1}. {question['question']}")

            choices = [f"{letter}. {question[letter]}" for letter in ["A", "B", "C", "D"]]

            selected = st.radio(
                "Choose your answer",
                choices,
                index=None,
                key=f"quiz_answer_{question['id']}",
            )

            st.session_state.quiz_answers[i] = selected[0] if selected else None

    if st.button("Submit quiz", use_container_width=True, type="primary"):
        unanswered = [
            i + 1
            for i in range(len(st.session_state.quiz_questions))
            if st.session_state.quiz_answers.get(i) is None
        ]

        if unanswered:
            st.warning(
                "Answer question "
                + ", ".join(str(number) for number in unanswered)
                + " before submitting."
            )
        else:
            score = sum(
                1
                for i, question in enumerate(st.session_state.quiz_questions)
                if st.session_state.quiz_answers.get(i) == question["correct"]
            )

            total = len(st.session_state.quiz_questions)

            st.session_state.quiz_score = score
            st.session_state.quiz_total = total
            st.session_state.quiz_percentage = (score / total) * 100
            st.session_state.quiz_finished = True
            st.session_state.quiz_started = False
            st.rerun()


if st.session_state.quiz_finished:

    @st.dialog("Quiz complete")
    def show_quiz_result():
        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        percentage = st.session_state.quiz_percentage

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Score", f"{score}/{total}")

        with col2:
            st.metric("Percentage", f"{percentage:.0f}%")

        st.markdown("---")

        if percentage == 100:
            st.success("Perfect score — every answer correct.")
        elif percentage >= 80:
            st.success("Excellent work.")
        elif percentage >= 60:
            st.info("Good job. Keep practising.")
        elif percentage >= 40:
            st.warning("Getting there — review and try again.")
        else:
            st.error("Worth another run through the material.")

        st.markdown("---")

        if st.button("Done", use_container_width=True, type="primary"):
            st.session_state.quiz_finished = False
            st.session_state.quiz_answers = {}
            st.rerun()

    show_quiz_result()
