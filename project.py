import base64
import math
import os
from uuid import uuid4

import streamlit as st
import streamlit.components.v1 as components

# ==========================================================
# PAGE CONFIG
# Must be the first Streamlit call, and may only run ONCE.
# ==========================================================

st.set_page_config(
    page_title="My Profile & Grade Calculator",
    page_icon="🎓",
    layout="centered",
)


APP_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(APP_DIR, "background.mp4")


# ==========================================================
# BLURRED VIDEO BACKGROUND
# ==========================================================

@st.cache_data(show_spinner=False)
def load_background_video(path):
    """Return the video as base64, or None if the file is missing."""
    try:
        with open(path, "rb") as video_file:
            return base64.b64encode(video_file.read()).decode()
    except OSError:
        return None


video_base64 = load_background_video(VIDEO_PATH)

if video_base64:
    background_html = f"""
    <div class="custom-background">
        <video autoplay muted loop playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
    </div>
    <div class="background-overlay"></div>
    """
else:
    # Graceful fallback so the app still runs without background.mp4
    background_html = """
    <div class="custom-background fallback"></div>
    <div class="background-overlay"></div>
    """

st.markdown(background_html, unsafe_allow_html=True)


# ==========================================================
# THEME + LAYOUT
# One stylesheet, organised top to bottom:
# tokens → background → typography → cards → controls
# → table → navigation → motion → responsive
# ==========================================================

