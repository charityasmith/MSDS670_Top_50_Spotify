""""" 
traffic_accidents_visuals.py 

Python 3 
This script generates data visualizations for information on traffic accidents
across various regions and time periods using Matplotlib's stateless interface.

Author: Charity Smith
""" 

#%%
# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects  
import os
import numpy as np

dpi = 300

# if you are on windows, you are going to have to change the file path to
# windows style
project_dir = r''
data_dir = project_dir + r'data/'
output_dir = project_dir + r'output/'

#%%

# Data Source:Traffic Accidents
# https://www.kaggle.com/datasets/oktayrdeki/traffic-accidents/data
# Load the cleaned dataset
data_filename = "traffic_accidents_clean.csv"
df = pd.read_csv(data_dir + data_filename)


# Plot 1
# Bar Chart - Top Five Primary Contributing Causes of Accidents

# Count occurrences of each primary contributory cause
cause_counts = df["prim_contributory_cause"].value_counts()

# Keep only the top 5 causes
top_causes = cause_counts.nlargest(5)

# Convert labels to title case (no ALL CAPS)
top_causes.index = top_causes.index.str.title()

# Set up figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Select a color for bars
bar_color = "#1F5D89" # Dusk blue

# Create a horizontal bar chart with slightly wider bars
ax.barh(top_causes.index[::-1], top_causes.values[::-1], color=bar_color, height=0.7)

# Title and labels
ax.set_title("Top 5 Primary Contributing Causes of Accidents", fontsize=18, fontweight='bold', pad=25)
ax.set_xlabel("Number of Accidents", fontsize=14, labelpad=12)
ax.set_ylabel("Contributing Cause", fontsize=14, labelpad=12)

# Improve readability of y-axis labels
ax.set_yticklabels(top_causes.index[::-1], fontsize=13, fontweight='bold', ha='right')

# Remove gridlines
ax.xaxis.grid(False)
ax.yaxis.grid(False)

# Keep tick marks for reference
ax.tick_params(axis="x", length=5, width=1)
ax.tick_params(axis="y", length=0)  # Remove ticks on y-axis for cleaner look

# Tighten layout
plt.tight_layout()

# Define output directory and save figure
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
plot_filename = os.path.join(output_dir, "top_5_contributing_causes.png")
fig.savefig(plot_filename, dpi=300, bbox_inches="tight")


# Plot 2
# Line Chart -Accidents by Hour of the Day
# Group by hour and count accidents
hourly_accidents = df["crash_hour"].value_counts().sort_index()

# Set up figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Select color for the line
line_color = "#7B287D"  # Dark magenta/plum

# Create line plot (No markers, no peak emphasis)
ax.plot(hourly_accidents.index, hourly_accidents.values, linestyle="-", 
        color=line_color, linewidth=3, alpha=0.9)

# Title and Labels
ax.set_title("Number of Traffic Accidents Throughout the Day", 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel("Hour of the Day (24-Hour Format)", fontsize=14, labelpad=12)
ax.set_ylabel("Number of Accidents", fontsize=14, labelpad=12)

# Improve X-axis tick labels (Show every hour
ax.set_xticks(range(0, 24, 1))  
ax.set_xticklabels(range(0, 24, 1), fontsize=12, fontweight='bold')

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Remove gridlines but keep tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)

# Apply tight layout
plt.tight_layout()

# Define output directory and save figure
plot_filename = os.path.join(output_dir, "traffic_accidents_trend.png")
fig.savefig(plot_filename, dpi=300, bbox_inches="tight")





# Plot 3
# Bar Chart - Total Injuries by Lighting Condition

# Aggregate total injuries by lighting condition (excluding 'Unknown')
lighting_totals = (
    df[df["lighting_condition"] != "UNKNOWN"]
    .groupby("lighting_condition")["injuries_total"]
    .sum()
    .sort_values(ascending=False)  # Sort highest to lowest
)

# Rename categories for clarity
rename_dict = {
    "DARKNESS, LIGHTED ROAD": "Dark - Lit Road",  # Improved clarity
    "DARKNESS": "Dark",
    "DAYLIGHT": "Daylight",
    "DAWN": "Dawn",
    "DUSK": "Dusk"
}

lighting_totals.index = [rename_dict.get(label, label.title()) for label in lighting_totals.index]

# Set up figure and axis
fig, ax = plt.subplots(figsize=(9, 6))

# Select a deep teal color
bar_color = "#007F73"  # Deep Teal

# Create the bar chart
ax.bar(lighting_totals.index, lighting_totals.values, color=bar_color, width=0.7)

# Title and labels
ax.set_title("Total Injuries by Lighting Condition", fontsize=16, fontweight="bold", pad=25)
ax.set_xlabel("Lighting Condition", fontsize=14, labelpad=10)
ax.set_ylabel("Total Injuries", fontsize=14, labelpad=10)

# Improve readability of x-axis labels
ax.set_xticklabels(lighting_totals.index, fontsize=12)

# Remove gridlines
ax.yaxis.grid(False)
ax.xaxis.grid(False)

# Save figure
plot_filename = os.path.join(output_dir, "injuries_by_lighting.png")
fig.savefig(plot_filename, dpi=300, bbox_inches="tight")



# Plot 4
# Matplotlib Grid -  Accidents by Day of Week and Hour

# Aggregate accidents by day of the week and hour
accidents_grid = df.groupby(["crash_day_of_week", "crash_hour"]).size().unstack()

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Colormap
cmap = "YlOrBr"
cax = ax.imshow(accidents_grid, aspect="auto", cmap=cmap, vmin=0, vmax=accidents_grid.values.max())

# Add colorbar with better scaling
cbar = fig.colorbar(cax)
cbar.set_label("Accident Frequency", fontsize=14)

# Set labels and improved title
ax.set_title("Traffic Accidents by Hour and Day of the Week", fontsize=16, fontweight="bold", pad=25)
ax.set_xlabel("Hour of the Day (24-Hour Format)", fontsize=14, labelpad=10)
ax.set_ylabel("Day of the Week", fontsize=14, labelpad=10)

# Format x-axis (0-23 hours) with gridlines
ax.set_xticks(np.arange(24))
ax.set_xticklabels(np.arange(24), fontsize=12)
ax.set_xticks(np.arange(24) - 0.5, minor=True) 

# Format y-axis (Days of the Week)
days_ordered = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
ax.set_yticks(np.arange(len(days_ordered)))
ax.set_yticklabels(days_ordered, fontsize=14)

# Add subtle gridlines
ax.grid(True, which="minor", linestyle="--", linewidth=0.5, alpha=0.3)

# Adjust layout
plt.subplots_adjust(left=0.22)

# Save figure
plot_filename = os.path.join(output_dir, "accidents_by_day_hour.png")
fig.savefig(plot_filename, dpi=300, bbox_inches="tight")

# Show plot
plt.show()
