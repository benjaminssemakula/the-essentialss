import streamlit as st
import os
import base64
import math

# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Executive Suite | Profile & Grade Calculator",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# CUSTOM LIVE VIDEO BACKGROUND & CANVAS RESET
# ==========================================================

video_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "background.mp4"
)

video_base64 = ""
if os.path.exists(video_path):
    with open(video_path, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode()

st.markdown(
    f"""
    <style>
    /* Global Canvas Reset */
    .stApp {{
        background: #0b0c10 !important;
        color: #f1f5f9;
    }}

    /* Fixed Background Video */
    .custom-background {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -10;
        overflow: hidden;
    }}

    .custom-background video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.5) contrast(1.1);
    }}

    /* Frosted Gradient Overlay */
    .background-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: radial-gradient(circle at 50% 20%, rgba(15, 23, 42, 0.5) 0%, rgba(2, 6, 23, 0.9) 100%);
        z-index: -9;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }}
    </style>

    {"<div class='custom-background'><video autoplay muted loop playsinline><source src='data:video/mp4;base64," + video_base64 + "' type='video/mp4'></video></div>" if video_base64 else ""}
    <div class="background-overlay"></div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# EXECUTIVE DESIGN SYSTEM & STYLING
# ==========================================================

st.markdown("""
<style>
/* Layout Constraints */
.block-container {
    width: min(92vw, 1200px) !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding-top: 24px !important;
    padding-bottom: 80px !important;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    overflow-x: hidden !important;
    scroll-behavior: smooth !important;
    scroll-padding-top: 100px !important;
}

/* Typography Hierarchy */
h1, h2, h3, h4 {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif !important;
    letter-spacing: -0.025em !important;
}

.corporate-gradient-text {
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Micro-Badges */
.corporate-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #38bdf8;
    margin-bottom: 8px;
    text-transform: uppercase;
}

/* Executive Navigation Bar */
.navigation-bar {
    position: sticky;
    top: 15px;
    z-index: 999;
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 10px 14px;
    margin-bottom: 36px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.navigation-title {
    text-align: center;
    color: #64748b;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.14em;
    margin-bottom: 8px;
}

.navigation-link {
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
    color: #e2e8f0 !important;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 6px;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.navigation-link:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    color: #ffffff !important;
}

/* Custom Executive Cards */
.profile-card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.35);
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.profile-card:hover {
    border-color: rgba(255, 255, 255, 0.22);
}

.avatar-container {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    box-shadow: 0 10px 20px rgba(2, 132, 199, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.25);
}

/* Streamlit Input Modernization */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #94a3b8 !important;
    margin-bottom: 6px !important;
}

.stTextInput input, .stNumberInput input {
    background: rgba(15, 23, 42, 0.7) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
}

/* Streamlit Button Modernization */
.stButton > button {
    background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.03) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 14px !important;
    min-height: 48px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(180deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.08) 100%) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4) !important;
}

