import unittest

from support_hub.service import SupportHubService


class TicketSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SupportHubService()

    def test_search_uses_title_description_and_tags(self) -> None:
        titles = {ticket.id for ticket in self.service.search_tickets("search")}
        self.assertIn("T-101", titles)

        descriptions = {ticket.id for ticket in self.service.search_tickets("ownership")}
        self.assertIn("T-102", descriptions)

        tags = {ticket.id for ticket in self.service.search_tickets("ui")}
        self.assertIn("T-100", tags)

    def test_blank_query_returns_all_tickets(self) -> None:
        self.assertEqual(len(self.service.search_tickets("   ")), 3)


if __name__ == "__main__":
    unittest.main()
