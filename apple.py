"""Adds the To Do List and Money Manager nav links + home cards to your Essentials app.

Usage (run in the folder that has your file):
    python apply_patch.py project.py

A backup is saved as project.py.bak before anything is changed.
"""
import shutil
import sys
from pathlib import Path

target = Path(sys.argv[1] if len(sys.argv) > 1 else "project.py")
source = target.read_text(encoding="utf-8")

if "_todo_art" in source:
    sys.exit("Already patched - nothing to do.")

ART = '''_todo_art = (
    '<div class="portal-art art-todo">'
    '<div class="t done"><b>✓</b><span>Finish homework</span></div>'
    '<div class="t done"><b>✓</b><span>Pack school bag</span></div>'
    '<div class="t"><b></b><span>Study for quiz</span></div>'
    '<div class="bar"><i></i></div></div>'
)
_money_art = (
    '<div class="portal-art art-money"><div class="lbl">Remaining balance</div>'
    '<div class="amt">Rp 250 000</div>'
    '<div class="row"><span>Allowance</span><b class="in">+ 300 000</b></div>'
    '<div class="row"><span>Lunch</span><b class="out">- 50 000</b></div></div>'
)


'''

PORTAL_DEF = "def _portal(i, href, eyebrow, title, copy, sub, art, light=False):"

OLD_GAME_PORTAL = (
    '"Five difficulty levels. Your attempts, your challenge.", _game_art, light=True)\n'
    '    + "</div>",'
)
NEW_GAME_PORTAL = (
    '"Five difficulty levels. Your attempts, your challenge.", _game_art, light=True)\n'
    '    + _portal(4, "todo", "Stay on track", "To Do List",\n'
    '              "Add tasks and tick them off.",\n'
    '              "Watch your progress bar fill up.", _todo_art)\n'
    '    + _portal(5, "money", "Allowance tracker", "Money Manager",\n'
    '              "Record what you get and what you spend.",\n'
    '              "Download your history anytime.", _money_art, light=True)\n'
    '    + "</div>",'
)

edits = [
    (
        "nav_column_count = 5 if st.session_state.profile_complete else 6",
        "nav_column_count = 7 if st.session_state.profile_complete else 8",
    ),
    (
        'nav_link("number-game", "Guess Game"),',
        'nav_link("number-game", "Guess Game"),\n'
        '        nav_link("todo", "To-Do"),\n'
        '        nav_link("money", "Money"),',
    ),
    (PORTAL_DEF, ART + PORTAL_DEF),
    (OLD_GAME_PORTAL, NEW_GAME_PORTAL),
]

for old, new in edits:
    if source.count(old) != 1:
        sys.exit(f"Could not find this exactly once, nothing was changed:\n{old[:80]}")
    source = source.replace(old, new)

shutil.copy(target, target.with_name(target.name + ".bak"))
target.write_text(source, encoding="utf-8")
print(f"Done. Patched {target} (backup: {target.name}.bak)")