/* Container Border Overrides for Native Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 23, 42, 0.65) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 20px !important;
    padding: 12px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

/* Tables & Grading Scale */
div[data-testid="stTable"] table {
    font-size: 15px !important;
    background: rgba(15, 23, 42, 0.75) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

div[data-testid="stTable"] th {
    color: #f8fafc !important;
    background: rgba(30, 41, 59, 0.9) !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 14px 16px !important;
}

div[data-testid="stTable"] td {
    color: #cbd5e1 !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}

/* Modal Dialog Modernization */
[data-testid="stDialog"] > div {
    background: rgba(15, 23, 42, 0.96) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 26px !important;
    box-shadow: 0 40px 100px rgba(0, 0, 0, 0.8) !important;
}

/* Section Anchors & Spacers */
.section-anchor {
    scroll-margin-top: 110px;
}

.section-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin: 40px 0;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    .profile-card {
        padding: 20px;
    }

    .navigation-bar {
        padding: 6px;
    }

    .navigation-link {
        font-size: 11px;
        padding: 8px 2px;
    }

    .stHorizontalBlock:has(.stButton) {
        flex-wrap: nowrap !important;
        gap: 6px !important;
    }

    .stHorizontalBlock:has(.stButton) > div {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }

    .stButton > button {
        min-height: 42px !important;
        font-size: 0.88rem !important;
        padding: 6px 2px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Hide default Streamlit chrome
st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# NAVIGATION BAR
# ==========================================================

st.markdown("""
<div class="navigation-bar">
    <div class="navigation-title">EXECUTIVE SUITE</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">
        <a class="navigation-link" href="#profile">👤 Profile</a>
        <a class="navigation-link" href="#calculator">🧮 Calculator</a>
        <a class="navigation-link" href="#grading">🎓 Grading</a>
        <a class="navigation-link" href="#quiz-maker">🧠 Quiz Master</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# 1. PROFILE SECTION
# ==========================================================

st.markdown('<div id="profile" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px;">
    <span class="corporate-badge">ACCOUNT OVERVIEW</span>
    <h1 class="corporate-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Executive Profile</h1>
    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Configure your academic identity and personal credentials.</p>
</div>
""", unsafe_allow_html=True)

input_col, preview_col = st.columns([1.1, 0.9], gap="large")

with input_col:
    with st.container():
        name = st.text_input("Full Name", value="Alex Mercer", placeholder="e.g. John Doe")
        
        col_age, col_school = st.columns([1, 2])
        with col_age:
            age = st.number_input("Age", min_value=1, max_value=100, value=20, step=1)
        with col_school:
            school = st.text_input("Institution", value="Stanford University", placeholder="University / School")
            
        favorite_subject = st.text_input("Primary Focus", value="Computer Science", placeholder="e.g. Physics")
        hobby = st.text_input("Specialization / Interest", value="Algorithmic Trading", placeholder="e.g. Photography")

with preview_col:
    st.markdown("<p style='font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#94a3b8; margin-bottom:10px;'>Live Card Preview</p>", unsafe_allow_html=True)
    
    initials = "".join([part[0].upper() for part in name.split()[:2]]) if name.strip() else "EX"
    
    st.markdown(f"""
    <div class="profile-card">
        <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 24px;">
            <div class="avatar-container">{initials}</div>
            <div>
                <h3 style="margin: 0; font-size: 1.3rem; color: #ffffff;">{name if name else "Your Name"}</h3>
                <p style="margin: 2px 0 0 0; color: #38bdf8; font-size: 0.88rem; font-weight: 600;">{school if school else "Institution Name"}</p>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 18px;">
            <div>
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Age Record</span>
                <p style="margin: 4px 0 0 0; font-weight: 600; color: #e2e8f0;">{age} yrs old</p>
            </div>
            <div>
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Focus Area</span>
                <p style="margin: 4px 0 0 0; font-weight: 600; color: #e2e8f0;">{favorite_subject if favorite_subject else "N/A"}</p>
            </div>
        </div>
        
        <div style="margin-top: 14px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px;">
            <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Secondary Interest</span>
            <p style="margin: 4px 0 0 0; font-weight: 600; color: #e2e8f0;">{hobby if hobby else "N/A"}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


@st.dialog("Credentials Finalized")
def show_profile_popup():
    st.markdown(f"""
    <div style="text-align: center; padding: 10px 0;">
        <div class="avatar-container" style="margin: 0 auto 16px auto;">{initials}</div>
        <h2 style="margin: 0; color: #ffffff;">{name}</h2>
        <p style="color: #38bdf8; font-weight: 600; margin-top: 4px;">{school}</p>
    </div>
    <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 16px; border: 1px solid rgba(255,255,255,0.08); margin: 20px 0;">
        <p style="margin: 6px 0; color: #cbd5e1;">👤 <strong>Name:</strong> {name}</p>
        <p style="margin: 6px 0; color: #cbd5e1;">🎂 <strong>Age:</strong> {age} years old</p>
        <p style="margin: 6px 0; color: #cbd5e1;">🏫 <strong>Institution:</strong> {school}</p>
        <p style="margin: 6px 0; color: #cbd5e1;">📚 <strong>Primary Focus:</strong> {favorite_subject}</p>
        <p style="margin: 6px 0; color: #cbd5e1;">🎨 <strong>Interest:</strong> {hobby}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Confirm Record", use_container_width=True):
        st.rerun()


st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

if st.button("✨ Save Profile Record", use_container_width=True):
    if name and school and favorite_subject and hobby:
        show_profile_popup()
    else:
        st.warning("Please complete all profile fields first.")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ==========================================================
# 2. SCIENTIFIC CALCULATOR
# ==========================================================

st.markdown('<div id="calculator" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px;">
    <span class="corporate-badge">COMPUTATIONAL TOOL</span>
    <h1 class="corporate-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Scientific Calculator</h1>
    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Perform basic and advanced mathematical calculations.</p>
</div>
""", unsafe_allow_html=True)

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

    try:
        allowed = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e
        }
        result = eval(expression, {"__builtins__": {}}, allowed)

        if isinstance(result, float):
            if result.is_integer():
                result = str(int(result))
            else:
                result = str(round(result, 10))
        else:
            result = str(result)

        st.session_state.calc_result = result
    except ZeroDivisionError:
        st.session_state.calc_result = "Error: Cannot divide by zero"
    except Exception:
        st.session_state.calc_result = "Error: Invalid expression"


@st.dialog("Calculation Output")
def show_calculator_result():
    st.markdown("<p style='font-size:12px; color:#94a3b8; text-transform:uppercase; font-weight:700;'>Submitted Expression</p>", unsafe_allow_html=True)
    st.code(st.session_state.calc_display, language=None)
    
    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:24px;
            font-size:36px;
            font-weight:800;
            color:#ffffff;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 20px;
            margin: 16px 0 24px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        ">
            {st.session_state.calc_result}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("✓ Dismiss", use_container_width=True):
        st.session_state.calc_result = ""
        st.rerun()


calc_col, sci_col = st.columns([1.2, 0.8], gap="large")

with calc_col:
    st.text_input(
        "Display",
        value=st.session_state.calc_display if st.session_state.calc_display else "0",
        disabled=True,
        label_visibility="collapsed"
    )

    calculator_rows = [
        [("7", "seven", "7"), ("8", "eight", "8"), ("9", "nine", "9"), ("÷", "divide", "/")],
        [("4", "four", "4"), ("5", "five", "5"), ("6", "six", "6"), ("×", "multiply", "*")],
        [("1", "one", "1"), ("2", "two", "2"), ("3", "three", "3"), ("-", "minus", "-")],
        [("0", "zero", "0"), (".", "decimal", "."), ("(", "left_parenthesis", "("), ("+", "plus", "+")],
        [(")", "right_parenthesis", ")"), ("⌫", "backspace", None), ("C", "clear", None), ("=", "equals", None)]
    ]

    for row in calculator_rows:
        columns = st.columns(4)
        for column, button_data in zip(columns, row):
            label, key, value = button_data
            with column:
                if key == "backspace":
                    st.button(label, key=key, use_container_width=True, on_click=backspace_calculator)
                elif key == "clear":
                    st.button(label, key=key, use_container_width=True, on_click=clear_calculator)
                elif key == "equals":
                    st.button(label, key=key, use_container_width=True, on_click=calculate_result)
                else:
                    st.button(label, key=key, use_container_width=True, on_click=add_to_calculator, args=(value,))

with sci_col:
    st.markdown("<p style='font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#94a3b8; margin-bottom:10px;'>Scientific Functions</p>", unsafe_allow_html=True)
    
    scientific_rows = [
        [("√", "sqrt", "sqrt("), ("sin", "sin", "sin(")],
        [("cos", "cos", "cos("), ("tan", "tan", "tan(")],
        [("log", "log", "log("), ("ln", "ln", "ln(")],
        [("π", "pi", "pi"), ("e", "e", "e")]
    ]

    for row in scientific_rows:
        columns = st.columns(2)
        for column, button_data in zip(columns, row):
            label, key, value = button_data
            with column:
                st.button(label, key=key, use_container_width=True, on_click=add_to_calculator, args=(value,))

if st.session_state.calc_result:
    show_calculator_result()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ==========================================================
# 3. GRADE CALCULATOR
# ==========================================================

st.markdown('<div id="grading" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px;">
    <span class="corporate-badge">PERFORMANCE ANALYTICS</span>
    <h1 class="corporate-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Grade Calculator</h1>
    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Calculate overall GPA with weighted scores and attendance tracking.</p>
</div>
""", unsafe_allow_html=True)

if "grade_subjects" not in st.session_state:
    st.session_state.grade_subjects = ["Mathematics", "Science", "English"]

if "subject_weights" not in st.session_state:
    st.session_state.subject_weights = {"Mathematics": 6, "Science": 4, "English": 5}


def get_letter_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    return "F"


def get_grade_points(letter):
    return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}[letter]


st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:12px;'>Evaluation Formula: <strong>70% Assessment + 30% Attendance</strong></p>", unsafe_allow_html=True)

scores = {}
weights = {}
attendance = {}

for subject_name in st.session_state.grade_subjects:
    with st.container():
        st.markdown(f"<h4 style='margin:0 0 12px 0; font-size:1.1rem; color:#f8fafc;'>📚 {subject_name}</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            scores[subject_name] = st.number_input("Score / 100", min_value=0, max_value=100, value=85, step=1, key=f"grade_score_{subject_name}")
        with col2:
            attendance[subject_name] = st.number_input("Classes Attended / 10", min_value=0, max_value=10, value=9, step=1, key=f"attendance_{subject_name}")
        with col3:
            default_weight = st.session_state.subject_weights.get(subject_name, 1)
            weights[subject_name] = st.number_input("Subject Weight", min_value=1, max_value=20, value=default_weight, step=1, key=f"weight_{subject_name}")
            st.session_state.subject_weights[subject_name] = weights[subject_name]

# Add Subject Controls
col_add_input, col_add_btn = st.columns([3, 1])
with col_add_input:
    new_subject = st.text_input("New Subject Title", placeholder="e.g. Microeconomics", label_visibility="collapsed")
with col_add_btn:
    if st.button("➕ Add Course", use_container_width=True):
        cleaned = new_subject.strip()
        if not cleaned:
            st.warning("Please enter a valid subject title.")
        elif cleaned in st.session_state.grade_subjects:
            st.warning("Subject already exists.")
        else:
            st.session_state.grade_subjects.append(cleaned)
            st.session_state.subject_weights[cleaned] = 1
            st.rerun()

# Calculation Action Buttons
col_calc, col_reset = st.columns(2)
with col_calc:
    calculate = st.button("🧮 Compute GPA", use_container_width=True)
with col_reset:
    reset = st.button("↻ Reset Assessment", use_container_width=True)

if reset:
    st.session_state.grade_subjects = ["Mathematics", "Science", "English"]
    st.session_state.subject_weights = {"Mathematics": 6, "Science": 4, "English": 5}
    keys_to_remove = [k for k in list(st.session_state.keys()) if k.startswith("grade_score_") or k.startswith("attendance_") or k.startswith("weight_")]
    for k in keys_to_remove:
        del st.session_state[k]
    st.rerun()

if calculate:
    total_weighted_gpa = 0
    total_weights = 0
    results = []

    for subject_name in st.session_state.grade_subjects:
        score = scores[subject_name]
        classes_attended = attendance[subject_name]
        weight = weights[subject_name]

        att_pct = (classes_attended / 10) * 100
        final_score = (score * 0.70) + (att_pct * 0.30)
        letter = get_letter_grade(final_score)
        points = get_grade_points(letter)

        total_weighted_gpa += (points * weight)
        total_weights += weight

        results.append({
            "subject": subject_name, "score": score, "attended": classes_attended,
            "att_pct": att_pct, "final_score": final_score, "letter": letter,
            "points": points, "weight": weight
        })

    final_gpa = total_weighted_gpa / total_weights if total_weights > 0 else 0

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    
    # Result Summary Hero
    st.markdown(f"""
    <div class="profile-card" style="text-align: center; border-color: rgba(56, 189, 248, 0.3);">
        <span class="corporate-badge">CUMULATIVE GPA</span>
        <h1 style="font-size: 3.5rem; margin: 10px 0; color: #ffffff;">{final_gpa:.2f} <span style="font-size: 1.5rem; color: #64748b;">/ 4.00</span></h1>
        <p style="color: #38bdf8; font-weight: 600; margin: 0;">{"Academic Distinction" if final_gpa >= 3.5 else "Satisfactory Standing"}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:1.1rem; font-weight:700; color:#f8fafc; margin: 24px 0 12px 0;'>Subject Breakdown</p>", unsafe_allow_html=True)

    for res in results:
        with st.container():
            c1, c2, c3 = st.columns([1.5, 1.5, 1])
            with c1:
                st.markdown(f"**📚 {res['subject']}**")
                st.caption(f"Score: {res['score']}/100 | Attended: {res['attended']}/10")
            with c2:
                st.markdown(f"Final Grade: **{res['final_score']:.1f}%**")
                st.caption(f"Weight: {res['weight']} unit(s)")
            with c3:
                st.markdown(f"### **{res['letter']}** ({res['points']:.1f})")

# Grading Scale Reference Table
st.markdown("<p style='font-size:1rem; font-weight:700; color:#cbd5e1; margin: 30px 0 12px 0;'>Standard Grading Scale Reference</p>", unsafe_allow_html=True)
st.table({
    "Letter Grade": ["A", "B", "C", "D", "F"],
    "Percentage Range": ["90% – 100%", "80% – 89%", "70% – 79%", "60% – 69%", "0% – 59%"],
    "Description": ["Outstanding / Excellent", "Above Average / Good", "Satisfactory / Average", "Minimum Passing", "Failing"],
    "GPA Points": ["4.0", "3.0", "2.0", "1.0", "0.0"]
})

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ==========================================================
# 4. QUIZ MASTER
# ==========================================================

st.markdown('<div id="quiz-maker" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 24px;">
    <span class="corporate-badge">KNOWLEDGE ASSESSMENT</span>
    <h1 class="corporate-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Quiz Master</h1>
    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Construct and take customized multiple-choice evaluations.</p>
</div>
""", unsafe_allow_html=True)

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if st.button("➕ Add New Question Item", use_container_width=True):
    st.session_state.quiz_questions.append({
        "question": "", "A": "", "B": "", "C": "", "D": "", "correct": "A"
    })
    st.rerun()

if st.session_state.quiz_questions:
    for idx, q in enumerate(st.session_state.quiz_questions):
        with st.container():
            st.markdown(f"<p style='font-size:0.85rem; font-weight:700; color:#38bdf8;'>QUESTION {idx + 1}</p>", unsafe_allow_html=True)
            q["question"] = st.text_input(f"Question Title #{idx + 1}", value=q["question"], key=f"q_title_{idx}")
            
            c1, c2 = st.columns(2)
            with c1:
                q["A"] = st.text_input(f"Option A", value=q["A"], key=f"q_a_{idx}")
                q["B"] = st.text_input(f"Option B", value=q["B"], key=f"q_b_{idx}")
            with c2:
                q["C"] = st.text_input(f"Option C", value=q["C"], key=f"q_c_{idx}")
                q["D"] = st.text_input(f"Option D", value=q["D"], key=f"q_d_{idx}")
                
            q["correct"] = st.selectbox(f"Correct Answer Key", ["A", "B", "C", "D"], index=["A", "B", "C", "D"].index(q["correct"]), key=f"q_corr_{idx}")
else:
    st.info("No assessment questions configured yet. Click the button above to add your first question.")
