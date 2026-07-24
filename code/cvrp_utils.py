"""Shared utility """

from math import hypot


def distance(customer_a, customer_b):
    """Return the Euc distance between two customers."""
    return hypot(
        customer_a["x"] - customer_b["x"],
        customer_a["y"] - customer_b["y"],
    )


def route_demand(route, customers):
    """Return the tot demand served by one route."""
    return sum(customers[customer_id]["demand"] for customer_id in route)


def calculate_route_distance(route, customers, depot_id=0):
    """
    Calculate the total distance for one route
    """
    if not route:
        return 0.0

    depot = customers[depot_id]
    total = distance(depot, customers[route[0]])

    for current_id, next_id in zip(route, route[1:]):
        total += distance(
            customers[current_id],
            customers[next_id],
        )

    total += distance(customers[route[-1]], depot)
    return total


def calculate_total_distance(routes, customers, depot_id=0):
    """Return the tot distance traveled across all vehicle"""
    return sum(
        calculate_route_distance(route, customers, depot_id)
        for route in routes
    )
