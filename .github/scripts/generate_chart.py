import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# --- Script Arguments ---
# 1: CSV file path
# 2: Output SVG file path
# 3: Chart Title
# 4: X-axis column name
# 5: Y-axis column name
# 6: Group-by column name
# 7: X-axis label
# 8: Y-axis label
# ---

# Read arguments from command line
csv_path = sys.argv[1]
output_path = sys.argv[2]
title = sys.argv[3]
x_col = sys.argv[4]
y_col = sys.argv[5]
group_col = sys.argv[6]
x_label = sys.argv[7]
y_label = sys.argv[8]

# Check if the CSV file exists and is not empty
if not os.path.exists(csv_path) or os.path.getsize(csv_path) < 2:
    print(f"Data file not found or is empty: {csv_path}")
    # Create a placeholder empty SVG
    with open(output_path, 'w') as f:
        f.write('<svg width="500" height="50" xmlns="http://www.w3.org/2000/svg"><text x="10" y="30" font-family="sans-serif" font-size="16px" fill="grey">No data to plot yet.</text></svg>')
    sys.exit(0)

# Read and process the data
df = pd.read_csv(csv_path)
df = df.sort_values(by=x_col)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data for each group (each registry)
for group_name, group_data in df.groupby(group_col):
    ax.plot(group_data[x_col], group_data[y_col], marker='o', linestyle='-', label=group_name)

# --- Style the plot ---
ax.set_title(title, fontsize=16)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label, fontsize=12)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(title=group_col)
plt.tight_layout()

# Save the plot as an SVG file
fig.savefig(output_path, format='svg')
print(f"Chart saved to {output_path}")
