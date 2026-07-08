# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Owner & pet management** — an `Owner` can have multiple `Pet`s, and each pet keeps its own list of care `Task`s.
- **Task details** — every task has a title, duration, priority, optional start time (`HH:MM`), and a repeat frequency.
- **Sorting by time** — `Scheduler.sort_by_time()` orders the day chronologically (unscheduled tasks last).
- **Sorting by priority** — `Scheduler.sort_by_priority()` puts high-priority tasks first, shorter tasks breaking ties.
- **Filtering** — by completion status (`Scheduler.filter_by_status()`) or by pet (`Owner.tasks_for_pet()`).
- **Conflict warnings** — `Scheduler.conflict_warnings()` flags exact same-time clashes and run-over overlaps with friendly messages (never crashes).
- **Daily / weekly recurrence** — completing a recurring task (`Task.mark_complete()`) auto-creates the next occurrence using `datetime.timedelta`.
- **Two front-ends** — an interactive Streamlit UI (`app.py`) and a terminal demo (`main.py`).

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

A day sorted by time, with conflict warnings, produced by `python main.py`:

```
=== Sorted by time (unscheduled last) ===
   08:00  Morning walk      30 min  [high  ] (todo)
   08:15  Feeding           10 min  [high  ] (todo)
   12:00  Litter cleanup    10 min  [medium] (todo)
   12:00  Medication         5 min  [high  ] (todo)
   18:00  Evening walk      30 min  [high  ] (todo)
     --    Play/enrichment   15 min  [low   ] (todo)

=== Conflict warnings ===
   WARNING: 'Morning walk' (08:00, 30 min) runs into 'Feeding' at 08:15.
   WARNING: 'Litter cleanup' and 'Medication' are both scheduled at 12:00.
```

## 🧪 Testing PawPal+

The automated test suite lives in `tests/test_pawpal.py` (18 tests). Run it with:

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

**What the tests cover:**

- **Sorting** — tasks come back in chronological order (unscheduled last), priority sort puts high first with shorter tasks breaking ties, and sorting doesn't mutate the input list.
- **Filtering** — by completion status (done vs. todo) and by pet name (including an unknown pet returning an empty list).
- **Recurring tasks** — completing a `daily` task creates a fresh task due the next day, `weekly` advances 7 days, and a one-off task returns `None`.
- **Conflict detection** — exact same-time clashes and run-over overlaps are flagged, while spaced-out and unscheduled tasks are not.
- **Edge cases** — a pet with no tasks, an owner with no pets, and sorting an empty list all behave safely.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.1.1, pluggy-1.6.0
collected 18 items

tests\test_pawpal.py ..................                                  [100%]

============================= 18 passed in 0.06s ==============================
```

**Confidence Level: ⭐⭐⭐⭐☆ (4/5)** — every core behavior (sorting, filtering, recurrence, conflict detection) is covered and passing. Dropping one star because conflict detection only compares time-adjacent tasks (see the tradeoff noted in `reflection.md` §2b), and `Scheduler.build_plan()` / `explain()` are not yet implemented or tested.

## 📐 Smarter Scheduling

PawPal+ adds a small algorithmic layer in `pawpal_system.py`. All of it is
demonstrated end-to-end by the CLI demo in `main.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | `sort_by_time()` sorts by `"HH:MM"` start time (unscheduled tasks go last); `sort_by_priority()` orders high→low priority with shorter tasks breaking ties |
| Filtering | `Scheduler.filter_by_status()`, `Owner.tasks_for_pet()` | Filter by completion status (done vs. todo) or by which pet a task belongs to |
| Conflict handling | `Scheduler.find_conflicts()`, `Scheduler.conflict_warnings()` | Sorts by time and flags any task whose slot overlaps the next; `conflict_warnings()` returns friendly warning strings instead of raising, so a clash never crashes the app |
| Recurring tasks | `Task.mark_complete()` (uses `frequency` + `due_date`) | Completing a `"daily"`/`"weekly"` task auto-creates the next occurrence with its `due_date` advanced via `datetime.timedelta` |

## 📸 Demo Walkthrough

### The Streamlit app (`streamlit run app.py`)

The UI is organized top-to-bottom so a pet owner can build a full day in a few clicks:

1. **Owner** — set your name and how many minutes you have available today.
2. **Pets** — fill the "Add pet" form (name, species, breed, age) and submit. Each pet appears in a table showing how many tasks it has. Add as many pets as you like.
3. **Tasks** — pick a pet, then add a task with a title, duration, priority, an optional start time, and a repeat setting (none / daily / weekly).
4. **Today's Schedule** — the app calls `Scheduler.sort_by_time()` to show every task in chronological order (unscheduled tasks last), with columns for pet, duration, priority, repeat, and status. Use the "Show tasks for" dropdown to filter to a single pet.
5. **Conflict warnings** — the app calls `Scheduler.conflict_warnings()` and renders each clash as a yellow `st.warning` (e.g. two tasks at the same time, or one running into the next). If nothing overlaps, it shows a green "No scheduling conflicts" message.

Because the `Owner` is stored in `st.session_state`, everything you add persists as you interact with the page.

**Example workflow:** add pet *Biscuit* → schedule *Morning walk* at 08:00 (daily) → schedule *Feeding* at 08:15 → open **Today's Schedule** and see the two tasks in order with a warning that the walk runs into feeding.

### The terminal demo (`python main.py`)

Running the CLI demo exercises every `Scheduler` behavior without the UI:

```
=== All tasks (insertion order) ===
   18:00  Evening walk      30 min  [high  ] (todo)
   08:00  Morning walk      30 min  [high  ] (todo)
   08:15  Feeding           10 min  [high  ] (todo)
   12:00  Litter cleanup    10 min  [medium] (todo)
   12:00  Medication         5 min  [high  ] (todo)
     --    Play/enrichment   15 min  [low   ] (todo)

=== Sorted by time (unscheduled last) ===
   08:00  Morning walk      30 min  [high  ] (todo)
   08:15  Feeding           10 min  [high  ] (todo)
   12:00  Litter cleanup    10 min  [medium] (todo)
   12:00  Medication         5 min  [high  ] (todo)
   18:00  Evening walk      30 min  [high  ] (todo)
     --    Play/enrichment   15 min  [low   ] (todo)

=== Sorted by priority (high first) ===
   12:00  Medication         5 min  [high  ] (todo)
   08:15  Feeding           10 min  [high  ] (todo)
   18:00  Evening walk      30 min  [high  ] (todo)
   08:00  Morning walk      30 min  [high  ] (todo)
   12:00  Litter cleanup    10 min  [medium] (todo)
     --    Play/enrichment   15 min  [low   ] (todo)

=== Conflict warnings ===
   WARNING: 'Morning walk' (08:00, 30 min) runs into 'Feeding' at 08:15.
   WARNING: 'Litter cleanup' and 'Medication' are both scheduled at 12:00.

=== Recurring: complete Biscuit's daily 'Morning walk' ===
   Original due 2026-07-07 -> completed=True
   Auto-created next occurrence due 2026-07-08
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
