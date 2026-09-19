import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Essentials | Academic & Computational Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_video_base64(video_path="background.mp4"):
    if os.path.exists(video_path):
        try:
            with open(video_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode('utf-8'), True
        except Exception:
            return None, False
    return None, False

video_b64, video_found = get_video_base64("background.mp4")

if "calc_expr" not in st.session_state:
    st.session_state.calc_expr = ""
if "calc_display" not in st.session_state:
    st.session_state.calc_display = "0"

if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {"name": "General Mathematics", "score": 85.0, "attendance": 9.0, "weight": 3.0}
    ]

if "quiz_items" not in st.session_state:
    st.session_state.quiz_items = [
        {
            "q": "What is 15% expressed as a decimal?",
            "a": "0.015", "b": "0.15", "c": "1.5", "d": "15.0",
            "correct": "B", "selected": None
        }
    ]

if "quiz_evaluated" not in st.session_state:
    st.session_state.quiz_evaluated = False

video_html = ""
if video_found and video_b64:
    video_html = f"""
    <div class="video-background-container">
        <video autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
    </div>
    """

bg_fallback_css = "" if video_found else """
.stApp {
    background: radial-gradient(circle at 50% 30%, #27272a 0%, #09090b 100%) !important;
}
"""

st.markdown(f"""
<style>
    {bg_fallback_css}
    
    /* Video Background Container */
    .video-background-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -100;
        overflow: hidden;
        pointer-events: none;
    }}
    .video-background-container video {{
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        filter: brightness(0.65) contrast(1.05);
    }}

    /* Low Blur Overlay so background remains crisp */
    .stApp {{
        background: transparent !important;
    }}
    
    /* Global Container Padding & Glassmorphism Theme */
    [data-testid="stAppViewContainer"] {{
        background: rgba(9, 9, 11, 0.65) !important;
        backdrop-filter: blur(3px) !important;
        -webkit-backdrop-filter: blur(3px) !important;
        scroll-behavior: smooth !important;
    }}

    /* Glass Cards */
    .glass-card {{
        background: rgba(24, 24, 27, 0.72) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.7) !important;
    }}

    /* Typography */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #f4f4f5 !important;
    }}

    h1, h2, h3, h4 {{
        color: #ffffff !important;
        font-weight: 800 !important;
    }}

    /* Custom Streamlit Buttons Styling */
    .stButton>button {{
        width: 100% !important;
        background: rgba(39, 39, 42, 0.85) !important;
        color: #f4f4f5 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 0.75rem !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.15s ease-in-out !important;
    }}
    .stButton>button:hover {{
        background: rgba(82, 82, 91, 0.9) !important;
        color: #ffffff !important;
        border-color: #a1a1aa !important;
        transform: translateY(-1px);
    }}
    .stButton>button:active {{
        transform: scale(0.97);
    }}

    /* Inputs Styling */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background: rgba(24, 24, 27, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 0.75rem !important;
        color: #f4f4f5 !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #a1a1aa !important;
        box-shadow: 0 0 0 2px rgba(161, 161, 170, 0.2) !important;
    }}

    /* Hide Main Streamlit Chrome */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    /* Smooth Target Offset */
    .section-anchor {{
        scroll-margin-top: 110px;
    }}

    /* Calculator Display */
    .calc-screen {{
        background: #09090b;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: right;
        margin-bottom: 0.75rem;
    }}
</style>
{video_html}
""", unsafe_allow_html=True)

