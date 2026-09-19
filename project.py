import streamlit as st
import os
import base64
import math

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Essentials | Profile, Calculator & Grading",
    page_icon="⚡",
    layout="wide"
)

# ==========================================================
# BACKGROUND VIDEO INJECTOR
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
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    #bg-video-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -100;
        overflow: hidden;
        pointer-events: none;
    }}

    #bg-video-container video {{
        min-width: 100%;
        min-height: 100%;
        width: auto;
        height: auto;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        object-fit: cover;
        filter: brightness(0.65) contrast(1.05);
    }}

    #bg-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: radial-gradient(circle at 50% 20%, rgba(24, 24, 27, 0.45) 0%, rgba(9, 9, 11, 0.75) 100%);
        z-index: -99;
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        pointer-events: none;
    }}
    </style>

    <div id="bg-video-container">
        {"<video autoplay loop muted playsinline webkit-playsinline preload='auto'><source src='data:video/mp4;base64," + video_base64 + "' type='video/mp4'></video>" if video_base64 else ""}
    </div>
    <div id="bg-overlay"></div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# ESSENTIALS DESIGN SYSTEM & SMOOTH SCROLL SCRIPT
# ==========================================================

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    scroll-behavior: smooth !important;
}

.block-container {
    width: min(92vw, 1200px) !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding-top: 20px !important;
    padding-bottom: 80px !important;
}

.section-anchor {
    scroll-margin-top: 110px;
}

h1, h2, h3, h4 {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif !important;
    letter-spacing: -0.025em !important;
}

