"""Automated tests for the PawPal+ system.

Run with:  python -m pytest

Covers the core intelligence of the scheduler:
  - sorting (by time and by priority)
  - filtering (by status and by pet)
  - recurring-task logic (daily / weekly / one-off)
  - conflict detection (exact same time and run-over overlaps)
plus edge cases like a pet with no tasks and an owner with no pets.
"""

from datetime import date

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture
def scheduler():
    return Scheduler(available_minutes=180)


@pytest.fixture
def owner_with_tasks():
    """An owner with two pets and tasks deliberately added out of order."""
    owner = Owner(name="Jordan", available_minutes=180)
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Mochi", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Evening walk", 30, "high", time="18:00"))
    dog.add_task(Task("Morning walk", 30, "high", time="08:00"))
    cat.add_task(Task("Litter cleanup", 10, "medium", time="12:00"))
    cat.add_task(Task("Play", 15, "low"))  # no scheduled time
    return owner


# --------------------------------------------------------------------------- #
# Sorting correctness
# --------------------------------------------------------------------------- #
def test_sort_by_time_is_chronological(scheduler, owner_with_tasks):
    ordered = scheduler.sort_by_time(owner_with_tasks.all_tasks())
    titles = [t.title for t in ordered]
    # Scheduled tasks in clock order, unscheduled ("Play") pushed to the end.
    assert titles == ["Morning walk", "Litter cleanup", "Evening walk", "Play"]


def test_sort_by_time_does_not_mutate_input(scheduler, owner_with_tasks):
    tasks = owner_with_tasks.all_tasks()
    before = [t.title for t in tasks]
    scheduler.sort_by_time(tasks)
    assert [t.title for t in tasks] == before  # original order untouched


def test_sort_by_priority_high_first(scheduler):
    tasks = [
        Task("Low job", 10, "low"),
        Task("High job", 10, "high"),
        Task("Medium job", 10, "medium"),
    ]
    ordered = scheduler.sort_by_priority(tasks)
    assert [t.priority for t in ordered] == ["high", "medium", "low"]


def test_sort_by_priority_shorter_task_breaks_tie(scheduler):
    tasks = [
        Task("Long high", 60, "high"),
        Task("Short high", 5, "high"),
    ]
    ordered = scheduler.sort_by_priority(tasks)
    assert [t.title for t in ordered] == ["Short high", "Long high"]


def test_priority_rank_mapping():
    assert Task("a", 5, "high").priority_rank() == 3
    assert Task("b", 5, "medium").priority_rank() == 2
    assert Task("c", 5, "low").priority_rank() == 1
    assert Task("d", 5, "bogus").priority_rank() == 0  # unknown -> 0, no crash


# --------------------------------------------------------------------------- #
# Filtering
# --------------------------------------------------------------------------- #
def test_filter_by_status(scheduler):
    done = Task("Done", 5, "low", completed=True)
    todo = Task("Todo", 5, "low", completed=False)
    tasks = [done, todo]
    assert scheduler.filter_by_status(tasks, completed=False) == [todo]
    assert scheduler.filter_by_status(tasks, completed=True) == [done]


def test_tasks_for_pet(owner_with_tasks):
    mochi_titles = [t.title for t in owner_with_tasks.tasks_for_pet("Mochi")]
    assert sorted(mochi_titles) == ["Litter cleanup", "Play"]


def test_tasks_for_unknown_pet_is_empty(owner_with_tasks):
    assert owner_with_tasks.tasks_for_pet("Nobody") == []


# --------------------------------------------------------------------------- #
# Recurrence logic
# --------------------------------------------------------------------------- #
def test_daily_task_creates_next_day_occurrence():
    task = Task("Morning walk", 30, "high", frequency="daily",
                due_date=date(2026, 7, 7))
    nxt = task.mark_complete()
    assert task.completed is True
    assert nxt is not None
    assert nxt.completed is False
    assert nxt.due_date == date(2026, 7, 8)  # today + 1 day
    assert nxt.title == task.title


def test_weekly_task_advances_seven_days():
    task = Task("Grooming", 45, "medium", frequency="weekly",
                due_date=date(2026, 7, 7))
    nxt = task.mark_complete()
    assert nxt is not None
    assert nxt.due_date == date(2026, 7, 14)


def test_one_off_task_has_no_next_occurrence():
    task = Task("Vet visit", 60, "high", frequency="none")
    nxt = task.mark_complete()
    assert task.completed is True
    assert nxt is None


# --------------------------------------------------------------------------- #
# Conflict detection
# --------------------------------------------------------------------------- #
def test_exact_same_time_is_flagged(scheduler):
    tasks = [
        Task("Litter cleanup", 10, "medium", time="12:00"),
        Task("Medication", 5, "high", time="12:00"),
    ]
    warnings = scheduler.conflict_warnings(tasks)
    assert len(warnings) == 1
    assert "12:00" in warnings[0]


def test_run_over_overlap_is_flagged(scheduler):
    tasks = [
        Task("Morning walk", 30, "high", time="08:00"),  # ends 08:30
        Task("Feeding", 10, "high", time="08:15"),        # starts during walk
    ]
    assert len(scheduler.find_conflicts(tasks)) == 1


def test_no_conflict_when_spaced_out(scheduler):
    tasks = [
        Task("Walk", 30, "high", time="08:00"),   # 08:00-08:30
        Task("Feed", 10, "high", time="09:00"),   # 09:00-09:10
    ]
    assert scheduler.find_conflicts(tasks) == []
    assert scheduler.conflict_warnings(tasks) == []


def test_unscheduled_tasks_never_conflict(scheduler):
    tasks = [Task("Play", 15, "low"), Task("Nap", 30, "low")]  # no times
    assert scheduler.find_conflicts(tasks) == []


# --------------------------------------------------------------------------- #
# Edge cases
# --------------------------------------------------------------------------- #
def test_pet_with_no_tasks():
    pet = Pet(name="Rex", species="dog")
    assert pet.list_tasks() == []


def test_owner_with_no_pets_has_no_tasks(scheduler):
    owner = Owner(name="Alex")
    assert owner.all_tasks() == []
    assert scheduler.conflict_warnings(owner.all_tasks()) == []


def test_sorting_empty_list_is_safe(scheduler):
    assert scheduler.sort_by_time([]) == []
    assert scheduler.sort_by_priority([]) == []
