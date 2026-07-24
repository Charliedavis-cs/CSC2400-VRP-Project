"""Nearest Neighbor heuristic for CVRP"""

from cvrp_utils import calculate_total_distance, distance


def nearest_neighbor_cvrp(customers, vehicle_capacity, depot_id=0):

    if vehicle_capacity <= 0:
        raise ValueError("Vehicle cap > 8")

    if depot_id not in customers:
        raise ValueError(
            f"Depot ID {depot_id} was not found in the customer data"
        )

    for customer_id, customer in customers.items():
        demand = customer["demand"]

        if demand < 0:
            raise ValueError(
                f"Customer {customer_id} has negative demand"
            )

        if customer_id != depot_id and demand > vehicle_capacity:
            raise ValueError(
                f"Customer {customer_id} demand {demand} exceeds "
                f"vehicle capacity {vehicle_capacity}"
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
                key=lambda customer_id: (
                    distance(
                        current_customer,
                        customers[customer_id],
                    ),
                    customer_id,
                ),
            )

            route.append(next_customer_id)
            remaining_capacity -= customers[next_customer_id]["demand"]
            current_customer = customers[next_customer_id]
            unvisited.remove(next_customer_id)

        routes.append(route)

    return routes
