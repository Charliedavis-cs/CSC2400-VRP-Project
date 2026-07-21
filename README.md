# Capacitated Vehicle Routing Problem Algorithm Comparison

## Team Members

- [Mandy Jones](https://github.com/search?q=Mandy+Jones&type=users)
- [Tomu Yamashita](https://github.com/search?q=Tomu+Yamashita&type=users)
- [Tristen Martin](https://github.com/search?q=Tristen+Martin&type=users)
- [Charles Davis](https://github.com/Charliedavis-cs)

## Project Description

This repository contains the CSC 2400 Algorithms project for comparing algorithms for the Capacitated Vehicle Routing Problem. In this problem a set of customers with known demands must be served by vehicles that start and end at a place. Each vehicle has a fixed capacity, and the goal is to create routes that serve all customers while minimizing total travel distance and respecting capacity limits.

## Algorithms Being Compared

- Nearest Neighbor Heuristic
- Clarke-Wright Savings Algorithm
- Harmony Search

For checkpoint 2, the Nearest Neighbor Heuristic is implemented as the working baseline. Clarke-Wright Savings and Harmony Search are planned next so the final project can compare a simple greedy heuristic, a classical savings based heuristic, and a metaheuristic approach.

## Dataset Plan

The current sample dataset is stored in `data/sample_customers.csv`. Customer `0` is the depot, and every other row represents one customer with `x` coordinate, `y` coordinate, and demand.

## Experimentation Plan

The experiment runner translates the project's comparison plan into code by loading a dataset, running a CVRP algorithm, measuring runtime, calculating total distance, and recording the number of vehicle routes. Each algorithm will eventually be run on the same datasets and evaluated using the same output columns:

- `algorithm`
- `dataset`
- `customers`
- `vehicle_capacity`
- `runtime_ms`
- `total_distance`
- `number_of_routes`

This makes it possible to compare algorithms using consistent metrics. For checkpoint 2, this process is implemented for the Nearest Neighbor baseline.

## Repository Structure

- `code/`: Python source code for algorithms and experiment scripts.
- `data/`: Input datasets, including the starter custom customer dataset and future CVRPLIB data files.
- `results/`: Raw experiment outputs, including CSV files with runtime and route-distance results.
- `tables_graphs/`: Generated comparison tables and graphs for the final analysis.
- `reports/`: Checkpoint reports and final written project materials.

## How to Run

Run the starter experiment from the repository root:

```bash
python code/experiment_runner.py
```

The experiment runner loads `data/sample_customers.csv`, treats customer `0` as the depot, runs the Nearest Neighbor CVRP baseline with vehicle capacity `40`, prints the routes, and saves summary metrics to `results/raw_results.csv`.

## Current Output

The current experiment records:

- Algorithm name
- Dataset name
- Number of customers
- Vehicle capacity
- Runtime in milliseconds
- Total route distance
- Number of vehicle routes

The starter dataset run currently produces:

- Vehicle capacity: `40`
- Number of customers served: `10`
- Number of routes: `4`
- Total route distance: `365.13`

Results are saved in `results/raw_results.csv`.

