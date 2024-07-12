import re
from time import sleep
import pandas as pd
import numpy as np
import plotly.express as px

# Load the data

medals = pd.read_csv('olympic_medals.csv')

# Extract year from slug_game
medals["year"] = medals["slug_game"].apply(lambda x: int(re.search(r'\d{4}', x).group()))

# Define Summer Olympic sports
summer_olympic_sports = [
    '3x3 Basketball', 'Archery', 'Artistic Gymnastics', 'Artistic Swimming', 'Athletics',
    'Badminton', 'Baseball', 'Baseball/Softball', 'Basketball', 'Beach Volleyball',
    'Boxing', 'Canoe Marathon', 'Canoe Slalom', 'Canoe Sprint', 'Cricket', 'Cycling BMX',
    'Cycling BMX Freestyle', 'Cycling BMX Racing', 'Cycling Mountain Bike', 'Cycling Road',
    'Cycling Track', 'Diving', 'Equestrian', 'Fencing', 'Football', 'Golf', 'Gymnastics Artistic',
    'Gymnastics Rhythmic', 'Handball', 'Hockey', 'Judo', 'Karate', 'Lacrosse', 'Marathon Swimming',
    'Modern Pentathlon', 'Polo', 'Rhythmic Gymnastics', 'Rowing', 'Rugby', 'Rugby Sevens',
    'Sailing', 'Shooting', 'Skateboarding', 'Softball', 'Sport Climbing', 'Surfing', 'Swimming',
    'Synchronized Swimming', 'Table Tennis', 'Taekwondo', 'Tennis', 'Trampoline', 'Triathlon',
    'Volleyball', 'Water Polo', 'Weightlifting', 'Wrestling'
]

# Filter the dataset to include only Summer Olympic sports
summer_olympic_medals = medals[medals["discipline_title"].isin(summer_olympic_sports)]

# Group by country, sport, year, and medal type, and count the occurrences
medals_by_year_by_sport = summer_olympic_medals.groupby(["country_name", "discipline_title", "medal_type", "year"]).size().reset_index(name="medals")

# Group by country, sport, and medal type, and count the occurrences
medals_by_year = summer_olympic_medals.groupby(["country_name", "discipline_title", "medal_type"]).size().reset_index(name="medals")

# Group by country to get the total number of medals
total_medals_by_country = medals_by_year.groupby("country_name")["medals"].sum().reset_index()

# Create a stacked bar chart
fig = px.bar(total_medals_by_country, x='country_name', y='medals', title='Total Medals by Country and Type',
             labels={'medals': 'Number of Medals', 'country_name': 'Country'},
             text='medals')

# Adjust the layout to ensure all country names are visible
fig.update_layout(
    barmode='stack',
    xaxis={'categoryorder':'total descending', 'tickangle': -45},
    margin={'t': 50, 'b': 150},
    height=800,
    width=1200
)

fig.show()

##########################################################
# GETTING RID OF THE HISTORICAL NAMES
##########################################################

# Comprehensive mapping of historical and duplicate country names to current equivalents
country_mapping = {
    "Soviet Union": "Russia",
    "Russian Federation": "Russia",
    "Russia": "Russia",
    "Yugoslavia": ["Serbia", "Croatia", "Slovenia", "Bosnia and Herzegovina", "Montenegro", "North Macedonia"],
    "East Germany": "Germany",
    "West Germany": "Germany",
    "German Democratic Republic (Germany)": "Germany",
    "Federal Republic of Germany": "Germany",
    "Germany": "Germany",
    "Czechoslovakia": ["Czech Republic", "Slovakia"],
    "United Arab Republic": ["Egypt", "Syria"],
    "Serbia and Montenegro": ["Serbia", "Montenegro"],
    "Bohemia": "Czech Republic",
    "China, People's Republic of": "China",
    "Hong Kong, China": "Hong Kong",
    "Republic of Korea": "South Korea",
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Republic of": "North Korea",
    "Great Britain": "United Kingdom",
    "United Kingdom": "United Kingdom",
    "United States of America": "United States",
    "United States": "United States",
    "Taiwan": "Chinese Taipei",
    "Chinese Taipei": "Chinese Taipei"
}

# Function to map historical and duplicate countries to current equivalents
def normalize_country_names(country):
    for hist, current in country_mapping.items():
        if country == hist:
            return current if isinstance(current, str) else current[0]  # Choose the first successor state
    return country

# Apply the function to the country_name column
summer_olympic_medals['country_name'] = summer_olympic_medals['country_name'].apply(normalize_country_names)

# Group by country, sport, and medal type, and count the occurrences
medals_by_year_updated = summer_olympic_medals.groupby(["country_name", "discipline_title", "medal_type"]).size().reset_index(name="medals")

# Group by country, sport, year, and medal type, and count the occurrences
medals_by_year_by_sport_updated = summer_olympic_medals.groupby(["country_name", "discipline_title", "medal_type", "year"]).size().reset_index(name="medals")

# Group by country to get the total number of medals
total_medals_by_country_updated = medals_by_year_updated.groupby("country_name")["medals"].sum().reset_index()

sleep(5)
# Create a stacked bar chart for the updated data
fig_updated = px.bar(total_medals_by_country_updated, x='country_name', y='medals', title='Total Medals by Country (Updated)',
                     labels={'medals': 'Number of Medals', 'country_name': 'Country'},
                     text='medals')

# Adjust the layout to ensure all country names are visible
fig_updated.update_layout(
    barmode='stack',
    xaxis={'categoryorder':'total descending', 'tickangle': -45},
    margin={'t': 50, 'b': 150},
    height=800,
    width=1200
)


fig_updated.show()
