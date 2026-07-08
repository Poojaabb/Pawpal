import streamlit as st

# Step 1: Establish the connection — bring the logic layer into the UI.
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+. This UI is now wired to the logic layer in `pawpal_system.py`.
Add pets and tasks below — they are stored as real `Pet` and `Task` objects that
persist in memory for the whole session.
"""
)

# Step 2: Manage application "memory".
# Streamlit re-runs this script top-to-bottom on every interaction, so we keep a
# single Owner instance in st.session_state instead of rebuilding it each run.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

owner: Owner = st.session_state.owner

st.divider()

# --- Owner info ---------------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = st.number_input(
    "Time available today (minutes)",
    min_value=0,
    max_value=1440,
    value=owner.available_minutes,
)

st.divider()

# --- Step 3: Wire "Add a Pet" to Owner.add_pet -------------------------------
st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=1)
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    owner.add_pet(Pet(name=pet_name, species=species, breed=breed, age=int(age)))
    st.success(f"Added {pet_name} ({species}).")

pets = owner.list_pets()
if pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": p.name, "species": p.species, "breed": p.breed, "age": p.age,
             "tasks": len(p.list_tasks())}
            for p in pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Step 3: Wire "Add a Task" to Pet.add_task -------------------------------
st.subheader("Tasks")
if not pets:
    st.info("Add a pet first, then you can add tasks for it.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names = [p.name for p in pets]
        selected_pet_name = st.selectbox("For which pet?", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        # Find the selected Pet object and attach the new Task to it.
        target_pet = next(p for p in pets if p.name == selected_pet_name)
        target_pet.add_task(
            Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet_name}.")

    # Show every task across all pets.
    all_tasks = owner.all_tasks()
    if all_tasks:
        st.write("All tasks:")
        st.table(
            [
                {"title": t.title, "duration_minutes": t.duration_minutes,
                 "priority": t.priority}
                for t in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Scheduling (next phase) --------------------------------------------------
st.subheader("Build Schedule")
st.caption("Scheduling logic is implemented in the next phase.")

if st.button("Generate schedule"):
    st.warning(
        "Scheduling not implemented yet. Next phase: implement Scheduler.build_plan() "
        "and call it here with owner.all_tasks()."
    )
