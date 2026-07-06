import csv
import time
from pathlib import Path

from nearest_neighbor import calculate_total_distance, nearest_neighbor_cvrp


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "sample_customers.csv"
RESULTS_PATH = ROOT_DIR / "results" / "raw_results.csv"
VEHICLE_CAPACITY = 40


def load_customers(csv_path):
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


def route_demand(route, customers):
    return sum(customers[customer_id]["demand"] for customer_id in route)


def print_routes(routes, customers):
    print("Nearest Neighbor CVRP Routes")
    print(f"Vehicle capacity: {VEHICLE_CAPACITY}")

    for index, route in enumerate(routes, start=1):
        route_display = " -> ".join(str(customer_id) for customer_id in [0, *route, 0])
        print(f"Route {index}: {route_display} | demand = {route_demand(route, customers)}")


def save_results(result_row):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "algorithm",
        "dataset",
        "customers",
        "vehicle_capacity",
        "runtime_ms",
        "total_distance",
        "number_of_routes",
    ]

    with RESULTS_PATH.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(result_row)


def main():
    customers = load_customers(DATA_PATH)

    start_time = time.perf_counter()
    routes = nearest_neighbor_cvrp(customers, VEHICLE_CAPACITY)
    runtime_ms = (time.perf_counter() - start_time) * 1000

    total_distance = calculate_total_distance(routes, customers)

    print_routes(routes, customers)
    print(f"Total distance: {total_distance:.2f}")
    print(f"Runtime: {runtime_ms:.3f} ms")
    print(f"Number of routes: {len(routes)}")

    save_results(
        {
            "algorithm": "Nearest Neighbor Heuristic",
            "dataset": DATA_PATH.name,
            "customers": len(customers) - 1,
            "vehicle_capacity": VEHICLE_CAPACITY,
            "runtime_ms": f"{runtime_ms:.3f}",
            "total_distance": f"{total_distance:.2f}",
            "number_of_routes": len(routes),
        }
    )

    print(f"Results saved to {RESULTS_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
