import re
import pandas as pd
import numpy as np
import plotly.express as px

# Load the data

medals = pd.read_csv('olympic_medals.csv') # Load the data

# print(medals)

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

# drop the temporary column
summer_olympic_medals = summer_olympic_medals.drop("year", axis=1)
# print(summer_olympic_medals)

# Group by country, sport, and medal type, and count the occurrences
medals_by_country = summer_olympic_medals.groupby(["country_name", "discipline_title", "medal_type"]).size().reset_index(name="medals")

print(medals_by_country)