st.markdown("""
<div style="position: sticky; top: 1rem; z-index: 999; margin-bottom: 2rem;">
    <div style="background: rgba(24, 24, 27, 0.82); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 1rem; padding: 0.75rem 1.25rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; box-shadow: 0 20px 40px -15px rgba(0,0,0,0.8);">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            <div style="width: 32px; height: 32px; border-radius: 10px; background: linear-gradient(135deg, #d4d4d8, #71717a); display: flex; align-items: center; justify-content: center; font-weight: 900; color: #09090b; font-size: 1rem;">E</div>
            <span style="font-weight: 800; font-size: 1.1rem; letter-spacing: -0.02em; color: #ffffff;">ESSENTIALS <span style="color: #a1a1aa; font-weight: 600;">SUITE</span></span>
        </div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button onclick="scrollToSection('sec-profile')" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); color: #f4f4f5; padding: 0.4rem 0.85rem; border-radius: 0.6rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: 0.2s;">👤 Profile</button>
            <button onclick="scrollToSection('sec-calc')" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); color: #f4f4f5; padding: 0.4rem 0.85rem; border-radius: 0.6rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: 0.2s;">🧮 Calc</button>
            <button onclick="scrollToSection('sec-grading')" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); color: #f4f4f5; padding: 0.4rem 0.85rem; border-radius: 0.6rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: 0.2s;">🎓 Grades</button>
            <button onclick="scrollToSection('sec-quiz')" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); color: #f4f4f5; padding: 0.4rem 0.85rem; border-radius: 0.6rem; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: 0.2s;">🧠 Quiz</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# JS bridge to handle smooth scrolling inside Streamlit container
components.html("""
<script>
    function scrollToSection(id) {
        const parentDoc = window.parent.document;
        const target = parentDoc.getElementById(id);
        const container = parentDoc.querySelector('[data-testid="stAppViewContainer"]');
        if (target && container) {
            const topPos = target.getBoundingClientRect().top + container.scrollTop - 100;
            container.scrollTo({
                top: topPos,
                behavior: 'smooth'
            });
        }
    }
</script>
""", height=0, width=0)

if not video_found:
    st.info("💡 **Live Background Note:** Place `background.mp4` in the project directory to enable the live video wallpaper.")

st.markdown('<div id="sec-profile" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 1rem;">
    <span style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #a1a1aa; background: rgba(255,255,255,0.05); padding: 0.2rem 0.6rem; border-radius: 1rem; border: 1px solid rgba(255,255,255,0.1);">Account Setup</span>
    <h2 style="font-size: 1.75rem; margin-top: 0.4rem; margin-bottom: 0.2rem;">Essentials Profile</h2>
    <p style="font-size: 0.85rem; color: #a1a1aa; margin: 0;">Fill out your information below to build your credential identity card.</p>
</div>
""", unsafe_allow_html=True)

col_prof_form, col_prof_preview = st.columns([7, 5])

with col_prof_form:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    p_name = st.text_input("Full Name", value="", placeholder="e.g. Alex Mercer")
    
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        p_age = st.text_input("Age", value="", placeholder="e.g. 21")
    with col_p2:
        p_school = st.text_input("Institution / University", value="", placeholder="e.g. Stanford University")
        
    col_p3, col_p4 = st.columns(2)
    with col_p3:
        p_subject = st.text_input("Primary Focus / Major", value="", placeholder="e.g. Computer Science")
    with col_p4:
        p_hobby = st.text_input("Specialization / Hobby", value="", placeholder="e.g. Quantitative Finance")
    
    save_btn = st.button("✨ Save Credentials")
    st.markdown('</div>', unsafe_allow_html=True)

