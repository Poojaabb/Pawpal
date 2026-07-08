"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care planning assistant.
These are skeletons generated from diagrams/uml_draft.mmd (no logic yet).
Implement the method bodies in Phase 4.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    category: str = "general"
    recurring: bool = False

    def priority_rank(self) -> int:
        """Return a sortable integer for this task's priority (higher = more urgent)."""
        raise NotImplementedError


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


class Scheduler:
    """Builds and explains a daily plan from tasks under time/priority constraints."""

    def __init__(self, available_minutes: int) -> None:
        self.available_minutes = available_minutes
        self._reasoning: list[str] = []

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by priority (and duration as a tiebreaker)."""
        raise NotImplementedError

    def build_plan(self, tasks: list[Task]) -> list[Task]:
        """Select and order tasks that fit within available_minutes."""
        raise NotImplementedError

    def explain(self) -> str:
        """Return a human-readable explanation of why the plan was chosen."""
        raise NotImplementedError
