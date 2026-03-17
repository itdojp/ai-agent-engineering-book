import unittest

from support_hub.service import SupportHubService


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


if __name__ == "__main__":
    unittest.main()
