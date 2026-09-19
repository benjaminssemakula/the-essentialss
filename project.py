import streamlit as st
import os
import base64
import math

# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🎓",
    layout="centered"
)

# ==========================================================
# CUSTOM LIVE VIDEO BACKGROUND
# ==========================================================

video_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "background.mp4"
)

with open(video_path, "rb") as video_file:
    video_bytes = video_file.read()

video_base64 = base64.b64encode(video_bytes).decode()

st.markdown(
    f"""
    <style>

    /* Make the Streamlit background transparent */
    .stApp {{
        background: transparent !important;
    }}

    /* Video background */
    .custom-background {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -10;
        overflow: hidden;
    }}

    .custom-background video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        top: 0;
        left: 0;
    }}

    /* Dark overlay so text is easier to see */
    .background-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.35);
        z-index: -9;
    }}

    
    /* Compact mobile calculator */
    @media (max-width: 600px) {
        .calculator-display {
            margin-bottom: 0.35rem !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.calculator-display) {
            gap: 0.2rem !important;
        }

        .stButton > button {
            min-height: 42px !important;
            padding: 0.35rem 0.25rem !important;
            font-size: 0.88rem !important;
        }

        input, textarea, select {
            font-size: 0.9rem !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 0.35rem !important;
        }
    }


    /* Stronger backdrop blur for readability */
    .glass-card,
    .stExpander,
    div[data-testid="stMetric"],
    div[data-testid="stDataFrame"],
    div[data-testid="stForm"],
    div[data-testid="stPopover"],
    div[data-testid="stDialog"] > div {
        backdrop-filter: blur(18px) saturate(115%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(115%) !important;
        background: rgba(10, 12, 16, 0.72) !important;
        border-color: rgba(255, 255, 255, 0.10) !important;
    }

    /* Keep text crisp above the blurred background */
    .main .block-container {
        position: relative;
        z-index: 1;
    }

    /* Subtle readability veil behind the main content */
    .main .block-container::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: -1;
        pointer-events: none;
        background: rgba(0, 0, 0, 0.12);
        backdrop-filter: blur(3px);
        -webkit-backdrop-filter: blur(3px);
    }

</style>

    <div class="custom-background">
        <video autoplay muted loop playsinline>
            <source
                src="data:video/mp4;base64,{video_base64}"
                type="video/mp4"
            >
        </video>
    </div>

    <div class="background-overlay"></div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# ESSENTIALS APP
# ==========================================================

# ==========================================================
# CLEAN DARK DESIGN SYSTEM
# ==========================================================

st.markdown("""
<style>
:root {
    --bg: #07070a;
    --surface: rgba(17, 17, 21, 0.82);
    --surface-strong: rgba(22, 22, 27, 0.94);
    --border: rgba(255,255,255,.09);
    --border-hover: rgba(255,255,255,.18);
    --text: #f5f5f7;
    --muted: #9a9aa3;
    --accent: #d4d4d8;
    --shadow: 0 18px 55px rgba(0,0,0,.34);
}

/* Base */
.stApp {
    color: var(--text);
    background: transparent !important;
}
html {
    scroll-behavior: smooth !important;
    scroll-padding-top: 105px;
}
body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    overflow-x: hidden !important;
}
.block-container {
    width: min(92vw, 1080px) !important;
    max-width: 1080px !important;
    margin: 0 auto !important;
    padding: 34px 0 72px !important;
}

/* Typography */
h1, h2, h3 {
    color: #fff !important;
    letter-spacing: -.035em !important;
    font-weight: 750 !important;
}
h1 { font-size: clamp(2rem, 4vw, 3.2rem) !important; line-height: 1.05 !important; }
h2 { font-size: clamp(1.45rem, 3vw, 2rem) !important; }
h3 { font-size: 1.15rem !important; }
p, label, .stMarkdown, .stCaption {
    color: var(--muted);
}
[data-testid="stCaptionContainer"] { color: var(--muted) !important; }

