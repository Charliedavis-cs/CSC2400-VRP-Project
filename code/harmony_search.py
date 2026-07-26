"""A simplified Harmony Search for the CVRP."""

import random

from cvrp_utils import calculate_total_distance, split_order_into_routes
from validators import validate_customer_data


def repair_order(order, customer_ids):
    """Remove duplicates and add any missing customers."""
    repaired = []
    used = set()

    for customer_id in order:
        if customer_id in customer_ids and customer_id not in used:
            repaired.append(customer_id)
            used.add(customer_id)

    for customer_id in customer_ids:
        if customer_id not in used:
            repaired.append(customer_id)

    return repaired


def pitch_adjust(order, random_source):
    """Make one small random change to a customer ordering."""
    if len(order) < 2:
        return order

    changed = order[:]
    first = random_source.randrange(len(changed))
    second = random_source.randrange(len(changed))
    changed[first], changed[second] = changed[second], changed[first]
    return changed


def harmony_search_cvrp(
    customers,
    vehicle_capacity,
    depot_id=0,
    memory_size=10,
    iterations=500,
    memory_rate=0.9,
    pitch_rate=0.3,
    seed=2400,
):
    """Search for a good route ordering using a small harmony memory."""
    validate_customer_data(customers, vehicle_capacity, depot_id)
    customer_ids = sorted(set(customers) - {depot_id})
    random_source = random.Random(seed)
    memory = []
    operation_count = 0

    for unused in range(memory_size):
        order = customer_ids[:]
        random_source.shuffle(order)
        routes = split_order_into_routes(order, customers, vehicle_capacity)
        score = calculate_total_distance(routes, customers, depot_id)
        memory.append((score, order))

    memory.sort(key=lambda item: item[0])

    for unused in range(iterations):
        candidate = []

        # Choose each position from memory or from unused customers
        for position in range(len(customer_ids)):
            if random_source.random() < memory_rate:
                source_order = random_source.choice(memory)[1]
                candidate.append(source_order[position])
            else:
                candidate.append(random_source.choice(customer_ids))

        candidate = repair_order(candidate, customer_ids)
        if random_source.random() < pitch_rate:
            candidate = pitch_adjust(candidate, random_source)

        routes = split_order_into_routes(candidate, customers, vehicle_capacity)
        score = calculate_total_distance(routes, customers, depot_id)
        operation_count += 1

        if score < memory[-1][0]:
            memory[-1] = (score, candidate)
            memory.sort(key=lambda item: item[0])

    best_order = memory[0][1]
    best_routes = split_order_into_routes(
        best_order, customers, vehicle_capacity
    )
    return best_routes, operation_count
