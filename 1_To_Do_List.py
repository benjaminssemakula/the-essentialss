from uuid import uuid4

import streamlit as st

from essentials_theme import apply_theme, require_profile

apply_theme("To Do List", "📝")
require_profile()

st.title("To do List")
st.markdown(
    '<p class="lede">Add a task, confirm it, then tick it off when it is done.</p>',
    unsafe_allow_html=True,
)

if "todo_items" not in st.session_state:
    st.session_state.todo_items = []
if "todo_empty_warning" not in st.session_state:
    st.session_state.todo_empty_warning = False


def add_todo_task():
    text = st.session_state.todo_input.strip()
    if not text:
        st.session_state.todo_empty_warning = True
        return
    st.session_state.todo_items.append({"id": uuid4().hex[:8], "text": text, "done": False})
    st.session_state.todo_input = ""
    st.session_state.todo_empty_warning = False


def toggle_todo_task(task_id):
    for task in st.session_state.todo_items:
        if task["id"] == task_id:
            task["done"] = st.session_state[f"todo_done_{task_id}"]


def clear_done_todos():
    st.session_state.todo_items = [t for t in st.session_state.todo_items if not t["done"]]


with st.container(border=True):
    st.subheader("Add a task")
    st.text_input(
        "Task",
        placeholder="What do you need to do?",
        key="todo_input",
        label_visibility="collapsed",
    )
    st.button(
        "Confirm task",
        key="todo_confirm",
        use_container_width=True,
        type="primary",
        on_click=add_todo_task,
    )
    if st.session_state.todo_empty_warning:
        st.warning("Type a task first.")

todo_total = len(st.session_state.todo_items)
todo_done = sum(1 for t in st.session_state.todo_items if t["done"])

with st.container(border=True):
    st.subheader("Your progress")
    if todo_total == 0:
        st.progress(0.0, text="No tasks yet")
    else:
        st.progress(
            todo_done / todo_total,
            text=f"{todo_done} of {todo_total} completed · {round(todo_done / todo_total * 100)}%",
        )
        if todo_done == todo_total:
            st.success("All tasks completed. Great job.")

with st.container(border=True):
    st.subheader("Your tasks")
    if not st.session_state.todo_items:
        st.markdown(
            '<p class="lede" style="margin:0">Nothing here yet. Add your first task above.</p>',
            unsafe_allow_html=True,
        )
    for task in st.session_state.todo_items:
        st.checkbox(
            f"~~{task['text']}~~" if task["done"] else task["text"],
            value=task["done"],
            key=f"todo_done_{task['id']}",
            on_change=toggle_todo_task,
            args=(task["id"],),
        )
    if todo_done:
        st.button("Remove completed tasks", key="todo_clear_done", use_container_width=True, on_click=clear_done_todos)