.essentials-gradient-text {
    background: linear-gradient(135deg, #f4f4f5 0%, #a1a1aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

.essentials-badge {
    display: inline-block;
    background: rgba(161, 161, 170, 0.12);
    border: 1px solid rgba(161, 161, 170, 0.25);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #e4e4e7;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.navigation-bar {
    position: sticky;
    top: 15px;
    z-index: 9999;
    background: rgba(24, 24, 27, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 10px 14px;
    margin-bottom: 32px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.navigation-title {
    text-align: center;
    color: #71717a;
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
    color: #e4e4e7 !important;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.navigation-link:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    color: #ffffff !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(24, 24, 27, 0.6) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    padding: 16px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: rgba(24, 24, 27, 0.7) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #a1a1aa !important;
    box-shadow: 0 0 0 3px rgba(161, 161, 170, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(180deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.06) 100%) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stTable"] table {
    background: rgba(24, 24, 27, 0.75) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

div[data-testid="stTable"] th {
    color: #f4f4f5 !important;
    background: rgba(39, 39, 42, 0.9) !important;
}

[data-testid="stDialog"] > div {
    background: rgba(24, 24, 27, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 24px !important;
}

.section-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin: 40px 0;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.navigation-link');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').replace('#', '');
            const targetElem = document.getElementById(targetId);
            const container = document.querySelector('[data-testid="stAppViewContainer"]');
            if (targetElem && container) {
                const topOffset = targetElem.getBoundingClientRect().top + container.scrollTop - 110;
                container.scrollTo({ top: topOffset, behavior: 'smooth' });
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)

# Hide Streamlit UI Chrome
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
    <div class="navigation-title">ESSENTIALS</div>
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
<div style="margin-bottom: 20px;">
    <span class="essentials-badge">USER PROFILE</span>
    <h1 class="essentials-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Personal Details</h1>
    <p style="color: #a1a1aa; font-size: 0.95rem; margin: 0;">Fill in your details to create your personalized card.</p>
</div>
""", unsafe_allow_html=True)

input_col, preview_col = st.columns([1.1, 0.9], gap="large")

with input_col:
    with st.container(border=True):
        name = st.text_input("Name", value="", placeholder="Enter your full name")
        school = st.text_input("School", value="", placeholder="Enter your school name")
        favorite_subject = st.text_input("Favorite Subject", value="", placeholder="e.g. Mathematics, Science")
        hobby = st.text_input("Favorite Hobby", value="", placeholder="e.g. Football, Gaming, Drawing")

with preview_col:
    st.markdown("<p style='font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#a1a1aa; margin-bottom:10px;'>Card Preview</p>", unsafe_allow_html=True)
    
    initials = "".join([part[0].upper() for part in name.split()[:2]]) if name.strip() else "??"
    
    with st.container(border=True):
        col_avatar, col_info = st.columns([1, 3])
        with col_avatar:
            st.markdown(f"""
            <div style="
                width: 64px; height: 64px; border-radius: 50%;
                background: linear-gradient(135deg, #3f3f46 0%, #18181b 100%);
                display: flex; align-items: center; justify-content: center;
                font-size: 22px; font-weight: 800; color: #ffffff;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
                border: 2px solid rgba(255, 255, 255, 0.15);
            ">{initials}</div>
            """, unsafe_allow_html=True)
        with col_info:
            st.markdown(f"### {name if name.strip() else 'Your Name'}")
            st.caption(f"🏫 **{school if school.strip() else 'School Name'}**")
        
        st.divider()
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.caption("FAVORITE SUBJECT")
            st.markdown(f"**{favorite_subject if favorite_subject.strip() else 'Not specified'}**")
        with stat_col2:
            st.caption("FAVORITE HOBBY")
            st.markdown(f"**{hobby if hobby.strip() else 'Not specified'}**")

@st.dialog("Profile Saved")
def show_profile_popup():
    st.markdown(f"""
    <div style="text-align: center; padding: 10px 0;">
        <div style="
            width: 64px; height: 64px; border-radius: 50%;
            background: linear-gradient(135deg, #3f3f46 0%, #18181b 100%);
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: 800; color: #ffffff; margin: 0 auto 12px auto;
        ">{initials}</div>
        <h2 style="margin: 0; color: #ffffff;">{name}</h2>
        <p style="color: #a1a1aa; font-weight: 600; margin-top: 4px;">{school}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.write(f"👤 **Name:** {name}")
        st.write(f"🏫 **School:** {school}")
        st.write(f"📚 **Favorite Subject:** {favorite_subject}")
        st.write(f"🎨 **Favorite Hobby:** {hobby}")

    if st.button("Confirm", use_container_width=True):
        st.rerun()

st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

if st.button("✨ Save Profile", use_container_width=True):
    if name.strip() and school.strip() and favorite_subject.strip() and hobby.strip():
        show_profile_popup()
    else:
        st.warning("Please fill out all fields before saving.")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ==========================================================
# 2. SCIENTIFIC CALCULATOR
# ==========================================================

st.markdown('<div id="calculator" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 20px;">
    <span class="essentials-badge">COMPUTATIONAL TOOL</span>
    <h1 class="essentials-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Scientific Calculator</h1>
    <p style="color: #a1a1aa; font-size: 0.95rem; margin: 0;">Perform basic and advanced mathematical calculations.</p>
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
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "log": math.log10, "ln": math.log,
            "pi": math.pi, "e": math.e
        }
        result = eval(expression, {"__builtins__": {}}, allowed)

        if isinstance(result, float):
            result = str(int(result)) if result.is_integer() else str(round(result, 10))
        else:
            result = str(result)

        st.session_state.calc_result = result
    except ZeroDivisionError:
        st.session_state.calc_result = "Error: Division by zero"
    except Exception:
        st.session_state.calc_result = "Error: Invalid expression"

@st.dialog("Calculation Result")
def show_calculator_result():
    st.caption("SUBMITTED EXPRESSION")
    st.code(st.session_state.calc_display, language=None)
    
    st.markdown(
        f"""
        <div style="
            text-align:center; padding:20px; font-size:32px; font-weight:800;
            color:#ffffff; background: rgba(39, 39, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 16px; margin: 16px 0;
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
        [("7", "7", "7"), ("8", "8", "8"), ("9", "9", "9"), ("÷", "divide", "/")],
        [("4", "4", "4"), ("5", "5", "5"), ("6", "6", "6"), ("×", "multiply", "*")],
        [("1", "1", "1"), ("2", "2", "2"), ("3", "3", "3"), ("-", "minus", "-")],
        [("0", "0", "0"), (".", "decimal", "."), ("(", "l_paren", "("), ("+", "plus", "+")],
        [(")", "r_paren", ")"), ("⌫", "backspace", None), ("C", "clear", None), ("=", "equals", None)]
    ]

    for row in calculator_rows:
        columns = st.columns(4)
        for column, button_data in zip(columns, row):
            label, key, value = button_data
            with column:
                if key == "backspace":
                    st.button(label, key=f"btn_{key}", use_container_width=True, on_click=backspace_calculator)
                elif key == "clear":
                    st.button(label, key=f"btn_{key}", use_container_width=True, on_click=clear_calculator)
                elif key == "equals":
                    st.button(label, key=f"btn_{key}", use_container_width=True, on_click=calculate_result)
                else:
                    st.button(label, key=f"btn_{key}", use_container_width=True, on_click=add_to_calculator, args=(value,))

with sci_col:
    st.markdown("<p style='font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#a1a1aa; margin-bottom:10px;'>Scientific Functions</p>", unsafe_allow_html=True)
    
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
                st.button(label, key=f"btn_sci_{key}", use_container_width=True, on_click=add_to_calculator, args=(value,))

if st.session_state.calc_result:
    show_calculator_result()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ==========================================================
# 3. GRADE CALCULATOR
# ==========================================================

st.markdown('<div id="grading" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 20px;">
    <span class="essentials-badge">PERFORMANCE ANALYTICS</span>
    <h1 class="essentials-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Grade Calculator</h1>
    <p style="color: #a1a1aa; font-size: 0.95rem; margin: 0;">Calculate overall GPA with weighted scores and attendance tracking.</p>
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

st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#e4e4e7; margin-bottom:12px;'>Evaluation Formula: <strong>70% Assessment + 30% Attendance</strong></p>", unsafe_allow_html=True)

scores = {}
weights = {}
attendance = {}

for subject_name in st.session_state.grade_subjects:
    with st.container(border=True):
        st.subheader(f"📚 {subject_name}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            scores[subject_name] = st.number_input("Score / 100", min_value=0, max_value=100, value=85, step=1, key=f"grade_score_{subject_name}")
        with col2:
            attendance[subject_name] = st.number_input("Classes Attended / 10", min_value=0, max_value=10, value=9, step=1, key=f"attendance_{subject_name}")
        with col3:
            default_weight = st.session_state.subject_weights.get(subject_name, 1)
            weights[subject_name] = st.number_input("Subject Weight", min_value=1, max_value=20, value=default_weight, step=1, key=f"weight_{subject_name}")
            st.session_state.subject_weights[subject_name] = weights[subject_name]

col_add_input, col_add_btn = st.columns([3, 1])
with col_add_input:
    new_subject = st.text_input("New Subject Title", placeholder="e.g. History", label_visibility="collapsed")
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
    
    with st.container(border=True):
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.caption("CUMULATIVE GPA")
        st.markdown(f"<h1 style='font-size: 3.5rem; margin: 0; color: #ffffff;'>{final_gpa:.2f} <span style='font-size: 1.5rem; color: #71717a;'>/ 4.00</span></h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #a1a1aa; font-weight: 600;'>{'Academic Distinction' if final_gpa >= 3.5 else 'Satisfactory Standing'}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:1.1rem; font-weight:700; color:#f4f4f5; margin: 24px 0 12px 0;'>Subject Breakdown</p>", unsafe_allow_html=True)

    for res in results:
        with st.container(border=True):
            c1, c2, c3 = st.columns([1.5, 1.5, 1])
            with c1:
                st.markdown(f"**📚 {res['subject']}**")
                st.caption(f"Score: {res['score']}/100 | Attended: {res['attended']}/10")
            with c2:
                st.markdown(f"Final Grade: **{res['final_score']:.1f}%**")
                st.caption(f"Weight: {res['weight']} unit(s)")
            with c3:
                st.markdown(f"### **{res['letter']}** ({res['points']:.1f})")

st.markdown("<p style='font-size:1rem; font-weight:700; color:#e4e4e7; margin: 30px 0 12px 0;'>Standard Grading Scale Reference</p>", unsafe_allow_html=True)
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
<div style="margin-bottom: 20px;">
    <span class="essentials-badge">KNOWLEDGE ASSESSMENT</span>
    <h1 class="essentials-gradient-text" style="margin: 4px 0 8px 0; font-size: 2.2rem;">Quiz Master</h1>
    <p style="color: #a1a1aa; font-size: 0.95rem; margin: 0;">Construct and take customized multiple-choice evaluations.</p>
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
        with st.container(border=True):
            st.caption(f"QUESTION {idx + 1}")
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