st.markdown(
    """
<style>

/* ---------- tokens ---------- */
:root {
    --text: #f5f5f7;
    --text-soft: rgba(245, 245, 247, 0.78);
    --glass: rgba(26, 26, 30, 0.72);
    --glass-strong: rgba(22, 22, 26, 0.88);
    --line: rgba(255, 255, 255, 0.14);
    --line-strong: rgba(255, 255, 255, 0.30);
    --radius-lg: 22px;
    --radius-md: 14px;
    --radius-sm: 12px;
    --shadow: 0 16px 40px rgba(0, 0, 0, 0.32);
    --nav-offset: 120px;
}

/* ---------- background ---------- */
.stApp {
    background: #101014 !important;
    color: var(--text);
}

.custom-background {
    position: fixed;
    inset: 0;
    z-index: -10;
    overflow: hidden;
}

.custom-background.fallback {
    background:
        radial-gradient(120% 90% at 15% 0%, #2b3550 0%, transparent 60%),
        radial-gradient(110% 90% at 90% 100%, #3a2b4a 0%, transparent 60%),
        #101014;
}

.custom-background video {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* The blur is what lets text sit cleanly on top. */
    filter: blur(14px) saturate(1.05) brightness(0.9);
    /* Scale up so blurred edges never show. */
    transform: translate(-50%, -50%) scale(1.14);
}

.background-overlay {
    position: fixed;
    inset: 0;
    z-index: -9;
    background:
        linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.38) 45%, rgba(0,0,0,0.62) 100%);
}

/* ---------- typography ---------- */
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: -0.6px;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.55);
}

p, label, li, .stMarkdown, .stText, .stCaption {
    color: var(--text) !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.45);
}

/* ---------- layout container ---------- */
.block-container {
    width: min(94vw, 1080px) !important;
    max-width: 1080px !important;
    margin: 0 auto !important;
    padding: 40px 24px 72px 24px !important;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    overflow-x: hidden !important;
}

/* ---------- glass cards ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--glass) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    padding: 14px !important;
    margin-bottom: 14px !important;
    box-shadow: var(--shadow);
}

/* ---------- inputs ---------- */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(30, 30, 34, 0.86) !important;
    color: #ffffff !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md) !important;
    font-size: 16px !important;
}

.stTextInput input,
.stNumberInput input {
    padding: 12px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--line-strong) !important;
    outline: 2px solid rgba(255, 255, 255, 0.22) !important;
    outline-offset: 1px;
}

/* ---------- buttons ---------- */
.stButton > button {
    background: rgba(42, 42, 46, 0.92) !important;
    color: #ffffff !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md) !important;
    min-height: 48px;
    font-weight: 600 !important;
    transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover {
    background: rgba(68, 68, 74, 0.96) !important;
    border-color: var(--line-strong) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.34);
}

.stButton > button:focus-visible {
    outline: 2px solid #ffffff !important;
    outline-offset: 2px;
}

.stButton > button:disabled {
    opacity: 0.45 !important;
    transform: none !important;
}

/* ---------- alerts + metrics ---------- */
.stAlert {
    background: var(--glass) !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(16px);
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* ---------- grading table ---------- */
div[data-testid="stTable"] table {
    font-size: 18px !important;
    background: var(--glass-strong) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}

div[data-testid="stTable"] th {
    color: #ffffff !important;
    background: rgba(56, 56, 62, 0.96) !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    padding: 14px 12px !important;
}

div[data-testid="stTable"] td {
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 13px 12px !important;
    background: rgba(34, 34, 38, 0.94) !important;
}

div[data-testid="stTable"] tr {
    border-bottom: 1px solid var(--line) !important;
}

/* ---------- dividers + spacing ---------- */
hr {
    border: none !important;
    border-top: 1px solid var(--line) !important;
    margin: 28px 0 !important;
}

.section-gap {
    height: 10vh;
    min-height: 56px;
}

/* ---------- smooth scrolling ---------- */
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.block-container {
    scroll-behavior: smooth !important;
    scroll-padding-top: var(--nav-offset) !important;
}

.section-anchor {
    display: block;
    height: 1px;
    scroll-margin-top: var(--nav-offset) !important;
}

/* ---------- navigation ---------- */
.navigation-bar {
    position: sticky;
    top: 8px;
    z-index: 999;
    background: rgba(22, 22, 26, 0.82);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 10px;
    margin-bottom: 28px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.38);
}

.navigation-title {
    text-align: center;
    color: var(--text-soft);
    font-weight: 700;
    font-size: 12px;
    margin-bottom: 9px;
}

.navigation-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
}

.navigation-link {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    text-decoration: none !important;
    color: #ffffff !important;
    background: rgba(56, 56, 62, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: var(--radius-sm);
    padding: 11px 6px;
    min-height: 42px;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.15;
    transition: background 0.2s ease, transform 0.2s ease;
}

.navigation-link:hover {
    background: rgba(82, 82, 90, 0.96);
    transform: translateY(-2px);
}

.navigation-link:focus-visible {
    outline: 2px solid #ffffff;
    outline-offset: 2px;
}

/* ---------- motion ---------- */
@keyframes profilePopup {
    0%   { opacity: 0; transform: scale(0.84) translateY(28px); }
    70%  { opacity: 1; transform: scale(1.02) translateY(-2px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes resultPop {
    0%   { opacity: 0; transform: scale(0.8); }
    65%  { opacity: 1; transform: scale(1.05); }
    100% { opacity: 1; transform: scale(1); }
}

[data-testid="stDialog"] {
    animation: profilePopup 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

[data-testid="stDialog"] > div {
    background: rgba(24, 24, 28, 0.97) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 26px !important;
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.7) !important;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* ---------- chrome ---------- */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

/* ==========================================================
   RESPONSIVE
   ========================================================== */

/* Desktop */
@media (min-width: 1100px) {
    .block-container { padding-top: 52px !important; padding-bottom: 84px !important; }
    h1 { font-size: 2.85rem !important; }
    h2 { font-size: 1.95rem !important; }
    h3 { font-size: 1.32rem !important; }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1099px) {
    .block-container { width: min(94vw, 900px) !important; padding-left: 20px !important; padding-right: 20px !important; }
}

/* Phone */
@media (max-width: 768px) {
    :root { --nav-offset: 96px; }

    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 18px 12px 48px 12px !important;
    }

    .custom-background video { filter: blur(10px) saturate(1.05) brightness(0.88); }

    h1 { font-size: 1.95rem !important; line-height: 1.14 !important; margin-bottom: 0.4rem !important; }
    h2 { font-size: 1.4rem !important; line-height: 1.2 !important; }
    h3 { font-size: 1.1rem !important; }
    p, label, .stMarkdown, .stText, .stCaption { font-size: 0.95rem !important; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
    }

    /* Keep calculator keys in a 4-across grid instead of wrapping. */
    .stHorizontalBlock:has(.stButton) {
        flex-wrap: nowrap !important;
        gap: 6px !important;
    }

    .stHorizontalBlock:has(.stButton) > div {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }

    .stHorizontalBlock:has(.stButton) .stButton,
    .stHorizontalBlock:has(.stButton) .stButton > button {
        width: 100% !important;
    }

    .stButton > button {
        min-height: 44px !important;
        padding: 8px 4px !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.92rem !important;
    }

    .stTextInput input,
    .stNumberInput input {
        min-height: 44px !important;
        font-size: 16px !important;
    }

    .navigation-bar { top: 6px !important; padding: 7px !important; margin-bottom: 20px !important; border-radius: 15px !important; }
    .navigation-title { font-size: 11px !important; margin-bottom: 6px !important; }
    .navigation-grid { gap: 6px !important; }
    .navigation-link { font-size: 11px !important; padding: 9px 2px !important; min-height: 38px !important; }

    div[data-testid="stTable"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    div[data-testid="stTable"] table { min-width: 540px !important; font-size: 15px !important; }
    div[data-testid="stTable"] th { font-size: 14px !important; padding: 11px 10px !important; }
    div[data-testid="stTable"] td { font-size: 14px !important; padding: 10px !important; }

    .section-gap { height: 6vh; min-height: 32px; }

    [data-testid="stDialog"] > div {
        width: calc(100vw - 24px) !important;
        max-width: calc(100vw - 24px) !important;
        border-radius: 22px !important;
    }
}

/* Small phones */
@media (max-width: 420px) {
    .block-container { padding-left: 9px !important; padding-right: 9px !important; }
    .navigation-link { font-size: 10px !important; padding-left: 1px !important; padding-right: 1px !important; }
    .stButton > button { font-size: 0.84rem !important; min-height: 42px !important; }
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# NAVIGATION
# ==========================================================

st.markdown(
    """
<div class="navigation-bar">
    <div class="navigation-title">Jump to a section</div>
    <div class="navigation-grid">
        <a class="navigation-link" href="#profile" data-smooth="profile">👤 Profile</a>
        <a class="navigation-link" href="#calculator" data-smooth="calculator">🧮 Calculator</a>
        <a class="navigation-link" href="#grading" data-smooth="grading">🎓 Grading</a>
        <a class="navigation-link" href="#quiz-maker" data-smooth="quiz-maker">🧠 Quiz</a>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# CSS `scroll-behavior` alone is unreliable inside Streamlit, because the
# element that actually scrolls is a nested container rather than <html>.
# This listener finds the real scrolling parent and animates to the target.
components.html(
    """
<script>
(function () {
    const doc = window.parent.document;
    if (doc.__smoothNavReady) return;
    doc.__smoothNavReady = true;

    function scrollableParent(el) {
        let node = el.parentElement;
        while (node) {
            const style = window.parent.getComputedStyle(node);
            const scrolls = /(auto|scroll|overlay)/.test(style.overflowY);
            if (scrolls && node.scrollHeight > node.clientHeight + 4) return node;
            node = node.parentElement;
        }
        return doc.scrollingElement || doc.documentElement;
    }

    doc.addEventListener('click', function (event) {
        const link = event.target.closest('a[data-smooth]');
        if (!link) return;

        const target = doc.getElementById(link.getAttribute('data-smooth'));
        if (!target) return;

        event.preventDefault();

        const reduce = window.parent.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const container = scrollableParent(target);
        const offset = 110;

        if (container === doc.scrollingElement || container === doc.documentElement) {
            const top = target.getBoundingClientRect().top + window.parent.scrollY - offset;
            window.parent.scrollTo({ top: top, behavior: reduce ? 'auto' : 'smooth' });
        } else {
            const top =
                target.getBoundingClientRect().top -
                container.getBoundingClientRect().top +
                container.scrollTop -
                offset;
            container.scrollTo({ top: top, behavior: reduce ? 'auto' : 'smooth' });
        }
    }, true);
})();
</script>
""",
    height=0,
)


# ==========================================================
# PROFILE
# ==========================================================

st.markdown('<div id="profile" class="section-anchor"></div>', unsafe_allow_html=True)

st.title("👋 My Profile")
st.write("Fill in the details below to create your profile.")

name = st.text_input("👤 What is your name?")
age = st.number_input("🎂 How old are you?", min_value=1, max_value=100, step=1)
school = st.text_input("🏫 What school do you go to?")
favorite_subject = st.text_input("📚 What is your favorite subject?")
hobby = st.text_input("🎨 What is your favorite hobby?")


@st.dialog("🎉 Profile created")
def show_profile_popup():
    st.subheader(f"Welcome, {name}! 👋")
    st.write("Here's a little bit about you.")
    st.markdown("---")
    st.write(f"👤 **Name:** {name}")
    st.write(f"🎂 **Age:** {age} years old")
    st.write(f"🏫 **School:** {school}")
    st.write(f"📚 **Favorite subject:** {favorite_subject}")
    st.write(f"🎨 **Favorite hobby:** {hobby}")
    st.markdown("---")
    st.success(f"Your profile is ready, {name}. 🎓")

    if st.button("✨ Done", use_container_width=True):
        st.rerun()


if st.button("✨ Create my profile", use_container_width=True):
    if name and school and favorite_subject and hobby:
        show_profile_popup()
    else:
        st.warning("Fill in every field to create your profile.")


st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)


