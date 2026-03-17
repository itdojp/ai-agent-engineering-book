from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


ALLOWED_STATUSES = {"open", "in_progress", "resolved"}


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: str = "open"
    assignee: str | None = None
    tags: List[str] = field(default_factory=list)
    history: List[str] = field(default_factory=list)

    def update_status(self, new_status: str) -> None:
        if new_status not in ALLOWED_STATUSES:
            raise ValueError(f"invalid status: {new_status}")
        self.history.append(f"status:{self.status}->{new_status}")
        self.status = new_status
