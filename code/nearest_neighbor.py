"""Nearest Neighbor heuristic for the CVRP."""

from cvrp_utils import distance
from validators import validate_customer_data


def nearest_neighbor_cvrp(customers, vehicle_capacity, depot_id=0):
    """Build routes by repeatedly choosing the closest customer that fits."""
    validate_customer_data(customers, vehicle_capacity, depot_id)

    unvisited = set(customers) - {depot_id}
    routes = []
    operation_count = 0

    while unvisited:
        current_route = []
        remaining_capacity = vehicle_capacity
        current_id = depot_id

        while True:
            nearest_id = None
            nearest_distance = None

            # Check every customer that can still fit in this truck
            for customer_id in sorted(unvisited):
                operation_count += 1
                demand = customers[customer_id]["demand"]
                if demand > remaining_capacity:
                    continue

                current_distance = distance(
                    customers[current_id], customers[customer_id]
                )
                if nearest_distance is None or current_distance < nearest_distance:
                    nearest_id = customer_id
                    nearest_distance = current_distance

            if nearest_id is None:
                break

            current_route.append(nearest_id)
            remaining_capacity -= customers[nearest_id]["demand"]
            current_id = nearest_id
            unvisited.remove(nearest_id)

        routes.append(current_route)

    return routes, operation_count
