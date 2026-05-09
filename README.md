# Map Coloring Constraint Satisfaction Program

This project implements a Constraint Satisfaction Problem (CSP) solver to solve map coloring tasks for Australia and Nairobi sub-counties using real geographical data.

## Features

- **Generic CSP Solver**: Uses backtracking search with the Minimum Remaining Values (MRV) heuristic for efficient coloring.
- **Real Geographical Data**: Loads actual boundaries for Australia and Nairobi from GeoJSON files.
- **Australia Map Coloring**: Colors the regions of Australia using only 3 colors.
- **Nairobi Sub-counties Coloring**: Solves the coloring problem for all 17 sub-counties of Nairobi and identifies the minimum number of colors required (4 colors).
- **Professional Visualization**: Uses `geopandas` and `matplotlib` to render the maps with actual boundaries, labels, and legends.

## Project Structure

- **Australia/**: Logic and results for Australian map coloring.
- **Nairobi/**: Logic and results for Nairobi sub-counties coloring.
- **visualize_maps.py**: A central script to run the coloring for either or both maps.
- **csp_solver.py**: The shared core CSP logic used by both projects.

## Installation

Ensure you have Python installed, then install the required geographical and plotting libraries:

```bash
pip install geopandas matplotlib requests pyogrio shapely
```

## Usage

You can use the interactive menu to run the coloring for any map:

```bash
python visualize_maps.py
```

Alternatively, you can run the scripts directly from their respective folders:

### Australia Map Coloring
```bash
python Australia/australia_map.py
```

### Nairobi Sub-counties Coloring
```bash
python Nairobi/nairobi_map.py
```

## Algorithm Details

The solver uses a **Backtracking Search** algorithm. It selects variables using the **Minimum Remaining Values (MRV)** heuristic, which prioritizes the most constrained regions first to reduce the search space. Adjacencies for the maps are calculated using **spatial join** techniques on the GeoJSON data, ensuring that only regions that share a boundary are considered neighbors.
