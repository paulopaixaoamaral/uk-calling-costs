from unittest import TestCase
from unittest.mock import patch

from src import calling_cost_for_countries


class ModuleTest(TestCase):
    @patch("src.module.repository")
    def test_calling_cost_for_countries(self, repository_mock):
        repository_costs_result = {
            "country A": "2 pounds",
            "country B": "3 pounds"
        }
        repository_mock.cost_for_countries.return_value = repository_costs_result

        costs = calling_cost_for_countries(
            countries=["country A", "country B"]
        )
        self.assertEqual(repository_costs_result, costs)
