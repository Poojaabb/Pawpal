# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
