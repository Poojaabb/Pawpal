"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care planning assistant.
These are skeletons generated from diagrams/uml_draft.mmd (no logic yet).
Implement the method bodies in Phase 4.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

# Maps priority labels to a sortable rank (higher = more urgent).
PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    category: str = "general"
    time: str = ""  # scheduled start "HH:MM"; "" means unscheduled
    frequency: str = "none"  # "none" | "daily" | "weekly"
    completed: bool = False
    due_date: date | None = None

    def priority_rank(self) -> int:
        """Return a sortable integer for this task's priority (higher = more urgent)."""
        return PRIORITY_ORDER.get(self.priority.lower(), 0)

    def start_minutes(self) -> int:
        """Return the start time as minutes past midnight (-1 if unscheduled)."""
        if not self.time:
            return -1
        hours, minutes = self.time.split(":")
        return int(hours) * 60 + int(minutes)

    def end_minutes(self) -> int:
        """Return the end time (start + duration) in minutes past midnight (-1 if unscheduled)."""
        start = self.start_minutes()
        return -1 if start < 0 else start + self.duration_minutes

    def mark_complete(self, today: date | None = None) -> "Task | None":
        """Mark this task done.

        If the task is recurring ("daily"/"weekly"), return a fresh, uncompleted
        Task for the next occurrence with its due_date advanced accordingly.
        Returns None for one-off tasks.
        """
        self.completed = True
        if self.frequency not in ("daily", "weekly"):
            return None
        base = self.due_date or today or date.today()
        step = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=base + step,
        )


@dataclass
class Pet:
    """A pet that an owner cares for."""

    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks


class Owner:
    """The pet owner, with preferences and a daily time budget."""

    def __init__(
        self,
        name: str,
        available_minutes: int = 0,
        preferences: list[str] | None = None,
    ) -> None:
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def list_pets(self) -> list[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def all_tasks(self) -> list[Task]:
        """Gather tasks across every pet into one flat list for the Scheduler."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.list_tasks())
        return tasks

    def tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return only the tasks belonging to the pet with the given name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.list_tasks()
        return []


class Scheduler:
    """Builds and explains a daily plan from tasks under time/priority constraints."""

    def __init__(self, available_minutes: int) -> None:
        self.available_minutes = available_minutes
        self._reasoning: list[str] = []

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by priority (high first), shorter tasks breaking ties."""
        return sorted(tasks, key=lambda t: (-t.priority_rank(), t.duration_minutes))

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by their scheduled 'HH:MM' start time.

        Unscheduled tasks (no time set) are pushed to the end.
        """
        return sorted(
            tasks,
            key=lambda t: t.start_minutes() if t.start_minutes() >= 0 else 24 * 60,
        )

    def filter_by_status(self, tasks: list[Task], completed: bool = False) -> list[Task]:
        """Return only tasks whose completion status matches `completed`."""
        return [t for t in tasks if t.completed == completed]

    def find_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of scheduled tasks whose time slots overlap.

        Only tasks with a start time are considered. Tasks are compared in time
        order, so each returned (a, b) pair means a's slot runs into b's start.
        """
        scheduled = self.sort_by_time([t for t in tasks if t.start_minutes() >= 0])
        conflicts: list[tuple[Task, Task]] = []
        for earlier, later in zip(scheduled, scheduled[1:]):
            if earlier.end_minutes() > later.start_minutes():
                conflicts.append((earlier, later))
        return conflicts

    def conflict_warnings(self, tasks: list[Task]) -> list[str]:
        """Return a friendly warning message for each scheduling conflict.

        Lightweight and non-fatal: if nothing overlaps, returns an empty list
        rather than raising. Callers can print these warnings without the
        program crashing.
        """
        warnings: list[str] = []
        for earlier, later in self.find_conflicts(tasks):
            if earlier.time == later.time:
                warnings.append(
                    f"WARNING: '{earlier.title}' and '{later.title}' are both "
                    f"scheduled at {earlier.time}."
                )
            else:
                warnings.append(
                    f"WARNING: '{earlier.title}' ({earlier.time}, "
                    f"{earlier.duration_minutes} min) runs into "
                    f"'{later.title}' at {later.time}."
                )
        return warnings

    def build_plan(self, tasks: list[Task]) -> list[Task]:
        """Select and order tasks that fit within available_minutes."""
        raise NotImplementedError

    def explain(self) -> str:
        """Return a human-readable explanation of why the plan was chosen."""
        raise NotImplementedError
