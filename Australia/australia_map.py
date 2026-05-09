import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import requests
from csp_solver import CSP, map_coloring_constraints

def solve_australia_real():
    # ---- 1. Download real Australia state boundaries (GeoJSON) ----
    url = "https://raw.githubusercontent.com/rowanhogan/australian-states/master/states.geojson"
    response = requests.get(url)
    gdf = gpd.read_file(response.text)

    print("Loaded regions:", list(gdf['STATE_NAME']))

    # ---- 2. Group into 5 regions (as requested by user) ----
    region_map = {
        "Western Australia":   "WA",
        "Northern Territory":  "NT",
        "South Australia":     "SA",
        "Queensland":          "QLD",
        "New South Wales":     "NSW/VIC",
        "Victoria":            "NSW/VIC",
        "Australian Capital Territory": "NSW/VIC",
        "Tasmania":            "NSW/VIC",
    }

    gdf["region"] = gdf["STATE_NAME"].map(region_map)
    gdf_merged = gdf.dissolve(by="region").reset_index()

    print("Merged into regions:", list(gdf_merged["region"]))

    # ---- 3. CSP Solving (Backtracking) ----
    variables = list(gdf_merged["region"])
    colors = ["teal", "purple", "amber"]
    domains = {v: colors for v in variables}
    
    # Adjacency for the 5 regions
    neighbors = {
        "WA":      ["NT", "SA"],
        "NT":      ["WA", "SA", "QLD"],
        "SA":      ["WA", "NT", "QLD", "NSW/VIC"],
        "QLD":     ["NT", "SA", "NSW/VIC"],
        "NSW/VIC": ["SA", "QLD"],
    }

    csp = CSP(variables, domains, neighbors, map_coloring_constraints)
    solution = csp.backtracking_search()

    if not solution:
        print("Error: No solution found with 3 colors!")
        return

    print("\nColor assignments:")
    for r, c in solution.items():
        print(f"   {r:12s}  ->  {c}")

    # ---- 4. Plot with real geography ----------------------------
    hex_colors = {
        "teal":   "#3DB89A",
        "purple": "#7B6FD4",
        "amber":  "#E8A020",
    }
    
    gdf_merged["color_hex"] = gdf_merged["region"].map(lambda r: hex_colors[solution[r]])

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("#D4EAF7")
    ax.set_facecolor("#D4EAF7")

    gdf_merged.plot(
        ax=ax,
        color=gdf_merged["color_hex"],
        edgecolor="white",
        linewidth=2.0,
    )

    # Labels at region centroids
    for _, row in gdf_merged.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row["region"],
            xy=(centroid.x, centroid.y),
            ha='center', va='center',
            fontsize=11, fontweight='bold',
            color='#1a1a2e',
            fontfamily='serif'
        )

    # Legend
    legend_patches = [
        mpatches.Patch(facecolor=hex_colors[c], edgecolor='gray',
                       label=f"{c.capitalize()} — {', '.join(r for r,v in solution.items() if v==c)}")
        for c in colors if c in solution.values()
    ]
    ax.legend(handles=legend_patches, loc='lower left',
              fontsize=10, title="Colors Used (≤3)",
              title_fontsize=10, framealpha=0.9)

    ax.set_title(
        "Australia — Real Map Coloring (CSP, 3 Colors)",
        fontsize=14, fontweight='bold', pad=15, fontfamily='serif'
    )
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("australia_real_map_colored.png", dpi=150, bbox_inches='tight')
    print("\nSaved as 'australia_real_map_colored.png'")
    plt.show()

if __name__ == "__main__":
    solve_australia_real()
