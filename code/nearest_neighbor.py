from math import sqrt


def distance(customer_a, customer_b):
    """Return the Euclidean distance between two customers."""
    return sqrt((customer_a["x"] - customer_b["x"]) ** 2 + (customer_a["y"] - customer_b["y"]) ** 2)


def calculate_route_distance(route, customers):
    """Calculate the depot-to-depot distance for one route."""
    if not route:
        return 0.0

    depot = customers[0]
    total = distance(depot, customers[route[0]])

    for current_id, next_id in zip(route, route[1:]):
        total += distance(customers[current_id], customers[next_id])

    total += distance(customers[route[-1]], depot)
    return total


def calculate_total_distance(routes, customers):
    """Calculate the total distance for all vehicle routes."""
    return sum(calculate_route_distance(route, customers) for route in routes)


def nearest_neighbor_cvrp(customers, vehicle_capacity, depot_id=0):
    """
    Build CVRP routes using a nearest neighbor heuristic.

    Each route starts at the depot, repeatedly visits the closest unvisited
    customer whose demand fits in the remaining capacity, and returns to the
    depot when no feasible customer remains.
    """
    if depot_id not in customers:
        raise ValueError(f"Depot id {depot_id} was not found in customers.")

    for customer_id, customer in customers.items():
        if customer_id != depot_id and customer["demand"] > vehicle_capacity:
            raise ValueError(
                f"Customer {customer_id} demand {customer['demand']} exceeds vehicle capacity {vehicle_capacity}."
            )

    unvisited = set(customers) - {depot_id}
    routes = []

    while unvisited:
        route = []
        remaining_capacity = vehicle_capacity
        current_customer = customers[depot_id]

        while True:
            feasible_customers = [
                customer_id
                for customer_id in unvisited
                if customers[customer_id]["demand"] <= remaining_capacity
            ]

            if not feasible_customers:
                break

            next_customer_id = min(
                feasible_customers,
                key=lambda customer_id: distance(current_customer, customers[customer_id]),
            )

            route.append(next_customer_id)
            remaining_capacity -= customers[next_customer_id]["demand"]
            current_customer = customers[next_customer_id]
            unvisited.remove(next_customer_id)

        routes.append(route)

    return routes
