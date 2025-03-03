"""""
top_spotify_songs.py

Python 3 
This script generates data visualizations for the top Spotify songs
and their trends for over 70 countries using Matplotlib's interface.

Author: Charity Smith
""" 

#%%
# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects  
import os
import numpy as np
import seaborn as sns
import matplotlib.ticker as mticker
import plotly.express as px
import pycountry
import networkx as nx


dpi = 300

# file path
project_dir = r''
data_dir = project_dir + r'data/'
output_dir = project_dir + r'output/'

#%%

# Data Source: Top Spotify Songs in 73 Countries
# https://www.kaggle.com/datasets/anandshaw2001/top-spotify-songs-in-73-countries/data
# Load the cleaned dataset
data_filename = "Top_spotify_songs_cleaned.csv"
df = pd.read_csv(data_dir + data_filename)

# Load the cleaned dataset
data_filename = "Top_spotify_songs_cleaned.csv"
df = pd.read_csv(data_dir + data_filename)


# Plot 1: Bar Chart - Most Popular Artists
# Normalize artist names (capitalize first letter of each word)
df["artists"] = df["artists"].str.title().str.strip()

# Count the number of times each artist appears in the Top 50
artist_counts = df["artists"].value_counts().head(5)  # Top 5 artists

# Sort so the most popular artist is at the top
artist_counts = artist_counts.sort_values(ascending=True)  # Reverse order for proper bar chart

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Horizontal bar chart
ax.barh(artist_counts.index, artist_counts.values, height=0.55, color="#29A76C") 

# Formatting improvements
ax.set_title("Top Artists in Spotify’s Global Top 50 (2025)", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Appearances in Top 50", fontsize=14, fontweight="bold", labelpad=10)
ax.set_ylabel("Artists", fontsize=14, fontweight="bold", labelpad=10)
ax.grid(False)  # Removing gridlines for a cleaner look

# Increase spacing between bars
plt.subplots_adjust(left=0.3)  

# Add a y-axis line
ax.spines["left"].set_visible(True)
ax.spines["left"].set_linewidth(1.2)

# Save the plot
os.makedirs(output_dir, exist_ok=True)  
plot_filename = os.path.join(output_dir, "top_5_popular_artists.png")
fig.savefig(plot_filename, dpi=dpi, bbox_inches="tight")



# Plot 2: Histogram - Distribution of Song Popularity Scores

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Histogram of song popularity scores
ax.hist(df["popularity"], bins=35, color="#6A0DAD", edgecolor="black", alpha=0.7)

# Formatting improvements
ax.set_title("Distribution of Song Popularity Scores (Spotify, 2025)", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Popularity Score", fontsize=14, fontweight="bold", labelpad=12)
ax.set_xticks(range(0, 110, 10))  # Set ticks every 10 points

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x//1000)}K")) # Convert to 'K' format, no decimals
ax.set_ylabel("Number of Songs", fontsize=14, fontweight="bold", labelpad=10)

ax.xaxis.set_tick_params(pad=5)
ax.yaxis.set_tick_params(pad=5)

ax.grid(False)  # Removing gridlines for a cleaner look

plt.margins(x=0.01, y=0.03)  # Reduce extra white space

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Save the plot
os.makedirs(output_dir, exist_ok=True)  
plot_filename = os.path.join(output_dir, "song_popularity_distribution.png")
fig.savefig(plot_filename, dpi=dpi, bbox_inches="tight")



# Plot 3: Box Plot: Popularity Scores by Explicit vs. Non-Explicit Songs (using Seaborn

# Convert boolean labels to "Explicit" and "Non-Explicit"
df["is_explicit"] = df["is_explicit"].replace({True: "Explicit", False: "Non-Explicit"})

# Create the figure
fig, ax = plt.subplots(figsize=(8, 6))

# Box plot with improved width
sns.boxplot(x="is_explicit", y="popularity", data=df, palette="Purples", ax=ax, showfliers=False, width=0.7)

# Formatting
ax.set_title("Popularity of Explicit vs. Non-Explicit Songs", fontsize=18, fontweight="bold", pad=15)
ax.set_xlabel("Song Type", fontsize=14, fontweight="bold", labelpad=10)
ax.set_ylabel("Popularity Score", fontsize=14, fontweight="bold", labelpad=10)

# Improve y-axis tick spacing
ax.yaxis.set_major_locator(mticker.MultipleLocator(10))  # Tick labels every 10 points

# Save the plot
plot_filename = os.path.join(output_dir, "explicit_vs_nonexplicit_popularity.png")
fig.savefig(plot_filename, dpi=dpi, bbox_inches="tight")

# Show plot
plt.show()


# Plot 4: Choropleth Map - Average Popularity by Country

# Ensure the country column is a string
df["country"] = df["country"].astype(str)

# Function to convert ISO-2 to ISO-3
def convert_iso2_to_iso3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except AttributeError:
        return None  # Return None for invalid country codes

# Apply conversion
df["country"] = df["country"].astype(str).str.upper()  # Ensure uppercase
df["country"] = df["country"].apply(convert_iso2_to_iso3)


# Drop rows where conversion failed
df = df.dropna(subset=["country"])


# Group by country and calculate average popularity
country_popularity = df.groupby("country")["popularity"].mean().reset_index()

# Create the choropleth map
fig = px.choropleth(
    country_popularity,
    locations="country",  
    locationmode="ISO-3",  
    color="popularity",
    hover_name="country",
    color_continuous_scale="Purples",
    title="Average Popularity of Songs by Country (Spotify, 2025)",
)

# Formatting for better appearance
fig.update_layout(
    title_font=dict(size=18, family="Arial", color="black"),
    geo=dict(showframe=False, showcoastlines=False, projection_type="natural earth"),
)

# Save the plot
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "choropleth_spotify_popularity.png")
fig.write_image(plot_filename, scale=3)

# Save the interactive map as an HTML file
html_filename = os.path.join(output_dir, "choropleth_spotify_popularity.html")
fig.write_html(html_filename)

# Show the plot
plt.show()









