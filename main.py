"""PawPal+ terminal demo.

Exercises the Phase 4 algorithmic layer directly (no Streamlit):
  - sorting tasks by time
  - filtering by status and by pet
  - recurring tasks (daily/weekly) via mark_complete()
  - basic conflict detection

Run it with:  python main.py
"""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def show(tasks):
    """Pretty-print a list of tasks."""
    if not tasks:
        print("   (none)")
        return
    for t in tasks:
        when = t.time or "  --  "
        status = "done" if t.completed else "todo"
        print(
            f"   {when}  {t.title:<16} {t.duration_minutes:>3} min  "
            f"[{t.priority:<6}] ({status})"
        )


def main() -> None:
    # --- Set up an owner with two pets -------------------------------------
    owner = Owner(name="Jordan", available_minutes=180)
    biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    mochi = Pet(name="Mochi", species="cat", breed="Tabby", age=2)
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # --- Add tasks deliberately OUT OF ORDER -------------------------------
    biscuit.add_task(Task("Evening walk", 30, "high", "exercise", time="18:00",
                          frequency="daily", due_date=date(2026, 7, 7)))
    biscuit.add_task(Task("Morning walk", 30, "high", "exercise", time="08:00",
                          frequency="daily", due_date=date(2026, 7, 7)))
    biscuit.add_task(Task("Feeding", 10, "high", "food", time="08:15"))  # overlaps walk
    mochi.add_task(Task("Litter cleanup", 10, "medium", "hygiene", time="12:00"))
    mochi.add_task(Task("Medication", 5, "high", "meds", time="12:00"))  # SAME time as cleanup
    mochi.add_task(Task("Play/enrichment", 15, "low", "enrichment"))  # no time set

    scheduler = Scheduler(available_minutes=owner.available_minutes)
    tasks = owner.all_tasks()

    print("=== All tasks (insertion order) ===")
    show(tasks)

    # --- Sorting by time ---------------------------------------------------
    print("\n=== Sorted by time (unscheduled last) ===")
    show(scheduler.sort_by_time(tasks))

    # --- Sorting by priority ----------------------------------------------
    print("\n=== Sorted by priority (high first) ===")
    show(scheduler.sort_by_priority(tasks))

    # --- Filtering by pet --------------------------------------------------
    print("\n=== Filter: only Mochi's tasks ===")
    show(owner.tasks_for_pet("Mochi"))

    # --- Conflict detection (lightweight warnings, no crash) ---------------
    print("\n=== Conflict warnings ===")
    warnings = scheduler.conflict_warnings(tasks)
    if not warnings:
        print("   No conflicts.")
    for message in warnings:
        print(f"   {message}")

    # --- Recurring tasks ---------------------------------------------------
    print("\n=== Recurring: complete Biscuit's daily 'Morning walk' ===")
    morning = next(t for t in biscuit.list_tasks() if t.title == "Morning walk")
    next_occurrence = morning.mark_complete()
    print(f"   Original due {morning.due_date} -> completed={morning.completed}")
    if next_occurrence:
        biscuit.add_task(next_occurrence)
        print(f"   Auto-created next occurrence due {next_occurrence.due_date}")

    # --- Filtering by status (after completing one) ------------------------
    print("\n=== Filter: incomplete (todo) tasks only ===")
    show(scheduler.filter_by_status(owner.all_tasks(), completed=False))

    print("\n=== Filter: completed tasks only ===")
    show(scheduler.filter_by_status(owner.all_tasks(), completed=True))


if __name__ == "__main__":
    main()