with col_prof_preview:
    initials = "--"
    if p_name.strip():
        parts = p_name.strip().split()
        initials = "".join([pt[0].upper() for pt in parts[:2]])

    disp_name = p_name.strip() if p_name.strip() else "Your Name"
    disp_school = p_school.strip() if p_school.strip() else "Institution Name"
    disp_age = f"{p_age.strip()} yrs old" if p_age.strip() else "--"
    disp_subject = p_subject.strip() if p_subject.strip() else "Primary Field"
    disp_hobby = p_hobby.strip() if p_hobby.strip() else "Specialization"

    name_style = "" if p_name.strip() else "font-style: italic; opacity: 0.6;"
    school_style = "" if p_school.strip() else "font-style: italic; opacity: 0.6;"
    age_style = "" if p_age.strip() else "font-style: italic; opacity: 0.6;"
    subject_style = "" if p_subject.strip() else "font-style: italic; opacity: 0.6;"
    hobby_style = "" if p_hobby.strip() else "font-style: italic; opacity: 0.6;"

    st.markdown(f"""
    <div class="glass-card" style="position: relative; overflow: hidden;">
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; font-weight: 700; color: #a1a1aa; text-transform: uppercase; margin-bottom: 1rem;">
            <span>Live Profile Card</span>
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #34d399; display: inline-block;"></span>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem;">
            <div style="width: 60px; height: 60px; border-radius: 1rem; background: linear-gradient(135deg, #3f3f46, #71717a); border: 1px solid rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 900; color: #ffffff; flex-shrink: 0;">
                {initials}
            </div>
            <div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff; {name_style}">{disp_name}</div>
                <div style="font-size: 0.8rem; color: #d4d4d8; {school_style}">{disp_school}</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; padding: 0.75rem 0; border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.8rem;">
            <div>
                <span style="color: #a1a1aa; display: block; font-size: 0.7rem;">Age Record</span>
                <span style="color: #ffffff; font-weight: 700; {age_style}">{disp_age}</span>
            </div>
            <div>
                <span style="color: #a1a1aa; display: block; font-size: 0.7rem;">Focus Area</span>
                <span style="color: #ffffff; font-weight: 700; {subject_style}">{disp_subject}</span>
            </div>
        </div>
        <div style="padding-top: 0.75rem; font-size: 0.8rem;">
            <span style="color: #a1a1aa; display: block; font-size: 0.7rem;">Specialization</span>
            <span style="color: #f4f4f5; font-weight: 600; {hobby_style}">{disp_hobby}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if save_btn:
        st.success("✓ Credentials updated into local preview!")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div id="sec-calc" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 1rem;">
    <span style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #a1a1aa; background: rgba(255,255,255,0.05); padding: 0.2rem 0.6rem; border-radius: 1rem; border: 1px solid rgba(255,255,255,0.1);">Computational Engine</span>
    <h2 style="font-size: 1.75rem; margin-top: 0.4rem; margin-bottom: 0.2rem;">Scientific Calculator</h2>
    <p style="font-size: 0.85rem; color: #a1a1aa; margin: 0;">Responsive mobile & desktop keypad for scientific math functions.</p>
</div>
""", unsafe_allow_html=True)

calc_col1, calc_col2, calc_col3 = st.columns([1, 2, 1])

with calc_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Screen Display
    st.markdown(f"""
    <div class="calc-screen">
        <div style="font-size: 0.75rem; color: #a1a1aa; font-family: monospace; min-height: 1.2rem;">{st.session_state.calc_expr}</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; font-family: monospace;">{st.session_state.calc_display}</div>
    </div>
    """, unsafe_allow_html=True)

    def calc_append(val):
        st.session_state.calc_expr += str(val)
        st.session_state.calc_display = st.session_state.calc_expr

    def calc_clear():
        st.session_state.calc_expr = ""
        st.session_state.calc_display = "0"

    def calc_backspace():
        st.session_state.calc_expr = st.session_state.calc_expr[:-1]
        st.session_state.calc_display = st.session_state.calc_expr if st.session_state.calc_expr else "0"

    def calc_eval():
        if not st.session_state.calc_expr:
            return
        try:
            # Safe Math Evaluation
            import math
            expr = st.session_state.calc_expr.replace("π", "math.pi").replace("e", "math.e")
            expr = expr.replace("sin(", "math.sin(").replace("cos(", "math.cos(").replace("tan(", "math.tan(")
            expr = expr.replace("sqrt(", "math.sqrt(").replace("log(", "math.log10(").replace("ln(", "math.log(")
            
            res = eval(expr, {"__builtins__": None, "math": math})
            if isinstance(res, float):
                res = round(res, 8)
            st.session_state.calc_display = str(res)
            st.session_state.calc_expr = str(res)
        except Exception:
            st.session_state.calc_display = "Error"
            st.session_state.calc_expr = ""

    # Grid Buttons Row 1
    r1_1, r1_2, r1_3, r1_4 = st.columns(4)
    r1_1.button("√", on_click=calc_append, args=("sqrt(",))
    r1_2.button("sin", on_click=calc_append, args=("sin(",))
    r1_3.button("cos", on_click=calc_append, args=("cos(",))
    r1_4.button("tan", on_click=calc_append, args=("tan(",))

    # Grid Buttons Row 2
    r2_1, r2_2, r2_3, r2_4 = st.columns(4)
    r2_1.button("log", on_click=calc_append, args=("log(",))
    r2_2.button("ln", on_click=calc_append, args=("ln(",))
    r2_3.button("π", on_click=calc_append, args=("π",))
    r2_4.button("e", on_click=calc_append, args=("e",))

    # Grid Buttons Row 3
    r3_1, r3_2, r3_3, r3_4 = st.columns(4)
    r3_1.button("C", on_click=calc_clear)
    r3_2.button("(", on_click=calc_append, args=("(",))
    r3_3.button(")", on_click=calc_append, args=(")",))
    r3_4.button("÷", on_click=calc_append, args=("/",))

    # Grid Buttons Row 4
    r4_1, r4_2, r4_3, r4_4 = st.columns(4)
    r4_1.button("7", on_click=calc_append, args=("7",))
    r4_2.button("8", on_click=calc_append, args=("8",))
    r4_3.button("9", on_click=calc_append, args=("9",))
    r4_4.button("×", on_click=calc_append, args=("*",))

    # Grid Buttons Row 5
    r5_1, r5_2, r5_3, r5_4 = st.columns(4)
    r5_1.button("4", on_click=calc_append, args=("4",))
    r5_2.button("5", on_click=calc_append, args=("5",))
    r5_3.button("6", on_click=calc_append, args=("6",))
    r5_4.button("-", on_click=calc_append, args=("-",))

    # Grid Buttons Row 6
    r6_1, r6_2, r6_3, r6_4 = st.columns(4)
    r6_1.button("1", on_click=calc_append, args=("1",))
    r6_2.button("2", on_click=calc_append, args=("2",))
    r6_3.button("3", on_click=calc_append, args=("3",))
    r6_4.button("+", on_click=calc_append, args=("+",))

    # Grid Buttons Row 7
    r7_1, r7_2, r7_3, r7_4 = st.columns(4)
    r7_1.button("0", on_click=calc_append, args=("0",))
    r7_2.button(".", on_click=calc_append, args=(".",))
    r7_3.button("⌫", on_click=calc_backspace)
    r7_4.button("=", on_click=calc_eval)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div id="sec-grading" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 1rem;">
    <span style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #a1a1aa; background: rgba(255,255,255,0.05); padding: 0.2rem 0.6rem; border-radius: 1rem; border: 1px solid rgba(255,255,255,0.1);">Academic Performance</span>
    <h2 style="font-size: 1.75rem; margin-top: 0.4rem; margin-bottom: 0.2rem;">Grade & GPA Evaluator</h2>
    <p style="font-size: 0.85rem; color: #a1a1aa; margin: 0;">Weighted formula: <strong>70% Assessment Score + 30% Attendance Ratio</strong>.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

