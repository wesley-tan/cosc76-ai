# Map Coloring Problem Solver using SAT
# Given a map with regions and their adjacencies, find a valid coloring using k colors

from SAT import SAT
import sys

def generate_map_coloring_cnf(regions, adjacencies, num_colors, filename):
    """Generate CNF file for Map Coloring problem
    
    Args:
        regions: List of region names
        adjacencies: List of tuples (region1, region2) representing adjacent regions
        num_colors: Number of colors to use
        filename: Output CNF filename
    """
    with open(filename, 'w') as f:
        
        # Each region must have at least one color
        for r_id, region in enumerate(regions, 1):
            # At least one color per region
            colors = [str(r_id*100 + c) for c in range(1, num_colors+1)]
            f.write(' '.join(colors) + '\n')
            
            # No two colors for same region
            for c1 in range(1, num_colors+1):
                for c2 in range(c1+1, num_colors+1):
                    f.write(f"-{r_id*100 + c1} -{r_id*100 + c2}\n")
        
        # Adjacent regions cannot have same color
        for r1, r2 in adjacencies:
            r1_id = regions.index(r1) + 1
            r2_id = regions.index(r2) + 1
            for color in range(1, num_colors+1):
                f.write(f"-{r1_id*100 + color} -{r2_id*100 + color}\n")

if __name__ == "__main__":
    # Example: Australia map coloring
    regions = ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS']
    adjacencies = [
        ('WA', 'NT'), ('WA', 'SA'),
        ('NT', 'SA'), ('NT', 'QLD'),
        ('SA', 'QLD'), ('SA', 'NSW'), ('SA', 'VIC'),
        ('QLD', 'NSW'),
        ('NSW', 'VIC'),
        # TAS is an island, no adjacencies
    ]
    num_colors = 4  # Classic 4-color theorem
    
    cnf_file = "map_coloring.cnf"
    sol_file = "map_coloring.sol"
    
    # Generate CNF file
    generate_map_coloring_cnf(regions, adjacencies, num_colors, cnf_file)
    
    # Solve using SAT solver
    sat = SAT(cnf_file)
    if sat.walksat():
        sat.write_solution(sol_file)
        print("\nSolution found for Map Coloring problem!")
        
        # Display solution
        print("\nColor assignments:")
        with open(sol_file, 'r') as f:
            for line in f:
                pos = int(line.strip())
                region_id = (pos // 100) - 1
                color = pos % 100
                print(f"{regions[region_id]}: Color {color}")
    else:
        print("\nNo solution found for Map Coloring problem.")
