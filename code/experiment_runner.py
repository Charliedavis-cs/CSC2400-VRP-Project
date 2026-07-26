"""Run the CVRP algorithms and save comparable results."""

import csv
import time
from pathlib import Path

from clarke_wright import clarke_wright_cvrp
from cvrp_utils import calculate_total_distance, route_demand
from exact_search import exact_cvrp
from harmony_search import harmony_search_cvrp
from nearest_neighbor import nearest_neighbor_cvrp
from validators import validate_routes


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "sample_customers.csv"
TINY_DATA_PATH = ROOT_DIR / "data" / "tiny_customers.csv"
RESULTS_PATH = ROOT_DIR / "results" / "raw_results.csv"
VEHICLE_CAPACITY = 40
REPETITIONS = 5


def load_customers(csv_path):
    """Load customer coordinates and demands from a CSV file."""
    customers = {}
    with csv_path.open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_id = int(row["id"])
            customers[customer_id] = {
                "id": customer_id,
                "x": float(row["x"]),
                "y": float(row["y"]),
                "demand": int(row["demand"]),
            }
    return customers


def run_algorithm(name, algorithm, customers, capacity, repetitions, seeds=None):
    """Run one algorithm several times and return one result per run."""
    results = []

    # Repeated runs show timing variation and Harmony Search randomness
    for run_number in range(1, repetitions + 1):
        start_time = time.perf_counter()
        if seeds is None:
            routes, operations = algorithm(customers, capacity)
        else:
            routes, operations = algorithm(
                customers, capacity, seed=seeds[run_number - 1]
            )
        runtime_ms = (time.perf_counter() - start_time) * 1000

        if not validate_routes(routes, customers, capacity):
            raise ValueError(f"{name} produced an invalid solution")

        results.append(
            {
                "algorithm": name,
                "run": run_number,
                "customers": len(customers) - 1,
                "vehicle_capacity": capacity,
                "runtime_ms": f"{runtime_ms:.3f}",
                "total_distance": f"{calculate_total_distance(routes, customers):.2f}",
                "number_of_routes": len(routes),
                "operations": operations,
                "routes": routes,
            }
        )
    return results


def save_results(results):
    """Save experiment rows without the route lists."""
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "algorithm",
        "dataset",
        "run",
        "customers",
        "vehicle_capacity",
        "runtime_ms",
        "total_distance",
        "number_of_routes",
        "operations",
    ]

    with RESULTS_PATH.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = {key: result[key] for key in fieldnames if key != "dataset"}
            row["dataset"] = result["dataset"]
            writer.writerow(row)


def print_best_results(results, customers):
    """Print the shortest result found for each algorithm."""
    names = []
    for result in results:
        if result["algorithm"] not in names:
            names.append(result["algorithm"])

    for name in names:
        matches = [row for row in results if row["algorithm"] == name]
        best = min(matches, key=lambda row: float(row["total_distance"]))
        print(f"\n{name}: {best['total_distance']} distance")
        for index, route in enumerate(best["routes"], start=1):
            print(
                f"  Route {index}: 0 -> "
                + " -> ".join(str(customer_id) for customer_id in route)
                + f" -> 0 | demand {route_demand(route, customers)}"
            )


def main():
    customers = load_customers(DATA_PATH)
    all_results = []
    algorithms = [
        ("Nearest Neighbor", nearest_neighbor_cvrp, None),
        ("Clarke-Wright Savings", clarke_wright_cvrp, None),
        ("Harmony Search", harmony_search_cvrp, [2400, 2401, 2402, 2403, 2404]),
    ]

    for name, algorithm, seeds in algorithms:
        rows = run_algorithm(
            name, algorithm, customers, VEHICLE_CAPACITY, REPETITIONS, seeds
        )
        for row in rows:
            row["dataset"] = DATA_PATH.name
        all_results.extend(rows)

    tiny_customers = load_customers(TINY_DATA_PATH)
    exact_rows = run_algorithm(
        "Exact Search", exact_cvrp, tiny_customers, VEHICLE_CAPACITY, 1
    )
    exact_rows[0]["dataset"] = TINY_DATA_PATH.name
    all_results.extend(exact_rows)

    save_results(all_results)
    print_best_results(all_results[:-1], customers)
    print(
        f"\nExact tiny-instance distance: "
        f"{exact_rows[0]['total_distance']}"
    )
    print(f"Results saved to {RESULTS_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