/* Glass cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(25,25,30,.88), rgba(12,12,16,.82)) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 14px !important;
    margin-bottom: 14px !important;
    box-shadow: var(--shadow);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox [data-baseweb="select"] {
    background: rgba(10,10,13,.72) !important;
    color: #fff !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
    transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
}
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: rgba(255,255,255,.28) !important;
    box-shadow: 0 0 0 3px rgba(255,255,255,.055) !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 44px;
    background: linear-gradient(180deg, rgba(255,255,255,.075), rgba(255,255,255,.035)) !important;
    color: #f8f8f8 !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-weight: 650 !important;
    transition: transform .18s ease, background .18s ease, border-color .18s ease, box-shadow .18s ease !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,.105) !important;
    border-color: var(--border-hover) !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(0,0,0,.22);
}
.stButton > button:active {
    transform: translateY(0) scale(.985);
}

/* Dividers */
hr {
    border: 0 !important;
    border-top: 1px solid rgba(255,255,255,.075) !important;
    margin: 34px 0 !important;
}

/* Alerts */
.stAlert {
    background: rgba(18,18,22,.84) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

/* Navigation */
.navigation-bar {
    position: sticky;
    top: 12px;
    z-index: 999;
    margin: 0 auto 34px;
    padding: 9px;
    background: rgba(13,13,17,.78);
    border: 1px solid rgba(255,255,255,.095);
    border-radius: 17px;
    box-shadow: 0 16px 45px rgba(0,0,0,.32);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}
.navigation-title {
    text-align: center;
    color: #777780;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .18em;
    margin: 2px 0 8px;
}
.navigation-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
}
.navigation-link {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 38px;
    padding: 7px 5px;
    color: #dedee2 !important;
    text-decoration: none !important;
    background: rgba(255,255,255,.035);
    border: 1px solid transparent;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 650;
    transition: all .2s ease;
}
.navigation-link:hover {
    color: #fff !important;
    background: rgba(255,255,255,.085);
    border-color: rgba(255,255,255,.09);
    transform: translateY(-1px);
}

/* Calculator */
.calculator-display input {
    text-align: right !important;
    font-size: 1.35rem !important;
    font-weight: 650 !important;
    letter-spacing: .02em;
}

/* Tables */
div[data-testid="stTable"] {
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}
div[data-testid="stTable"] table {
    background: rgba(13,13,17,.88) !important;
}
div[data-testid="stTable"] th {
    background: rgba(255,255,255,.055) !important;
    color: #fff !important;
    font-weight: 700 !important;
}
div[data-testid="stTable"] td {
    background: rgba(255,255,255,.018) !important;
    color: #ddd !important;
}

