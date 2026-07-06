# Capacitated Vehicle Routing Problem Algorithm Comparison

## Team Members

- Mandy Jones
- Tomu Yamashita
- Tristen Martin
- Charles Davis

## Project Description

This repository contains the CSC 2400 Algorithms term project for comparing algorithms for the Capacitated Vehicle Routing Problem (CVRP). In CVRP, a set of customers with known demands must be served by vehicles that start and end at a depot. Each vehicle has a fixed capacity, and the goal is to create routes that serve all customers while minimizing total travel distance and respecting capacity limits.

## Algorithms Being Compared

- Nearest Neighbor Heuristic
- Clarke-Wright Savings Algorithm
- Harmony Search

## Dataset Plan

The project will use CVRPLIB benchmark instances for algorithm comparison. CVRPLIB provides standard CVRP datasets that can be used to compare solution quality, route count, runtime, and scalability across different algorithms. A small custom CSV dataset is included now so the repository has working starter code for checkpoint 2.

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

