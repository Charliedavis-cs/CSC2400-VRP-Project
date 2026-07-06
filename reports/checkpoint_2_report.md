# Checkpoint 2 Report

## Project Problem

The Capacitated Vehicle Routing Problem (CVRP) asks how to route vehicles from a central depot to a set of customers while meeting customer demand and obeying vehicle capacity limits. Each customer must be visited, each vehicle starts and ends at the depot, and the project goal is to compare algorithms based on total route distance, runtime, and number of routes used.

## Completed So Far

The repository structure for the project has been created with folders for code, data, results, tables and graphs, and reports. This gives the project a clear organization for implementation, experiments, analysis outputs, and written deliverables.

The Nearest Neighbor baseline algorithm has been implemented. It starts at the depot, repeatedly selects the closest unvisited customer that fits within the remaining vehicle capacity, and starts a new vehicle route when no feasible customer remains.

A small sample dataset has been created in CSV format. Customer `0` is the depot, and the remaining customers have coordinates and demand values for testing the starter implementation.

The experiment runner loads the sample dataset, runs the Nearest Neighbor baseline with a vehicle capacity of `40`, records runtime, calculates total route distance, counts the number of vehicle routes, prints readable routes, and saves the results to `results/raw_results.csv`.

## Next Steps

- Add the Clarke-Wright Savings Algorithm.
- Prepare CVRPLIB benchmark data for experiments.
- Add the Harmony Search algorithm.
- Generate comparison tables and graphs for total distance, runtime, and route count.