/* Dialogs */
[data-testid="stDialog"] > div {
    background: rgba(15,15,19,.97) !important;
    border: 1px solid rgba(255,255,255,.11) !important;
    border-radius: 22px !important;
    box-shadow: 0 30px 90px rgba(0,0,0,.62) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

/* Section anchors */
.section-anchor {
    display: block;
    scroll-margin-top: 105px;
}

/* Responsive */
@media (max-width: 768px) {
    .block-container {
        width: calc(100vw - 24px) !important;
        max-width: none !important;
        padding: 20px 0 48px !important;
    }
    .navigation-bar {
        top: 7px;
        margin-bottom: 24px;
        border-radius: 15px;
        padding: 7px;
    }
    .navigation-grid { gap: 4px; }
    .navigation-link {
        min-height: 36px;
        padding: 6px 2px;
        font-size: 10.5px;
        white-space: nowrap;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 11px !important;
        border-radius: 17px !important;
    }
    .stHorizontalBlock {
        gap: 6px !important;
    }
    .stButton > button {
        min-height: 42px !important;
        font-size: .88rem !important;
        padding: 7px 4px !important;
    }
    .stTextInput input,
    .stNumberInput input {
        font-size: 16px !important;
    }
    div[data-testid="stTable"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
    }
    div[data-testid="stTable"] table {
        min-width: 560px;
    }
    [data-testid="stDialog"] > div {
        width: calc(100vw - 24px) !important;
        max-width: calc(100vw - 24px) !important;
    }
}
@media (max-width: 390px) {
    .block-container { width: calc(100vw - 18px) !important; }
    .navigation-link { font-size: 9.5px; }
    .stButton > button { font-size: .82rem !important; }
}

/* Existing animations, refined */
@keyframes resultPop {
    0% { opacity: 0; transform: scale(.92); }
    100% { opacity: 1; transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# NAVIGATION SYSTEM
# ==========================================================

# Navigation bar
st.markdown("""
<div class="navigation-bar">
    <div class="navigation-title">QUICK NAVIGATION</div>
    <div class="navigation-grid">
        <a class="navigation-link" href="#profile">👤 Profile</a>
        <a class="navigation-link" href="#calculator">🧮 Calculator</a>
        <a class="navigation-link" href="#grading">🎓 Grading</a>
        <a class="navigation-link" href="#quiz-maker">🧠 Quiz Maker</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# PROFILE
# ==========================================================

st.markdown('<div id="profile" class="section-anchor"></div>', unsafe_allow_html=True)

st.title("👋 My Profile")

st.write(
    "Welcome! Fill in the information below to create your profile."
)

name = st.text_input("👤 What is your name?")
age = st.number_input(
    "🎂 How old are you?",
    min_value=1,
    max_value=100,
    step=1
)
school = st.text_input("🏫 What school do you go to?")
favorite_subject = st.text_input("📚 What is your favorite subject?")
hobby = st.text_input("🎨 What is your favorite hobby?")


@st.dialog("🎉 Profile Created!")
def show_profile_popup():

    st.subheader(f"Welcome, {name}! 👋")

    st.write("Here's a little bit about you.")

    st.markdown("---")

    st.write(f"👤 **Name:** {name}")
    st.write(f"🎂 **Age:** {age} years old")
    st.write(f"🏫 **School:** {school}")
    st.write(f"📚 **Favorite Subject:** {favorite_subject}")
    st.write(f"🎨 **Favorite Hobby:** {hobby}")

    st.markdown("---")

    st.success(
        f"Welcome to your profile, {name}! 🎓"
    )

    if st.button("✨ Done", use_container_width=True):
        st.rerun()


if st.button(
    "✨ Create My Profile",
    use_container_width=True
):

    if name and school and favorite_subject and hobby:
        show_profile_popup()
    else:
        st.warning(
            "Please fill in all the fields first."
        )


# ==========================================================

# Extra vertical space so this section occupies its own screen when scrolling.
st.markdown('<div style="height: 8vh;"></div>', unsafe_allow_html=True)

# ==========================================================
# SCIENTIFIC CALCULATOR
# ==========================================================

st.markdown(
    '<div id="calculator" class="section-anchor"></div>',
    unsafe_allow_html=True
)

st.markdown("---")

st.title("🧮 Scientific Calculator")

st.write(
    "A simple scientific calculator with powerful functions."
)


# ==========================================================
# CALCULATOR STATE
# ==========================================================

if "calc_display" not in st.session_state:
    st.session_state.calc_display = ""

if "calc_result" not in st.session_state:
    st.session_state.calc_result = ""

if "calc_show_result" not in st.session_state:
    st.session_state.calc_show_result = False


# ==========================================================
# CALCULATOR FUNCTIONS
# ==========================================================

def add_to_calculator(value):
    st.session_state.calc_display += str(value)
    st.session_state.calc_result = ""
    st.session_state.calc_show_result = False


def clear_calculator():
    st.session_state.calc_display = ""
    st.session_state.calc_result = ""
    st.session_state.calc_show_result = False


def backspace_calculator():
    st.session_state.calc_display = (
        st.session_state.calc_display[:-1]
    )
    st.session_state.calc_result = ""
    st.session_state.calc_show_result = False


def calculate_result():

    expression = st.session_state.calc_display.strip()

    if not expression:
        return

    try:

        # --------------------------------------------------
        # Convert calculator symbols to Python-compatible
        # expressions
        # --------------------------------------------------

        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")

        # --------------------------------------------------
        # Scientific functions
        # Trigonometry uses DEGREES
        # --------------------------------------------------

        def sin_deg(x):
            return math.sin(math.radians(x))

        def cos_deg(x):
            return math.cos(math.radians(x))

        def tan_deg(x):
            return math.tan(math.radians(x))

        allowed = {
            "sqrt": math.sqrt,
            "sin": sin_deg,
            "cos": cos_deg,
            "tan": tan_deg,
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e
        }

        # --------------------------------------------------
        # Safe evaluation
        # --------------------------------------------------

        result = eval(
            expression,
            {"__builtins__": None},
            allowed
        )

        # --------------------------------------------------
        # Format result
        # --------------------------------------------------

        if isinstance(result, complex):

            st.session_state.calc_result = (
                "Error: Complex numbers are not supported"
            )

        elif isinstance(result, (int, float)):

            if not math.isfinite(result):

                st.session_state.calc_result = (
                    "Error: Result is undefined"
                )

            elif result == 0:

                st.session_state.calc_result = "0"

            elif float(result).is_integer():

                st.session_state.calc_result = str(
                    int(result)
                )

            else:

                st.session_state.calc_result = str(
                    round(float(result), 10)
                )

        else:

            st.session_state.calc_result = str(result)

        st.session_state.calc_show_result = True

    except ZeroDivisionError:

        st.session_state.calc_result = (
            "Error: Cannot divide by zero"
        )

        st.session_state.calc_show_result = True

    except ValueError:

        st.session_state.calc_result = (
            "Error: Invalid mathematical operation"
        )

        st.session_state.calc_show_result = True

    except OverflowError:

        st.session_state.calc_result = (
            "Error: Number is too large"
        )

        st.session_state.calc_show_result = True

    except Exception:

        st.session_state.calc_result = (
            "Error: Invalid calculation"
        )

        st.session_state.calc_show_result = True


# ==========================================================
# RESULT DIALOG
# ==========================================================

@st.dialog("🧮 Calculation Result")
def show_calculator_result():

    st.subheader("Your calculation")

    st.caption("Expression")

    st.code(
        st.session_state.calc_display,
        language=None
    )

    st.markdown("---")

    st.subheader("Result")

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:22px 14px;
            font-size:clamp(30px, 8vw, 46px);
            font-weight:750;
            color:white;
            background:rgba(255,255,255,0.055);
            border:1px solid rgba(255,255,255,0.09);
            border-radius:20px;
            margin:12px 0 24px 0;
            animation:resultPop .35s ease-out;
            overflow-wrap:anywhere;
            word-break:break-word;
        ">
            {st.session_state.calc_result}
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "↺ Continue",
            use_container_width=True
        ):

            st.session_state.calc_show_result = False
            st.rerun()

    with col2:

        if st.button(
            "✓ Done",
            use_container_width=True
        ):

            st.session_state.calc_display = ""
            st.session_state.calc_result = ""
            st.session_state.calc_show_result = False
            st.rerun()


# ==========================================================
# DISPLAY
# ==========================================================

st.markdown(
    """
    <div class="calculator-display">
    """,
    unsafe_allow_html=True
)

st.text_input(
    "Calculator Display",
    value=st.session_state.calc_display,
    disabled=True,
    label_visibility="collapsed",
    key="calculator_display_box"
)

st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# BASIC CALCULATOR BUTTONS
# ==========================================================

calculator_rows = [

    [
        ("7", "calc_7", "7"),
        ("8", "calc_8", "8"),
        ("9", "calc_9", "9"),
        ("÷", "calc_divide", "/")
    ],

    [
        ("4", "calc_4", "4"),
        ("5", "calc_5", "5"),
        ("6", "calc_6", "6"),
        ("×", "calc_multiply", "*")
    ],

    [
        ("1", "calc_1", "1"),
        ("2", "calc_2", "2"),
        ("3", "calc_3", "3"),
        ("−", "calc_minus", "-")
    ],

    [
        ("0", "calc_0", "0"),
        (".", "calc_decimal", "."),
        ("(", "calc_left", "("),
        ("+", "calc_plus", "+")
    ],

    [
        (")", "calc_right", ")"),
        ("⌫", "calc_backspace", None),
        ("C", "calc_clear", None),
        ("=", "calc_equals", None)
    ]
]


for row in calculator_rows:

    columns = st.columns(4)

    for column, button_data in zip(columns, row):

        label, key, value = button_data

        with column:

            if key == "calc_backspace":

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=backspace_calculator
                )

            elif key == "calc_clear":

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=clear_calculator
                )

            elif key == "calc_equals":

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=calculate_result,
                    disabled=not bool(
                        st.session_state.calc_display.strip()
                    )
                )

            else:

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=add_to_calculator,
                    args=(value,)
                )


# ==========================================================
# SCIENTIFIC FUNCTIONS
# ==========================================================

st.markdown("---")

st.subheader("🔬 Scientific Functions")

st.caption(
    "sin, cos and tan use degrees."
)


scientific_rows = [

    [
        ("√", "calc_sqrt", "sqrt("),
        ("sin", "calc_sin", "sin("),
        ("cos", "calc_cos", "cos("),
        ("tan", "calc_tan", "tan(")
    ],

    [
        ("log", "calc_log", "log("),
        ("ln", "calc_ln", "ln("),
        ("π", "calc_pi", "pi"),
        ("e", "calc_e", "e")
    ]

]


for row in scientific_rows:

    columns = st.columns(4)

    for column, button_data in zip(columns, row):

        label, key, value = button_data

        with column:

            st.button(
                label,
                key=key,
                use_container_width=True,
                on_click=add_to_calculator,
                args=(value,)
            )


# ==========================================================
# SHOW RESULT
# ==========================================================

if (
    st.session_state.calc_show_result
    and st.session_state.calc_result
):

    show_calculator_result()

# ==========================================================

# Extra vertical space so this section occupies its own screen when scrolling.
st.markdown('<div style="height: 8vh;"></div>', unsafe_allow_html=True)

# GRADE CALCULATOR
# ==========================================================

st.markdown('<div id="grading" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("---")

st.title("🎓 Grade Calculator")

st.write(
    "Calculate your GPA using subject scores, "
    "subject weights, and individual class attendance."
)


if "grade_subjects" not in st.session_state:

    st.session_state.grade_subjects = [
        "Mathematics",
        "Science",
        "English"
    ]


if "subject_weights" not in st.session_state:

    st.session_state.subject_weights = {
        "Mathematics": 6,
        "Science": 4,
        "English": 5
    }


def get_letter_grade(score):

    if score >= 90:
        return "A"

    elif score >= 80:
        return "B"

    elif score >= 70:
        return "C"

    elif score >= 60:
        return "D"

    return "F"


def get_grade_points(letter):

    return {
        "A": 4.0,
        "B": 3.0,
        "C": 2.0,
        "D": 1.0,
        "F": 0.0
    }[letter]


st.subheader("📝 Enter Your Scores")

st.write(
    "Each subject uses **70% score + 30% attendance**."
)

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
                key=f"grade_score_{subject_name}"
            )

        with col2:

            attendance[subject_name] = st.number_input(
                "Classes Attended",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key=f"attendance_{subject_name}"
            )

        with col3:

            default_weight = (
                st.session_state.subject_weights.get(
                    subject_name,
                    1
                )
            )

            weights[subject_name] = st.number_input(
                "Subject Weight",
                min_value=1,
                max_value=20,
                value=default_weight,
                step=1,
                key=f"weight_{subject_name}"
            )

            st.session_state.subject_weights[
                subject_name
            ] = weights[subject_name]


# Add subject

st.markdown("---")

st.subheader("➕ Add Another Subject")

col1, col2 = st.columns([3, 1])

with col1:

    new_subject = st.text_input(
        "Subject name",
        placeholder="Example: History",
        label_visibility="collapsed"
    )

with col2:

    add_subject = st.button(
        "➕ Add",
        use_container_width=True
    )


if add_subject:

    cleaned_subject = new_subject.strip()

    if not cleaned_subject:

        st.warning(
            "Please enter a subject name."
        )

    elif cleaned_subject in st.session_state.grade_subjects:

        st.warning(
            "That subject already exists."
        )

    else:

        st.session_state.grade_subjects.append(
            cleaned_subject
        )

        st.session_state.subject_weights[
            cleaned_subject
        ] = 1

        st.rerun()


# Calculate / Reset

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    calculate = st.button(
        "🧮 Calculate GPA",
        use_container_width=True
    )

with col2:

    reset = st.button(
        "↻ Reset Everything",
        use_container_width=True
    )


# Reset

if reset:

    st.session_state.grade_subjects = [
        "Mathematics",
        "Science",
        "English"
    ]

    st.session_state.subject_weights = {
        "Mathematics": 6,
        "Science": 4,
        "English": 5
    }

    keys_to_remove = [

        key

        for key in list(st.session_state.keys())

        if key.startswith("grade_score_")
        or key.startswith("attendance_")
        or key.startswith("weight_")
    ]

    for key in keys_to_remove:
        del st.session_state[key]

    st.rerun()


# Calculate GPA

if calculate:

    total_weighted_gpa = 0
    total_weights = 0
    results = []

    for subject_name in st.session_state.grade_subjects:

        score = scores[subject_name]
        classes_attended = attendance[subject_name]
        weight = weights[subject_name]

        attendance_percentage = (
            classes_attended / 10
        ) * 100

        subject_contribution = score * 0.70

        attendance_contribution = (
            attendance_percentage * 0.30
        )

        final_subject_score = (
            subject_contribution
            + attendance_contribution
        )

        letter = get_letter_grade(
            final_subject_score
        )

        points = get_grade_points(letter)

        weighted_gpa = points * weight

        total_weighted_gpa += weighted_gpa
        total_weights += weight

        results.append({
            "subject": subject_name,
            "score": score,
            "classes_attended": classes_attended,
            "attendance_percentage":
                attendance_percentage,
            "final_score":
                final_subject_score,
            "letter": letter,
            "points": points,
            "weight": weight
        })

    final_gpa = (
        total_weighted_gpa / total_weights
    )

    st.markdown("---")

    with st.container(border=True):

        st.subheader("🎓 Your Results")

        st.metric(
            label="Overall GPA",
            value=f"{final_gpa:.2f} / 4.00"
        )

    st.subheader("📊 Subject Breakdown")

    for index, result in enumerate(results):

        subject_name = result["subject"]
        score = result["score"]
        classes_attended = result["classes_attended"]
        attendance_percentage = result["attendance_percentage"]
        final_score = result["final_score"]
        letter = result["letter"]
        points = result["points"]
        weight = result["weight"]

        with st.container(
            key=f"result_{index}",
            border=True
        ):

            st.subheader(
                f"📚 {subject_name}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"📝 Original Score: **{score}/100**"
                )

                st.write(
                    f"🏫 Classes Attended: "
                    f"**{classes_attended}/10**"
                )

                st.write(
                    f"📅 Attendance: "
                    f"**{attendance_percentage:.0f}%**"
                )

            with col2:

                st.write(
                    f"🎯 Final Score: "
                    f"**{final_score:.2f}%**"
                )

                st.write(
                    f"⚖️ Subject Weight: **{weight}**"
                )

                st.write(
                    f"🎓 GPA Points: **{points:.1f}**"
                )

            st.write(
                f"### Grade: **{letter}**"
            )

    st.subheader(
        "🧮 How Your Grade Is Calculated"
    )

    with st.container(border=True):

        st.write(
            "📝 **Subject Score = 70%**"
        )

        st.write(
            "🏫 **Attendance = 30%**"
        )

        st.write(
            "🎯 **Final Subject Score = "
            "(Score × 70%) + (Attendance × 30%)**"
        )

    st.subheader("🏫 Attendance Summary")

    for result in results:

        st.write(
            f"**{result['subject']}:** "
            f"{result['classes_attended']}/10 classes "
            f"({result['attendance_percentage']:.0f}%)"
        )

    if final_gpa >= 3.5:

        st.success(
            "🏆 Outstanding! You are doing an excellent job!"
        )

    elif final_gpa >= 3.0:

        st.success(
            "🌟 Great work! Keep pushing yourself!"
        )

    elif final_gpa >= 2.0:

        st.info(
            "👍 Good effort! Keep working to improve your grades."
        )

    elif final_gpa >= 1.0:

        st.warning(
            "📖 Keep studying and don't give up!"
        )

    else:

        st.error(
            "💪 Don't give up! There is always room to improve."
        )


# ==========================================================
# GRADING SCALE
# ==========================================================

st.markdown("---")

st.subheader("📚 Grading Scale")

st.table({

    "Letter Grade": [
        "A",
        "B",
        "C",
        "D",
        "F"
    ],

    "Percentage Range": [
        "90% – 100%",
        "80% – 89%",
        "70% – 79%",
        "60% – 69%",
        "0% – 59%"
    ],

    "Description": [
        "Outstanding / Excellent",
        "Above Average / Good",
        "Satisfactory / Average",
        "Minimum Passing",
        "Failing"
    ],

    "GPA Points": [
        "4.0",
        "3.0",
        "2.0",
        "1.0",
        "0.0"
    ]
})


# ==========================================================

# Extra vertical space so this section occupies its own screen when scrolling.
st.markdown('<div style="height: 8vh;"></div>', unsafe_allow_html=True)

# QUIZ MASTER
# ==========================================================

st.markdown('<div id="quiz-maker" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("---")

st.title("🧠 Quiz Master")

st.write(
    "Create your own quiz with as many questions as you want."
)


# ==========================================================
# QUIZ STATE
# ==========================================================

if "quiz_questions" not in st.session_state:

    st.session_state.quiz_questions = []


if "quiz_started" not in st.session_state:

    st.session_state.quiz_started = False


if "quiz_finished" not in st.session_state:

    st.session_state.quiz_finished = False


if "quiz_answers" not in st.session_state:

    st.session_state.quiz_answers = {}


# ==========================================================
# ADD QUESTION
# ==========================================================

st.subheader("✏️ Build Your Quiz")

if st.button(
    "➕ Add Question",
    use_container_width=True
):

    st.session_state.quiz_questions.append({

        "question": "",

        "A": "",

        "B": "",

        "C": "",

        "D": "",

        "correct": "A"

    })

    st.rerun()


# ==========================================================
# QUESTION BUILDER
# ==========================================================

for i, question in enumerate(
    st.session_state.quiz_questions
):

    with st.container(border=True):

        st.subheader(
            f"Question {i + 1}"
        )

        question["question"] = st.text_input(
            "❓ Question",
            value=question["question"],
            placeholder="Enter your question...",
            key=f"quiz_question_{i}"
        )

        st.write("### 🔤 Choices")

        question["A"] = st.text_input(
            "Choice A",
            value=question["A"],
            placeholder="Enter choice A",
            key=f"quiz_choice_a_{i}"
        )

        question["B"] = st.text_input(
            "Choice B",
            value=question["B"],
            placeholder="Enter choice B",
            key=f"quiz_choice_b_{i}"
        )

        question["C"] = st.text_input(
            "Choice C",
            value=question["C"],
            placeholder="Enter choice C",
            key=f"quiz_choice_c_{i}"
        )

        question["D"] = st.text_input(
            "Choice D",
            value=question["D"],
            placeholder="Enter choice D",
            key=f"quiz_choice_d_{i}"
        )

        question["correct"] = st.selectbox(
            "✅ Which option is correct?",
            ["A", "B", "C", "D"],
            index=["A", "B", "C", "D"].index(
                question["correct"]
            ),
            key=f"quiz_correct_{i}"
        )

        if st.button(
            "🗑️ Remove Question",
            key=f"remove_quiz_question_{i}",
            use_container_width=True
        ):

            st.session_state.quiz_questions.pop(i)

            st.rerun()


# ==========================================================
# QUIZ CONTROLS
# ==========================================================

if len(st.session_state.quiz_questions) > 0:

    st.markdown("---")

    st.write(
        f"📋 **{len(st.session_state.quiz_questions)} "
        f"question(s) created**"
    )

    quiz_ready = True

    for question in st.session_state.quiz_questions:

        if not question["question"].strip():
            quiz_ready = False

        if not question["A"].strip():
            quiz_ready = False

        if not question["B"].strip():
            quiz_ready = False

        if not question["C"].strip():
            quiz_ready = False

        if not question["D"].strip():
            quiz_ready = False


    if not quiz_ready:

        st.warning(
            "Please fill in the question and all four choices."
        )


    if st.button(
        "▶️ Start Quiz",
        use_container_width=True,
        disabled=not quiz_ready
    ):

        st.session_state.quiz_started = True
        st.session_state.quiz_finished = False
        st.session_state.quiz_answers = {}

        st.rerun()


# ==========================================================
# TAKE QUIZ
# ==========================================================

if (
    st.session_state.quiz_started
    and len(st.session_state.quiz_questions) > 0
):

    st.markdown("---")

    st.title("📝 Take the Quiz")

    st.write(
        "Choose one answer for every question."
    )


    for i, question in enumerate(
        st.session_state.quiz_questions
    ):

        with st.container(border=True):

            st.subheader(
                f"{i + 1}. {question['question']}"
            )

            choices = [
                f"A. {question['A']}",
                f"B. {question['B']}",
                f"C. {question['C']}",
                f"D. {question['D']}"
            ]

            selected = st.radio(
                "Choose your answer:",
                choices,
                key=f"quiz_answer_{i}"
            )

            st.session_state.quiz_answers[i] = (
                selected[0]
            )


    # ======================================================
    # SUBMIT QUIZ
    # ======================================================

    if st.button(
        "🎯 Submit Quiz",
        use_container_width=True
    ):

        score = 0

        for i, question in enumerate(
            st.session_state.quiz_questions
        ):

            user_answer = (
                st.session_state.quiz_answers.get(i)
            )

            if user_answer == question["correct"]:

                score += 1


        total = len(
            st.session_state.quiz_questions
        )

        percentage = (
            score / total
        ) * 100

        st.session_state.quiz_score = score
        st.session_state.quiz_total = total
        st.session_state.quiz_percentage = percentage
        st.session_state.quiz_finished = True
        st.session_state.quiz_started = False

        st.rerun()


# ==========================================================
# QUIZ RESULT POPUP
# ==========================================================

# ==========================================================
# QUIZ RESULT
# ==========================================================

if st.session_state.quiz_finished:

    @st.dialog("🎉 Quiz Complete!")
    def show_quiz_result():

        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        percentage = st.session_state.quiz_percentage

        st.subheader("Your Quiz Results")

        st.write("")

        # Score
        st.metric(
            "🏆 Score",
            f"{score} / {total}"
        )

        # Percentage
        st.metric(
            "📊 Percentage",
            f"{percentage:.0f}%"
        )

        st.markdown("---")

        # Message based on score
        if percentage == 100:

            st.success(
                "🏆 Perfect score! You got every question correct!"
            )

        elif percentage >= 80:

            st.success(
                "🌟 Excellent work! You really know your stuff!"
            )

        elif percentage >= 60:

            st.info(
                "👍 Good job! Keep practicing!"
            )

        elif percentage >= 40:

            st.warning(
                "📚 Not bad! Keep studying and try again!"
            )

        else:

            st.error(
                "💪 Keep practicing! You can do better next time!"
            )

        st.markdown("---")

        if st.button(
            "✓ Done",
            use_container_width=True
        ):

            st.session_state.quiz_finished = False
            st.session_state.quiz_answers = {}

            st.rerun()

    show_quiz_result()

