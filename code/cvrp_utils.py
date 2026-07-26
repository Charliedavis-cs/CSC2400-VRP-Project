"""Shared calculations used by the CVRP algorithms."""

from math import hypot


def distance(customer_a, customer_b):
    """Return the Euclidean distance between two customers."""
    return hypot(
        customer_a["x"] - customer_b["x"],
        customer_a["y"] - customer_b["y"],
    )


def route_demand(route, customers):
    """Return the total demand served by one route."""
    total = 0
    for customer_id in route:
        total += customers[customer_id]["demand"]
    return total


def calculate_route_distance(route, customers, depot_id=0):
    """Return the depot-to-depot distance for one route."""
    if not route:
        return 0.0

    total = distance(customers[depot_id], customers[route[0]])

    for index in range(len(route) - 1):
        current_id = route[index]
        next_id = route[index + 1]
        total += distance(customers[current_id], customers[next_id])

    total += distance(customers[route[-1]], customers[depot_id])
    return total


def calculate_total_distance(routes, customers, depot_id=0):
    """Return the distance traveled by all vehicles."""
    total = 0.0
    for route in routes:
        total += calculate_route_distance(route, customers, depot_id)
    return total


def split_order_into_routes(order, customers, vehicle_capacity):
    """Split a customer ordering into capacity-feasible routes."""
    routes = []
    current_route = []
    current_demand = 0

    for customer_id in order:
        demand = customers[customer_id]["demand"]

        # Start a new route when the next demand is too large
        if current_route and current_demand + demand > vehicle_capacity:
            routes.append(current_route)
            current_route = []
            current_demand = 0

        current_route.append(customer_id)
        current_demand += demand

    if current_route:
        routes.append(current_route)

    return routes