for idx, subj in enumerate(st.session_state.subjects):
    st.markdown(f"##### 📚 Course #{idx+1}: {subj['name']}")
    sc1, sc2, sc3, sc4 = st.columns([3, 3, 3, 1])
    with sc1:
        st.session_state.subjects[idx]['score'] = st.number_input(f"Score (0-100)", min_value=0.0, max_value=100.0, value=float(subj['score']), key=f"score_{idx}")
    with sc2:
        st.session_state.subjects[idx]['attendance'] = st.number_input(f"Attendance (0-10)", min_value=0.0, max_value=10.0, value=float(subj['attendance']), key=f"att_{idx}")
    with sc3:
        st.session_state.subjects[idx]['weight'] = st.number_input(f"Credits Weight", min_value=1.0, max_value=20.0, value=float(subj['weight']), key=f"wt_{idx}")
    with sc4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if len(st.session_state.subjects) > 1:
            if st.button("✕", key=f"del_{idx}"):
                st.session_state.subjects.pop(idx)
                st.rerun()

st.markdown("---")
add_col1, add_col2 = st.columns([3, 1])
with add_col1:
    new_subject_name = st.text_input("New Course Name", placeholder="e.g. Econometrics", label_visibility="collapsed")
with add_col2:
    if st.button("➕ Add Course"):
        if new_subject_name.strip():
            st.session_state.subjects.append({
                "name": new_subject_name.strip(),
                "score": 80.0,
                "attendance": 8.0,
                "weight": 3.0
            })
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# GPA Calculation
total_weighted_points = 0.0
total_weights = 0.0
breakdown_items = []

for s in st.session_state.subjects:
    att_pct = (s["attendance"] / 10.0) * 100.0
    final_score = (s["score"] * 0.70) + (att_pct * 0.30)
    
    letter = 'F'
    points = 0.0
    if final_score >= 90: letter, points = 'A', 4.0
    elif final_score >= 80: letter, points = 'B', 3.0
    elif final_score >= 70: letter, points = 'C', 2.0
    elif final_score >= 60: letter, points = 'D', 1.0

    total_weighted_points += (points * s["weight"])
    total_weights += s["weight"]
    breakdown_items.append((s["name"], s["weight"], final_score, letter, points))