# ==========================================================
# SCIENTIFIC CALCULATOR
# ==========================================================

st.markdown('<div id="calculator" class="section-anchor"></div>', unsafe_allow_html=True)
st.markdown("---")

st.title("🧮 Scientific Calculator")
st.write("Tap the keys to build an expression, then press `=`.")

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
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
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


@st.dialog("🧮 Result")
def show_calculator_result():
    st.write("Expression")
    st.code(st.session_state.calc_display, language=None)

    st.markdown("---")

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:20px;
            font-size:40px;
            font-weight:700;
            color:#ffffff;
            background:rgba(45,45,50,0.85);
            border-radius:20px;
            margin:8px 0 22px 0;
            animation:resultPop 0.45s ease-out;
        ">{st.session_state.calc_result}</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("✓ Done", use_container_width=True):
        st.session_state.calc_result = ""
        st.rerun()


st.text_input(
    "Calculator display",
    value=st.session_state.calc_display,
    disabled=True,
    label_visibility="collapsed",
)

calculator_rows = [
    [("7", "seven", "7"), ("8", "eight", "8"), ("9", "nine", "9"), ("÷", "divide", "/")],
    [("4", "four", "4"), ("5", "five", "5"), ("6", "six", "6"), ("×", "multiply", "*")],
    [("1", "one", "1"), ("2", "two", "2"), ("3", "three", "3"), ("−", "minus", "-")],
    [("0", "zero", "0"), (".", "decimal", "."), ("(", "left_paren", "("), ("+", "plus", "+")],
    [(")", "right_paren", ")"), ("⌫", "backspace", None), ("C", "clear", None), ("=", "equals", None)],
]

