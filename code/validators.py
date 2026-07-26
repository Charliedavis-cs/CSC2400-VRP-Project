"""Checks for customer data and completed CVRP solutions."""

from cvrp_utils import route_demand


def validate_customer_data(customers, vehicle_capacity, depot_id=0):
    """Raise an error when the input cannot make a valid solution."""
    if vehicle_capacity <= 0:
        raise ValueError("Vehicle capacity must be positive")
    if depot_id not in customers:
        raise ValueError("The depot was not found in the customer data")

    for customer_id, customer in customers.items():
        demand = customer["demand"]
        if demand < 0:
            raise ValueError(f"Customer {customer_id} has negative demand")
        if customer_id != depot_id and demand > vehicle_capacity:
            raise ValueError(
                f"Customer {customer_id} demand exceeds vehicle capacity"
            )


def validate_routes(routes, customers, vehicle_capacity, depot_id=0):
    """Return True when every customer is served once within capacity."""
    expected = set(customers) - {depot_id}
    visited = []

    for route in routes:
        if not route or depot_id in route:
            return False
        if route_demand(route, customers) > vehicle_capacity:
            return False
        for customer_id in route:
            visited.append(customer_id)

    # Compare both the list length and set to catch duplicate customers
    return set(visited) == expected and len(visited) == len(expected)
