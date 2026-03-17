from __future__ import annotations

from dataclasses import replace

from .models import Ticket


class InMemoryTicketStore:
    def __init__(self, tickets: list[Ticket] | None = None) -> None:
        self._tickets = {ticket.id: replace(ticket) for ticket in (tickets or [])}

    def list(self) -> list[Ticket]:
        return [replace(ticket) for ticket in self._tickets.values()]

    def get(self, ticket_id: str) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise KeyError(ticket_id)
        return replace(ticket)

    def save(self, ticket: Ticket) -> Ticket:
        self._tickets[ticket.id] = replace(ticket)
        return replace(ticket)


def seed_store() -> InMemoryTicketStore:
    tickets = [
        Ticket(
            id="T-100",
            title="Login page shows stale status",
            description="Users sometimes see the previous ticket status after refresh.",
            status="open",
            assignee="yuki",
            tags=["bug", "ui"],
        ),
        Ticket(
            id="T-101",
            title="Add ticket search",
            description="Support agents need keyword search across title and description.",
            status="in_progress",
            assignee="ken",
            tags=["feature", "search"],
        ),
        Ticket(
            id="T-102",
            title="Track assignment changes",
            description="Managers need better history of who changed ticket ownership.",
            status="open",
            assignee=None,
            tags=["feature", "audit"],
        ),
    ]
    return InMemoryTicketStore(tickets)