for row in calculator_rows:
    columns = st.columns(4)

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
st.subheader("🔬 Scientific functions")

scientific_rows = [
    [("√", "sqrt", "sqrt("), ("sin", "sin", "sin("), ("cos", "cos", "cos("), ("tan", "tan", "tan(")],
    [("log", "log", "log("), ("ln", "ln", "ln("), ("π", "pi", "pi"), ("e", "e", "e")],
]

for row in scientific_rows:
    columns = st.columns(4)

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

st.title("🎓 Grade Calculator")
st.write("Work out your GPA from subject scores, weights, and class attendance.")

DEFAULT_SUBJECTS = ["Mathematics", "Science", "English"]
DEFAULT_WEIGHTS = {"Mathematics": 6, "Science": 4, "English": 5}

if "grade_subjects" not in st.session_state:
    st.session_state.grade_subjects = list(DEFAULT_SUBJECTS)

if "subject_weights" not in st.session_state:
    st.session_state.subject_weights = dict(DEFAULT_WEIGHTS)


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


st.subheader("📝 Enter your scores")
st.write("Each subject counts as **70% score + 30% attendance**.")

scores = {}
weights = {}
attendance = {}

for subject_name in st.session_state.grade_subjects:
    with st.container(border=True):
        st.subheader(f"📚 {subject_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            scores[subject_name] = st.number_input(
                "Score / 100",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                key=f"grade_score_{subject_name}",
            )

        with col2:
            attendance[subject_name] = st.number_input(
                "Classes attended",
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


st.markdown("---")
st.subheader("➕ Add another subject")

col1, col2 = st.columns([3, 1])

with col1:
    new_subject = st.text_input(
        "Subject name",
        placeholder="Example: History",
        label_visibility="collapsed",
    )

with col2:
    add_subject = st.button("➕ Add", use_container_width=True)

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


st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    calculate = st.button("🧮 Calculate GPA", use_container_width=True)

with col2:
    reset = st.button("↻ Reset everything", use_container_width=True)


if reset:
    st.session_state.grade_subjects = list(DEFAULT_SUBJECTS)
    st.session_state.subject_weights = dict(DEFAULT_WEIGHTS)

    for key in list(st.session_state.keys()):
        if key.startswith(("grade_score_", "attendance_", "weight_")):
            del st.session_state[key]

    st.rerun()


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

    st.markdown("---")

    with st.container(border=True):
        st.subheader("🎓 Your results")
        st.metric(label="Overall GPA", value=f"{final_gpa:.2f} / 4.00")

    st.subheader("📊 Subject breakdown")

    for index, result in enumerate(results):
        with st.container(key=f"result_{index}", border=True):
            st.subheader(f"📚 {result['subject']}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"📝 Original score: **{result['score']}/100**")
                st.write(f"🏫 Classes attended: **{result['classes_attended']}/10**")
                st.write(f"📅 Attendance: **{result['attendance_percentage']:.0f}%**")

            with col2:
                st.write(f"🎯 Final score: **{result['final_score']:.2f}%**")
                st.write(f"⚖️ Subject weight: **{result['weight']}**")
                st.write(f"🎓 GPA points: **{result['points']:.1f}**")

            st.write(f"### Grade: **{result['letter']}**")

    st.subheader("🧮 How your grade is worked out")

    with st.container(border=True):
        st.write("📝 **Subject score counts for 70%**")
        st.write("🏫 **Attendance counts for 30%**")
        st.write("🎯 **Final subject score = (score × 70%) + (attendance × 30%)**")

    st.subheader("🏫 Attendance summary")

    for result in results:
        st.write(
            f"**{result['subject']}:** {result['classes_attended']}/10 classes "
            f"({result['attendance_percentage']:.0f}%)"
        )

    if final_gpa >= 3.5:
        st.success("🏆 Outstanding work. Keep it up!")
    elif final_gpa >= 3.0:
        st.success("🌟 Great results. Keep pushing!")
    elif final_gpa >= 2.0:
        st.info("👍 Solid effort. There's room to climb.")
    elif final_gpa >= 1.0:
        st.warning("📖 Keep studying — steady progress adds up.")
    else:
        st.error("💪 Plenty of room to improve. Start with one subject.")


# ==========================================================
# GRADING SCALE
# ==========================================================

st.markdown("---")
st.subheader("📚 Grading scale")

st.table(
    {
        "Letter grade": ["A", "B", "C", "D", "F"],
        "Percentage range": ["90% – 100%", "80% – 89%", "70% – 79%", "60% – 69%", "0% – 59%"],
        "Description": [
            "Outstanding",
            "Above average",
            "Satisfactory",
            "Minimum passing",
            "Failing",
        ],
        "GPA points": ["4.0", "3.0", "2.0", "1.0", "0.0"],
    }
)


st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)


# ==========================================================
# QUIZ MAKER
# ==========================================================

st.markdown('<div id="quiz-maker" class="section-anchor"></div>', unsafe_allow_html=True)
st.markdown("---")

st.title("🧠 Quiz Master")
st.write("Build a quiz with as many questions as you like, then take it.")

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}