cumulative_gpa = (total_weighted_points / total_weights) if total_weights > 0 else 0.0

st.markdown(f"""
<div class="glass-card" style="text-align: center;">
    <span style="font-size: 0.75rem; font-weight: 700; color: #a1a1aa; text-transform: uppercase;">Cumulative Performance Result</span>
    <div style="font-size: 3.2rem; font-weight: 900; color: #ffffff; margin: 0.5rem 0;">{cumulative_gpa:.2f} <span style="font-size: 1.2rem; color: #a1a1aa; font-weight: 400;">/ 4.00</span></div>
    <div style="font-size: 0.9rem; font-weight: 600; color: #e4e4e7;">{"🏆 Outstanding Academic Honor" if cumulative_gpa >= 3.5 else ("✨ Good Academic Standing" if cumulative_gpa >= 3.0 else "📈 Satisfactory Progress")}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div id="sec-quiz" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom: 1rem;">
    <span style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #a1a1aa; background: rgba(255,255,255,0.05); padding: 0.2rem 0.6rem; border-radius: 1rem; border: 1px solid rgba(255,255,255,0.1);">Knowledge Assessment</span>
    <h2 style="font-size: 1.75rem; margin-top: 0.4rem; margin-bottom: 0.2rem;">Quiz Master Builder</h2>
    <p style="font-size: 0.85rem; color: #a1a1aa; margin: 0;">Create custom questionnaires and evaluate your progress interactive style.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

for q_idx, item in enumerate(st.session_state.quiz_items):
    st.markdown(f"##### Question #{q_idx+1}")
    item["q"] = st.text_input("Question Title", value=item["q"], key=f"q_title_{q_idx}")
    
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        item["a"] = st.text_input("Option A", value=item["a"], key=f"opt_a_{q_idx}")
        item["c"] = st.text_input("Option C", value=item["c"], key=f"opt_c_{q_idx}")
    with q_col2:
        item["b"] = st.text_input("Option B", value=item["b"], key=f"opt_b_{q_idx}")
        item["d"] = st.text_input("Option D", value=item["d"], key=f"opt_d_{q_idx}")

    ans_col1, ans_col2 = st.columns([2, 1])
    with ans_col1:
        item["selected"] = st.radio(
            "Select Your Answer",
            options=["A", "B", "C", "D"],
            index=["A", "B", "C", "D"].index(item["selected"]) if item["selected"] in ["A", "B", "C", "D"] else 0,
            key=f"ans_radio_{q_idx}",
            horizontal=True
        )
    with ans_col2:
        item["correct"] = st.selectbox(
            "Correct Answer Key",
            options=["A", "B", "C", "D"],
            index=["A", "B", "C", "D"].index(item["correct"]),
            key=f"ans_key_{q_idx}"
        )

    if len(st.session_state.quiz_items) > 1:
        if st.button("✕ Delete Question", key=f"del_q_{q_idx}"):
            st.session_state.quiz_items.pop(q_idx)
            st.rerun()
    st.markdown("---")

q_btn1, q_btn2 = st.columns(2)
with q_btn1:
    if st.button("➕ Add Question Prompt"):
        st.session_state.quiz_items.append({
            "q": "New Question Prompt",
            "a": "Option 1", "b": "Option 2", "c": "Option 3", "d": "Option 4",
            "correct": "A", "selected": "A"
        })
        st.session_state.quiz_evaluated = False
        st.rerun()

with q_btn2:
    if st.button("🚀 Evaluate Quiz"):
        st.session_state.quiz_evaluated = True

if st.session_state.quiz_evaluated:
    correct_cnt = sum([1 for q in st.session_state.quiz_items if q["selected"] == q["correct"]])
    tot_cnt = len(st.session_state.quiz_items)
    score_pct = (correct_cnt / tot_cnt) * 100 if tot_cnt > 0 else 0

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); border-radius: 0.75rem; padding: 1rem; text-align: center; margin-top: 1rem;">
        <h4 style="margin: 0; font-size: 1.2rem; color: #ffffff;">Quiz Score: {correct_cnt} / {tot_cnt}</h4>
        <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #a1a1aa;">Overall Accuracy: {score_pct:.0f}%</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
