from time import sleep
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import plotly.express as px

# Load the data
medals = pd.read_csv('olympic_results.csv')

# List of summer Olympic sports
summer_olympic_sports = [
    'Shooting', 'Diving', 'Canoe Sprint', 'Cycling Road', 'Football', 'Boxing',
    'Artistic Swimming', 'Handball', 'Rugby Sevens', 'Cycling BMX Racing', 'Triathlon',
    'Surfing', 'Table Tennis', 'Canoe Slalom', 'Trampoline Gymnastics', 'Volleyball',
    'Basketball', 'Taekwondo', 'Cycling Track', 'Fencing', 'Badminton', 'Water Polo',
    'Sport Climbing', 'Wrestling', 'Tennis', 'Artistic Gymnastics', 'Golf',
    'Cycling BMX Freestyle', 'Judo', 'Skateboarding', 'Archery', 'Weightlifting',
    'Baseball/Softball', 'Equestrian', 'Modern Pentathlon', 'Athletics', 'Swimming',
    'Sailing', 'Cycling Mountain Bike', 'Rowing', 'Karate', '3x3 Basketball',
    'Rhythmic Gymnastics', 'Hockey', 'Beach Volleyball'
]

# Country mapping dictionary
country_mapping = {
    'West Germany': 'Germany',
    'East Germany': 'Germany',
    'German Democratic Republic (Germany)': 'Germany',
    'Federal Republic of Germany': 'Germany',
    'Soviet Union': 'Russia',
    'Russia': 'Russia',
    'Russian Federation': 'Russia',
    'ROC': 'Russia',
    'Czechoslovakia': 'Czech Republic',
    'Czech Republic': 'Czech Republic',
    'Yugoslavia': 'Serbia',
    'Serbia and Montenegro': 'Serbia',
    'United States of America': 'USA',
    'People\'s Republic of China': 'China',
}

# Function to process each sport
def process_sport_data(sport):
    print(f"Processing data for {sport}...")

    sport_data = medals[medals['discipline_title'] == sport]
    
    # Creating df with relevant columns
    sport_data = sport_data[['event_title', 'slug_game', 'medal_type', 'rank_position', 'country_name', 'country_code', 'athlete_full_name']]

    # Resetting index
    sport_data.reset_index(drop=True, inplace=True)

    # Extracting host city
    sport_data['Host City'] = sport_data['slug_game'].str.rsplit('-').str[0]
    sport_data['Host City'] = sport_data['Host City'].str.title()

    # Extracting gender
    sport_data['Gender'] = sport_data['event_title'].str.extract(r'(women|men)', flags=re.IGNORECASE)
    sport_data['Gender'] = sport_data['Gender'].str.title()

    # Extracting host year
    sport_data['Year'] = sport_data['slug_game'].str[-4:].astype(int)

    # Dropping slug_game
    sport_data.drop(columns='slug_game', inplace=True)

    # Cleaning the athlete_full_names
    sport_data['athlete_full_name'] = sport_data['athlete_full_name'].fillna('Team ' + sport_data['country_name'])

    # Giving a more readable name
    sport_data.rename(columns={
        'event_title': 'Event',
        'medal_type': 'Medal',
        'rank_position': 'Rank',
        'country_name': 'Country',
        'country_code': 'Country Code',
        'athlete_full_name': 'Athlete',
    }, inplace=True)

    # Grouping by country and medal type, then pivoting
    medals_by_country_type = sport_data.groupby(['Country', 'Medal']).size().unstack(fill_value=0)

    # Adding a total medal count column
    medals_by_country_type['Total'] = medals_by_country_type.sum(axis=1)

    # Sorting by total medal count in descending order
    medals_by_country_type = medals_by_country_type.sort_values(by='Total', ascending=False).reset_index()

    # Renaming columns for better readability
    medals_by_country_type.columns.name = None
    medals_by_country_type.rename(columns={
        'Country': 'Country',
        'gold': 'Gold',
        'silver': 'Silver',
        'bronze': 'Bronze',
        'Total': 'Total Medals'
    }, inplace=True)

    print(f"With historical names:\n")
    print(medals_by_country_type)

    # Applying country mapping
    sport_data['Country'] = sport_data['Country'].replace(country_mapping)

    # Grouping by country and medal type, then pivoting
    medals_by_country_type = sport_data.groupby(['Country', 'Medal']).size().unstack(fill_value=0)

    # Adding a total medal count column
    medals_by_country_type['Total'] = medals_by_country_type.sum(axis=1)

    # Sorting by total medal count in descending order
    medals_by_country_type = medals_by_country_type.sort_values(by='Total', ascending=False).reset_index()

    # Renaming columns for better readability
    medals_by_country_type.columns.name = None
    medals_by_country_type.rename(columns={
        'Country': 'Country',
        'gold': 'Gold',
        'silver': 'Silver',
        'bronze': 'Bronze',
        'Total': 'Total Medals'
    }, inplace=True)

    print(f"Without historical names for:\n")
    print(medals_by_country_type)

# Process each sport and display the results
for sport in summer_olympic_sports:
    process_sport_data(sport)
