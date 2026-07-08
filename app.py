from datetime import date, time

import streamlit as st

# Bring the smart logic layer into the UI.
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown(
    "Plan your pets' daily care. Add pets and tasks below, then view a "
    "time-sorted schedule with automatic **conflict warnings**."
)

# --- Application "memory" -----------------------------------------------------
# Streamlit re-runs top-to-bottom on every interaction, so keep one Owner in
# session_state instead of rebuilding it each run.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

owner: Owner = st.session_state.owner
scheduler = Scheduler(available_minutes=owner.available_minutes)

st.divider()

# --- Owner info ---------------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = st.number_input(
    "Time available today (minutes)", min_value=0, max_value=1440,
    value=owner.available_minutes,
)

st.divider()

# --- Add a pet ----------------------------------------------------------------
st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=1)
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=pet_name, species=species, breed=breed, age=int(age)))
        st.success(f"Added {pet_name} ({species}).")

pets = owner.list_pets()
if pets:
    st.table(
        [
            {"name": p.name, "species": p.species, "breed": p.breed or "-",
             "age": p.age, "tasks": len(p.list_tasks())}
            for p in pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task ---------------------------------------------------------------
st.subheader("Tasks")
if not pets:
    st.info("Add a pet first, then you can add tasks for it.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_name = st.selectbox("For which pet?", [p.name for p in pets])
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        col3, col4 = st.columns(2)
        with col3:
            has_time = st.checkbox("Schedule at a specific time?", value=True)
            start = st.time_input("Start time", value=time(8, 0), disabled=not has_time)
        with col4:
            frequency = st.selectbox("Repeats", ["none", "daily", "weekly"])

        if st.form_submit_button("Add task"):
            target_pet = next(p for p in pets if p.name == selected_pet_name)
            target_pet.add_task(
                Task(
                    title=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                    time=start.strftime("%H:%M") if has_time else "",
                    frequency=frequency,
                    due_date=date.today() if frequency != "none" else None,
                )
            )
            st.success(f"Added '{task_title}' to {selected_pet_name}.")

st.divider()

# --- Today's schedule (sorting + conflict warnings) ---------------------------
st.subheader("📅 Today's Schedule")

if not owner.all_tasks():
    st.info("No tasks scheduled yet.")
else:
    # Optional filter by pet.
    view = st.selectbox("Show tasks for", ["All pets"] + [p.name for p in pets])
    if view == "All pets":
        tasks = owner.all_tasks()
    else:
        tasks = owner.tasks_for_pet(view)

    # Map each task object back to its pet name for display.
    pet_of = {id(t): p.name for p in pets for t in p.list_tasks()}

    ordered = scheduler.sort_by_time(tasks)
    st.table(
        [
            {
                "time": t.time or "unscheduled",
                "pet": pet_of.get(id(t), "-"),
                "task": t.title,
                "duration": f"{t.duration_minutes} min",
                "priority": t.priority,
                "repeats": t.frequency,
                "status": "✅ done" if t.completed else "⬜ todo",
            }
            for t in ordered
        ]
    )

    # Conflict warnings — surfaced clearly so the owner can act on them.
    warnings = scheduler.conflict_warnings(tasks)
    if warnings:
        for message in warnings:
            st.warning(message)
    else:
        st.success("No scheduling conflicts. 🎉")
