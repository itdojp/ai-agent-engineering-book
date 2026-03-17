from __future__ import annotations

from .models import Ticket
from .store import InMemoryTicketStore, seed_store


class SupportHubService:
    def __init__(self, store: InMemoryTicketStore | None = None) -> None:
        self.store = store or seed_store()

    def list_tickets(self, status: str | None = None, assignee: str | None = None) -> list[Ticket]:
        tickets = self.store.list()
        if status:
            tickets = [ticket for ticket in tickets if ticket.status == status]
        if assignee:
            tickets = [ticket for ticket in tickets if ticket.assignee == assignee]
        return tickets

    def get_ticket(self, ticket_id: str) -> Ticket:
        return self.store.get(ticket_id)

    def update_status(self, ticket_id: str, new_status: str) -> Ticket:
        ticket = self.store.get(ticket_id)
        ticket.update_status(new_status)
        return self.store.save(ticket)

    def search_tickets(self, query: str) -> list[Ticket]:
        normalized = query.strip().lower()
        if not normalized:
            return self.store.list()

        def matches(ticket: Ticket) -> bool:
            haystacks = [ticket.title, ticket.description, " ".join(ticket.tags)]
            return any(normalized in item.lower() for item in haystacks)

        return [ticket for ticket in self.store.list() if matches(ticket)]
