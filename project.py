import base64
import math
import os
from uuid import uuid4

import streamlit as st
import streamlit.components.v1 as components

# ==========================================================
# PAGE CONFIG  (first Streamlit call, only once)
# ==========================================================

st.set_page_config(
    page_title="My Profile & Grade Calculator",
    page_icon="🎓",
    layout="centered",
)


APP_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(APP_DIR, "background.mp4")


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
# NAVIGATION
# ==========================================================

st.markdown(
    """
<div class="navigation-bar">
    <a class="navigation-link" href="#profile" data-smooth="profile">Profile</a>
    <a class="navigation-link" href="#calculator" data-smooth="calculator">Calculator</a>
    <a class="navigation-link" href="#grading" data-smooth="grading">Grades</a>
    <a class="navigation-link" href="#quiz-maker" data-smooth="quiz-maker">Quiz</a>
</div>
""",
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

    const reduced = () => !win.__smoothNavForce && win.matchMedia('(prefers-reduced-motion: reduce)').matches;
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

        if (reduced()) {
            if (usesWindow) win.scrollTo(0, win.scrollY + distance);
            else scroller.scrollTop += distance;
            restore();
            return;
        }

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

        win.__smoothNavDebug.clicks += 1;
        win.__smoothNavDebug.lastLink = link.getAttribute('data-smooth');
        win.__smoothNavDebug.lastClickAt = new Date().toLocaleTimeString();

        const target = doc.getElementById(link.getAttribute('data-smooth'));
        if (!target) {
            win.__smoothNavDebug.lastOutcome = 'target id not found';
            return;
        }

        event.preventDefault();
        win.__smoothNavDebug.lastOutcome = 'scrolling…';
        scrollToTarget(target);
    }, true);

    /* Small readout for the troubleshooting expander, if it's open. */
    win.__smoothNavDebug = win.__smoothNavDebug || { clicks: 0, lastLink: null, lastClickAt: null, lastOutcome: null };

    win.__smoothNavReport = function () {
        const target = doc.getElementById('calculator');
        const scrollerLine = (function () {
            if (!target) return 'anchor not found';
            const scroller = findScroller(target);
            return (scroller.tagName.toLowerCase()
                + (scroller.getAttribute && scroller.getAttribute('data-testid') ? '[' + scroller.getAttribute('data-testid') + ']' : '')
                + ' — scrollHeight ' + scroller.scrollHeight + ', clientHeight ' + scroller.clientHeight);
        })();

        const debug = win.__smoothNavDebug;

        return scrollerLine
            + ' | reduce-motion: ' + reduced()
            + (win.__smoothNavForce ? ' (overridden ON)' : '')
            + ' | nav clicks seen: ' + debug.clicks
            + (debug.lastLink ? ' | last: ' + debug.lastLink + ' at ' + debug.lastClickAt : '');
    };
})();
</script>
""",
    height=0,
)


# ==========================================================
# PROFILE
# ==========================================================

st.markdown('<div id="profile" class="section-anchor"></div>', unsafe_allow_html=True)

st.title("Profile")
st.markdown(
    '<p class="lede">Tell us a little about yourself.</p>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    school = st.text_input("School")
    favorite_subject = st.text_input("Favorite subject")
    hobby = st.text_input("Favorite hobby")


@st.dialog("Profile created")
def show_profile_popup():
    st.subheader(f"Welcome, {name}")

    st.markdown("---")
    st.write(f"**Age** — {age}")
    st.write(f"**School** — {school}")
    st.write(f"**Favorite subject** — {favorite_subject}")
    st.write(f"**Favorite hobby** — {hobby}")
    st.markdown("---")

    if st.button("Done", use_container_width=True, type="primary"):
        st.rerun()


if st.button("Create profile", use_container_width=True, type="primary"):
    if name and school and favorite_subject and hobby:
        show_profile_popup()
    else:
        st.warning("Fill in every field to create your profile.")


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


st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    calculate = st.button("Calculate GPA", use_container_width=True, type="primary")

with col2:
    reset = st.button("Reset everything", use_container_width=True)


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

    if final_gpa >= 3.5:
        st.success("Outstanding work. Keep it up.")
    elif final_gpa >= 3.0:
        st.success("Great results. Keep pushing.")
    elif final_gpa >= 2.0:
        st.info("Solid effort. There's room to climb.")
    elif final_gpa >= 1.0:
        st.warning("Keep studying — steady progress adds up.")
    else:
        st.error("Plenty of room to improve. Start with one subject.")


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


# ==========================================================
# TROUBLESHOOTING
# Open this if the navigation ever stops scrolling smoothly —
# it reports which element the page is actually scrolling.
# ==========================================================

with st.expander("Navigation troubleshooting"):
    st.markdown(
        '<p class="lede" style="margin-bottom:12px">'
        "This shows which element the page is scrolling, whether your click "
        "reached the script, and whether your system has reduce-motion turned "
        "on — that setting forces an instant jump instead of an animation.</p>",
        unsafe_allow_html=True,
    )

    force_animation = st.toggle(
        "Animate even if my system prefers reduced motion",
        value=True,
        help="On by default: a nav click is a deliberate action, not incidental "
        "motion, so it animates even when your OS has reduce-motion on. Turn "
        "this off to respect that setting instead.",
    )

    components.html(
        f"""
<div style="font:13px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;
            color:rgba(255,255,255,0.88);padding:2px 0;line-height:1.6;">
    <span id="report">checking…</span>
</div>
<script>
(function () {{
    window.parent.__smoothNavForce = {str(force_animation).lower()};
    const output = document.getElementById('report');
    function update() {{
        try {{
            output.textContent = window.parent.__smoothNavReport
                ? window.parent.__smoothNavReport()
                : 'navigation script did not load';
        }} catch (error) {{
            output.textContent = 'blocked from reading the page: ' + error.message;
        }}
    }}
    setInterval(update, 500);
    update();
}})();
</script>
""",
        height=40,
    )
