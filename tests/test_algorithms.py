"""Basic tests for the CVRP project."""

import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "code"))

from clarke_wright import clarke_wright_cvrp
from exact_search import exact_cvrp
from experiment_runner import load_customers
from harmony_search import harmony_search_cvrp, repair_order
from nearest_neighbor import nearest_neighbor_cvrp
from validators import validate_routes


class AlgorithmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.customers = load_customers(
            ROOT_DIR / "data" / "sample_customers.csv"
        )

    def test_nearest_neighbor_returns_valid_routes(self):
        routes, operations = nearest_neighbor_cvrp(self.customers, 40)
        self.assertTrue(validate_routes(routes, self.customers, 40))
        self.assertGreater(operations, 0)

    def test_clarke_wright_returns_valid_routes(self):
        routes, operations = clarke_wright_cvrp(self.customers, 40)
        self.assertTrue(validate_routes(routes, self.customers, 40))
        self.assertGreater(operations, 0)

    def test_harmony_search_is_repeatable_with_a_seed(self):
        first_routes, unused = harmony_search_cvrp(
            self.customers, 40, iterations=50, seed=12
        )
        second_routes, unused = harmony_search_cvrp(
            self.customers, 40, iterations=50, seed=12
        )
        self.assertEqual(first_routes, second_routes)
        self.assertTrue(validate_routes(first_routes, self.customers, 40))

    def test_repair_order_removes_duplicates(self):
        repaired = repair_order([1, 1, 3], [1, 2, 3])
        self.assertEqual(repaired, [1, 3, 2])

    def test_exact_search_refuses_large_dataset(self):
        with self.assertRaises(ValueError):
            exact_cvrp(self.customers, 40)

    def test_customer_over_capacity_raises_error(self):
        bad_customers = {
            0: {"x": 0, "y": 0, "demand": 0},
            1: {"x": 1, "y": 1, "demand": 41},
        }
        with self.assertRaises(ValueError):
            nearest_neighbor_cvrp(bad_customers, 40)


if __name__ == "__main__":
    unittest.main()
