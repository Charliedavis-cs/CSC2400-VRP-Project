"""Clarke-Wright Savings heuristic for the CVRP."""

from cvrp_utils import distance, route_demand
from validators import validate_customer_data


def find_route(routes, customer_id):
    """Find the current route containing a customer."""
    for route in routes:
        if customer_id in route:
            return route
    return None


def clarke_wright_cvrp(customers, vehicle_capacity, depot_id=0):
    """Build routes by merging pairs that give the largest distance saving."""
    validate_customer_data(customers, vehicle_capacity, depot_id)
    customer_ids = sorted(set(customers) - {depot_id})
    routes = [[customer_id] for customer_id in customer_ids]
    savings = []
    operation_count = 0

    # Calculate a saving for every customer pair
    for first_index in range(len(customer_ids)):
        for second_index in range(first_index + 1, len(customer_ids)):
            first_id = customer_ids[first_index]
            second_id = customer_ids[second_index]
            saving = (
                distance(customers[depot_id], customers[first_id])
                + distance(customers[depot_id], customers[second_id])
                - distance(customers[first_id], customers[second_id])
            )
            savings.append((saving, first_id, second_id))
            operation_count += 1

    # Larger savings are checked first
    savings.sort(key=lambda item: (-item[0], item[1], item[2]))

    for saving, first_id, second_id in savings:
        route_one = find_route(routes, first_id)
        route_two = find_route(routes, second_id)
        operation_count += len(routes)

        if route_one is route_two:
            continue
        if first_id not in (route_one[0], route_one[-1]):
            continue
        if second_id not in (route_two[0], route_two[-1]):
            continue

        combined_demand = (
            route_demand(route_one, customers)
            + route_demand(route_two, customers)
        )
        if combined_demand > vehicle_capacity:
            continue

        # Turn the routes so the selected endpoints touch
        if route_one[0] == first_id:
            route_one.reverse()
        if route_two[-1] == second_id:
            route_two.reverse()

        merged_route = route_one + route_two
        routes.remove(route_one)
        routes.remove(route_two)
        routes.append(merged_route)

    return routes, operation_count