st.subheader("✏️ Build your quiz")

if st.button("➕ Add question", use_container_width=True):
    # A stable id keeps each widget tied to its own question, so removing
    # one in the middle no longer shuffles the text into the wrong boxes.
    st.session_state.quiz_questions.append(
        {"id": uuid4().hex[:8], "question": "", "A": "", "B": "", "C": "", "D": "", "correct": "A"}
    )
    st.rerun()


remove_index = None

for i, question in enumerate(st.session_state.quiz_questions):
    qid = question["id"]

    with st.container(border=True):
        st.subheader(f"Question {i + 1}")

        question["question"] = st.text_input(
            "❓ Question",
            value=question["question"],
            placeholder="Type your question...",
            key=f"quiz_question_{qid}",
        )

        for letter in ["A", "B", "C", "D"]:
            question[letter] = st.text_input(
                f"Choice {letter}",
                value=question[letter],
                placeholder=f"Enter choice {letter}",
                key=f"quiz_choice_{letter}_{qid}",
            )

        question["correct"] = st.selectbox(
            "✅ Correct answer",
            ["A", "B", "C", "D"],
            index=["A", "B", "C", "D"].index(question["correct"]),
            key=f"quiz_correct_{qid}",
        )

        if st.button("🗑️ Remove question", key=f"remove_quiz_{qid}", use_container_width=True):
            remove_index = i

