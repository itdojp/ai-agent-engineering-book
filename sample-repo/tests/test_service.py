import unittest

from support_hub.models import Ticket
from support_hub.service import SupportHubService
from support_hub.store import InMemoryTicketStore


class SupportHubServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SupportHubService()

    def test_list_tickets_filters_by_status(self) -> None:
        open_tickets = self.service.list_tickets(status="open")
        self.assertTrue(open_tickets)
        self.assertTrue(all(ticket.status == "open" for ticket in open_tickets))

    def test_update_status_persists_changes(self) -> None:
        ticket = self.service.update_status("T-100", "resolved")
        self.assertEqual(ticket.status, "resolved")

        reloaded = self.service.get_ticket("T-100")
        self.assertEqual(reloaded.status, "resolved")
        self.assertIn("status:open->resolved", reloaded.history)

    def test_list_tickets_filters_by_assignee(self) -> None:
        ken_tickets = self.service.list_tickets(assignee="ken")
        self.assertEqual(len(ken_tickets), 1)
        self.assertEqual(ken_tickets[0].id, "T-101")

    def test_store_returns_detached_ticket_copies(self) -> None:
        store = InMemoryTicketStore(
            [
                Ticket(
                    id="T-200",
                    title="Detached copy check",
                    description="Ensure callers cannot mutate store internals.",
                    tags=["bug"],
                    history=["created"],
                )
            ]
        )

        fetched = store.get("T-200")
        fetched.tags.append("mutated")
        fetched.history.append("edited")

        reloaded = store.get("T-200")
        self.assertEqual(reloaded.tags, ["bug"])
        self.assertEqual(reloaded.history, ["created"])

    def test_store_save_clones_mutable_fields(self) -> None:
        store = InMemoryTicketStore()
        ticket = Ticket(
            id="T-201",
            title="Save clone check",
            description="Ensure save detaches mutable fields.",
            tags=["feature"],
            history=["created"],
        )

        saved = store.save(ticket)
        ticket.tags.append("mutated-after-save")
        ticket.history.append("edited-after-save")
        saved.tags.append("mutated-return-value")
        saved.history.append("edited-return-value")

        reloaded = store.get("T-201")
        self.assertEqual(reloaded.tags, ["feature"])
        self.assertEqual(reloaded.history, ["created"])


if __name__ == "__main__":
    unittest.main()
