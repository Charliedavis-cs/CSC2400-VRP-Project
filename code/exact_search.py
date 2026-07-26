"""Exact brute-force comparison for tiny CVRP datasets."""

from itertools import permutations

from cvrp_utils import calculate_total_distance, route_demand
from validators import validate_customer_data


MAX_EXACT_CUSTOMERS = 8


def exact_cvrp(customers, vehicle_capacity, depot_id=0):
    """Try every ordering, but only when there are at most eight customers."""
    validate_customer_data(customers, vehicle_capacity, depot_id)
    customer_ids = sorted(set(customers) - {depot_id})

    if len(customer_ids) > MAX_EXACT_CUSTOMERS:
        raise ValueError(
            f"Exact search is limited to {MAX_EXACT_CUSTOMERS} customers"
        )

    best_routes = None
    best_distance = None
    operation_count = 0

    # This exact search is only practical for the tiny test case
    for order in permutations(customer_ids):
        number_of_break_patterns = 2 ** (len(order) - 1)

        # Each bit says whether a new vehicle starts at that position
        for break_pattern in range(number_of_break_patterns):
            routes = []
            current_route = [order[0]]

            for position in range(1, len(order)):
                should_break = break_pattern & (1 << (position - 1))
                if should_break:
                    routes.append(current_route)
                    current_route = []
                current_route.append(order[position])
            routes.append(current_route)
            operation_count += 1

            valid = True
            for route in routes:
                if route_demand(route, customers) > vehicle_capacity:
                    valid = False
                    break
            if not valid:
                continue

            total_distance = calculate_total_distance(
                routes, customers, depot_id
            )
            if best_distance is None or total_distance < best_distance:
                best_distance = total_distance
                best_routes = routes

    return best_routes, operation_count
