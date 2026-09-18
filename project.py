import streamlit as st
import os
import base64

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
# YOUR STREAMLIT APP GOES BELOW THIS LINE
# ==========================================================

st.title("🎓 My Streamlit App")

st.write("Your custom live video background is working!")

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="My Profile & Grade Calculator",
    page_icon="🎓",
    layout="centered"\
)


# ==========================================================
# APPLE-STYLE UI
# ==========================================================

st.markdown("""
<style>

.stApp {
    color: #f5f5f7;
}

.block-container {
    max-width: 900px;
    padding-top: 45px;
    padding-bottom: 60px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(30, 30, 32, 0.90) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 22px !important;
    padding: 8px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}


/* Larger, brighter Grading Scale */
div[data-testid="stTable"] table {
    font-size: 20px !important;
    background: rgba(25, 25, 28, 0.96) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}

div[data-testid="stTable"] th {
    color: #ffffff !important;
    background: rgba(55, 55, 60, 0.98) !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    padding: 16px 14px !important;
}

div[data-testid="stTable"] td {
    color: #ffffff !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    padding: 15px 14px !important;
    background: rgba(35, 35, 38, 0.96) !important;
}

div[data-testid="stTable"] tr {
    border-bottom: 1px solid rgba(255,255,255,0.16) !important;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

.stTextInput input,
.stNumberInput input {
    background: rgba(30,30,32,0.90) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    font-size: 16px !important;
    padding: 12px !important;
}

.stButton > button {
    background: rgba(40,40,43,0.95) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    min-height: 48px;
    font-weight: 600 !important;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: rgba(65,65,70,0.98) !important;
    border-color: rgba(255,255,255,0.35) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.18) !important;
    margin: 40px 0 !important;
}

.stAlert {
    background: rgba(30,30,32,0.90) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    backdrop-filter: blur(15px);
}

@keyframes profilePopup {
    0% {
        opacity: 0;
        transform: scale(0.75) translateY(40px);
        filter: blur(10px);
    }
    50% {
        opacity: 0.8;
        transform: scale(1.04) translateY(-5px);
        filter: blur(2px);
    }
    75% {
        opacity: 1;
        transform: scale(0.98) translateY(2px);
        filter: blur(0);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
        filter: blur(0);
    }
}

[data-testid="stDialog"] {
    animation: profilePopup 0.6s cubic-bezier(0.22,1,0.36,1);
}

[data-testid="stDialog"] > div {
    background: rgba(25,25,28,0.98) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 28px !important;
    box-shadow: 0 30px 80px rgba(0,0,0,0.7) !important;
}

@keyframes resultPop {
    0% {
        opacity: 0;
        transform: scale(0.7);
    }
    60% {
        opacity: 1;
        transform: scale(1.08);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes whooshIn {
    0% {
        opacity: 0;
        transform: translateX(-120px) scale(0.96);
        filter: blur(10px);
    }
    40% {
        opacity: 0.7;
        transform: translateX(15px) scale(1.01);
        filter: blur(3px);
    }
    70% {
        opacity: 1;
        transform: translateX(-4px) scale(1);
        filter: blur(0);
    }
    100% {
        opacity: 1;
        transform: translateX(0) scale(1);
        filter: blur(0);
    }
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# NAVIGATION SYSTEM
# ==========================================================

# Small navigation bar that jumps to each section.
# The sections remain on the same page, so normal scrolling
# still works too.

st.markdown("""
<style>

/* Smooth scrolling when using the navigation links */
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.block-container {
    scroll-behavior: smooth !important;
    scroll-padding-top: 120px !important;
}

/* Keep section targets from stopping underneath the sticky navigation */
.section-anchor {
    scroll-margin-top: 120px !important;
}

.navigation-bar {
    position: sticky;
    top: 10px;
    z-index: 999;
    background: rgba(25, 25, 28, 0.96);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 18px;
    padding: 10px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

.navigation-title {
    text-align: center;
    color: #ffffff;
    font-weight: 800;
    font-size: 13px;
    margin-bottom: 8px;
}

.navigation-link {
    display: block;
    text-align: center;
    text-decoration: none !important;
    color: #ffffff !important;
    background: rgba(55,55,60,0.95);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 10px 4px;
    font-size: 13px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.navigation-link:hover {
    background: rgba(80,80,86,0.98);
    transform: translateY(-2px);
}

.section-anchor {
    scroll-margin-top: 100px;
}

</style>
""", unsafe_allow_html=True)


# Navigation bar
st.markdown("""
<div class="navigation-bar">
    <div class="navigation-title">QUICK NAVIGATION</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">
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
st.markdown('<div style="height: 70vh;"></div>', unsafe_allow_html=True)

# SCIENTIFIC CALCULATOR
# ==========================================================

st.markdown('<div id="calculator" class="section-anchor"></div>', unsafe_allow_html=True)

st.markdown("---")

st.title("🧮 Scientific Calculator")

st.write(
    "A simple scientific calculator with powerful functions."
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
    st.session_state.calc_display = (
        st.session_state.calc_display[:-1]
    )
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

        result = eval(
            expression,
            {"__builtins__": {}},
            allowed
        )

        if isinstance(result, float):

            if result.is_integer():
                result = str(int(result))
            else:
                result = str(round(result, 10))

        else:
            result = str(result)

        st.session_state.calc_result = result

    except ZeroDivisionError:

        st.session_state.calc_result = (
            "Error: Cannot divide by zero"
        )

    except Exception:

        st.session_state.calc_result = (
            "Error: Invalid calculation"
        )


@st.dialog("🧮 Calculation Result")
def show_calculator_result():

    st.subheader("Your calculation")

    st.write("Expression")

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
            padding:20px;
            font-size:42px;
            font-weight:700;
            color:white;
            background:rgba(45,45,48,0.8);
            border-radius:20px;
            margin:10px 0 25px 0;
            animation:resultPop 0.5s ease-out;
        ">
            {st.session_state.calc_result}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("✓ Done", use_container_width=True):

        st.session_state.calc_result = ""

        st.rerun()


st.text_input(
    "Calculator Display",
    value=st.session_state.calc_display,
    disabled=True,
    label_visibility="collapsed"
)


# Calculator buttons

calculator_rows = [
    [
        ("7", "seven", "7"),
        ("8", "eight", "8"),
        ("9", "nine", "9"),
        ("÷", "divide", "/")
    ],
    [
        ("4", "four", "4"),
        ("5", "five", "5"),
        ("6", "six", "6"),
        ("×", "multiply", "*")
    ],
    [
        ("1", "one", "1"),
        ("2", "two", "2"),
        ("3", "three", "3"),
        ("-", "minus", "-")
    ],
    [
        ("0", "zero", "0"),
        (".", "decimal", "."),
        ("(", "left_parenthesis", "("),
        ("+", "plus", "+")
    ],
    [
        (")", "right_parenthesis", ")"),
        ("⌫", "backspace", None),
        ("C", "clear", None),
        ("=", "equals", None)
    ]
]


for row in calculator_rows:

    columns = st.columns(4)

    for column, button_data in zip(columns, row):

        label, key, value = button_data

        with column:

            if key == "backspace":

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=backspace_calculator
                )

            elif key == "clear":

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=clear_calculator
                )

            elif key == "equals":

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=calculate_result
                )

            else:

                st.button(
                    label,
                    key=key,
                    use_container_width=True,
                    on_click=add_to_calculator,
                    args=(value,)
                )


# Scientific functions

st.markdown("---")

st.subheader("🔬 Scientific Functions")

scientific_rows = [
    [
        ("√", "sqrt", "sqrt("),
        ("sin", "sin", "sin("),
        ("cos", "cos", "cos("),
        ("tan", "tan", "tan(")
    ],
    [
        ("log", "log", "log("),
        ("ln", "ln", "ln("),
        ("π", "pi", "pi"),
        ("e", "e", "e")
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


if st.session_state.calc_result:
    show_calculator_result()


# ==========================================================

# Extra vertical space so this section occupies its own screen when scrolling.
st.markdown('<div style="height: 70vh;"></div>', unsafe_allow_html=True)

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
st.markdown('<div style="height: 70vh;"></div>', unsafe_allow_html=True)

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

