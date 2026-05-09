import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import requests
import pandas as pd
from csp_solver import CSP, map_coloring_constraints

def solve_nairobi_real():
    # ---- 1. Download Nairobi boundaries (GeoJSON) ----
    url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/constituencies.geojson"
    response = requests.get(url)
    gdf_all = gpd.read_file(response.text)

    # Filter for Nairobi
    gdf = gdf_all[gdf_all['COUNTY_NAM'] == 'NAIROBI'].copy()
    gdf = gdf.reset_index(drop=True)
    
    # Sub-county names are in 'CONSTITUEN'
    variables = list(gdf['CONSTITUEN'])
    print(f"Loaded {len(variables)} Nairobi sub-counties.")

    # ---- 2. Spatial Join to find adjacencies ----
    # Two regions are adjacent if they share a boundary (not just a point)
    # We use 'touches' but for map coloring, points usually count as neighbors too
    neighbors = {}
    for i, row in gdf.iterrows():
        name = row['CONSTITUEN']
        # Find all other sub-counties that intersect this one
        intersecting = gdf[gdf.intersects(row.geometry)]
        neighbor_list = [n for n in intersecting['CONSTITUEN'] if n != name]
        neighbors[name] = neighbor_list

    # ---- 3. Find Minimum Number of Colors ----
    solution = None
    min_k = 0
    palette = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF", "#99FFFF"]
    
    for k in range(1, 7):
        print(f"Checking if {k} colors are sufficient...")
        colors = palette[:k]
        domains = {v: colors for v in variables}
        csp = CSP(variables, domains, neighbors, map_coloring_constraints)
        solution = csp.backtracking_search()
        if solution:
            min_k = k
            break

    if not solution:
        print("Error: Could not find solution with up to 6 colors!")
        return

    print(f"\nSUCCESS: Found solution with minimum {min_k} colors.")

    # ---- 4. Plot with real geography ----
    gdf["color"] = gdf["CONSTITUEN"].map(solution)

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("#F0F0F0")
    ax.set_facecolor("#F0F0F0")

    gdf.plot(
        ax=ax,
        color=gdf["color"],
        edgecolor="black",
        linewidth=0.8,
    )

    # Labels at sub-county centroids
    for _, row in gdf.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row["CONSTITUEN"],
            xy=(centroid.x, centroid.y),
            ha='center', va='center',
            fontsize=8, fontweight='bold',
            color='#333333'
        )

    # Legend
    legend_patches = [
        mpatches.Patch(facecolor=c, edgecolor='black', label=f"Color {i+1}")
        for i, c in enumerate(palette[:min_k])
    ]
    ax.legend(handles=legend_patches, loc='lower right',
              fontsize=10, title=f"Minimum Colors: {min_k}",
              title_fontsize=11)

    ax.set_title(
        "Nairobi — Real Map Coloring (CSP, Chromatic Number)",
        fontsize=14, fontweight='bold', pad=15
    )
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("nairobi_real_map_colored.png", dpi=150, bbox_inches='tight')
    print("\nSaved as 'nairobi_real_map_colored.png'")
    plt.show()

if __name__ == "__main__":
    solve_nairobi_real()