if remove_index is not None:
    st.session_state.quiz_questions.pop(remove_index)
    st.rerun()


if st.session_state.quiz_questions:
    st.markdown("---")
    st.write(f"📋 **{len(st.session_state.quiz_questions)} question(s) ready**")

    quiz_ready = all(
        question["question"].strip()
        and all(question[letter].strip() for letter in ["A", "B", "C", "D"])
        for question in st.session_state.quiz_questions
    )

    if not quiz_ready:
        st.warning("Every question needs a title and all four choices filled in.")

    if st.button("▶️ Start quiz", use_container_width=True, disabled=not quiz_ready):
        st.session_state.quiz_started = True
        st.session_state.quiz_finished = False
        st.session_state.quiz_answers = {}
        st.rerun()


if st.session_state.quiz_started and st.session_state.quiz_questions:
    st.markdown("---")
    st.title("📝 Take the quiz")
    st.write("Pick one answer for every question.")

    for i, question in enumerate(st.session_state.quiz_questions):
        with st.container(border=True):
            st.subheader(f"{i + 1}. {question['question']}")

            choices = [f"{letter}. {question[letter]}" for letter in ["A", "B", "C", "D"]]

            selected = st.radio(
                "Choose your answer:",
                choices,
                index=None,
                key=f"quiz_answer_{question['id']}",
            )

            st.session_state.quiz_answers[i] = selected[0] if selected else None

    if st.button("🎯 Submit quiz", use_container_width=True):
        unanswered = [
            i + 1 for i in range(len(st.session_state.quiz_questions))
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

    @st.dialog("🎉 Quiz complete")
    def show_quiz_result():
        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        percentage = st.session_state.quiz_percentage

        st.subheader("Your results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🏆 Score", f"{score} / {total}")

        with col2:
            st.metric("📊 Percentage", f"{percentage:.0f}%")

        st.markdown("---")

        if percentage == 100:
            st.success("🏆 Perfect score — every answer correct!")
        elif percentage >= 80:
            st.success("🌟 Excellent work.")
        elif percentage >= 60:
            st.info("👍 Good job. Keep practising.")
        elif percentage >= 40:
            st.warning("📚 Getting there — review and try again.")
        else:
            st.error("💪 Worth another run through the material.")

        st.markdown("---")

        if st.button("✓ Done", use_container_width=True):
            st.session_state.quiz_finished = False
            st.session_state.quiz_answers = {}
            st.rerun()

    show_quiz_result()
