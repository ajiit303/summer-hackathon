from tkinter import *
from tkinter import ttk
import pandas as pd
import re
import plotly.express as px
import plotly.io as pio
from sklearn.linear_model import LinearRegression
import numpy as np

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
def process_sport_data(sport, use_modern_names):
    sport_data = medals[medals['discipline_title'] == sport]
    
    # Creating df with relevant columns
    sport_data = sport_data[['event_title', 'slug_game', 'medal_type', 'rank_position', 'country_name', 'country_code', 'athlete_full_name']]
    
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

    if use_modern_names:
        # Applying country mapping for modern names
        sport_data['Country'] = sport_data['Country'].replace(country_mapping)

    return sport_data

# Function to show the data in the GUI
def show_data():
    selected_sport = sport_var.get()
    use_modern_names = modern_names_var.get() == "Modern"
    
    data = process_sport_data(selected_sport, use_modern_names)
    
    # Grouping by country and medal type, then pivoting
    medals_by_country_type = data.groupby(['Country', 'Medal']).size().unstack(fill_value=0)

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
    
    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Insert new data
    for index, row in medals_by_country_type.iterrows():
        tree.insert("", "end", values=list(row))

    if use_modern_names:
        show_map_button.pack()
        predict_button.pack()
    else:
        show_map_button.pack_forget()
        predict_button.pack_forget()

# Function to show the choropleth map
def show_map():
    selected_sport = sport_var.get()
    data = process_sport_data(selected_sport, True)
    
    # Grouping by country and medal type, then pivoting
    medals_by_country_type = data.groupby(['Country', 'Medal']).size().unstack(fill_value=0)

    # Adding a total medal count column
    medals_by_country_type['Total'] = medals_by_country_type.sum(axis=1)

    fig = px.choropleth(
        data_frame=medals_by_country_type.reset_index(),
        locations="Country",
        locationmode="country names",
        color="Total",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"Total Medals in {selected_sport} (Modern Country Names)"
    )
    fig.show()

# Function to show the bar chart
def show_bar_chart():
    selected_sport = sport_var.get()
    data = process_sport_data(selected_sport, modern_names_var.get() == "Modern")
    
    # Grouping by country and medal type, then pivoting
    medals_by_country_type = data.groupby(['Country', 'Medal']).size().unstack(fill_value=0)

    # Adding a total medal count column
    medals_by_country_type['Total'] = medals_by_country_type.sum(axis=1)
    
    fig = px.histogram(medals_by_country_type.reset_index(), x='Country', y='Total', 
                       title=f"Total Medals Won By Countries In Olympics {selected_sport}", 
                       barmode='stack')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    pio.show(fig)

# Function to predict the 2024 winners using linear regression
def predict_2024_winners():
    selected_sport = sport_var.get()
    data = process_sport_data(selected_sport, True)
    
    # Prepare the data for linear regression
    grouped_data = data.groupby(['Year', 'Country']).size().reset_index(name='Total Medals')
    modern_names_data = grouped_data.groupby('Country').sum().reset_index()

    # Train the linear regression model
    model = LinearRegression()
    
    # Dictionary to store predictions
    predictions = {}
    
    for country in modern_names_data['Country'].unique():
        country_data = grouped_data[grouped_data['Country'] == country]
        if len(country_data) >= 2:  # Ensure there is enough data to train the model
            X = country_data['Year'].values.reshape(-1, 1)
            y = country_data['Total Medals'].values
            model.fit(X, y)
            prediction = model.predict(np.array([[2024]]))
            predictions[country] = prediction[0]
    
    # Create DataFrame from predictions
    predictions_df = pd.DataFrame(list(predictions.items()), columns=['Country', 'Predicted 2024'])
    top_5_countries = predictions_df.nlargest(5, 'Predicted 2024')
    
    # Display the predictions in the GUI
    top_5_text = "Top 5 Predicted Countries for 2024:\n"
    for i, row in top_5_countries.iterrows():
        top_5_text += f"{i+1}. {row['Country']} - Predicted {row['Predicted 2024']:.2f} medals\n"
    
    # Show the predictions in a message box
    top_5_window = Toplevel(root)
    top_5_window.title("Prediction for 2024")
    Label(top_5_window, text=top_5_text, padx=10, pady=10).pack()

# Create the main window
root = Tk()
root.title("Olympic Data Viewer")

# Create the dropdown for sports
sport_label = Label(root, text="Select Sport:")
sport_label.pack()
sport_var = StringVar(value=summer_olympic_sports[0])
sport_dropdown = ttk.Combobox(root, textvariable=sport_var, values=summer_olympic_sports)
sport_dropdown.pack()

# Create the dropdown for country naming
modern_names_label = Label(root, text="Country Names:")
modern_names_label.pack()
modern_names_var = StringVar(value="Historic")
modern_names_dropdown = ttk.Combobox(root, textvariable=modern_names_var, values=["Historic", "Modern"])
modern_names_dropdown.pack()

# Create the button to show data
show_button = Button(root, text="Show Data", command=show_data)
show_button.pack()

# Create the button to show the map
show_map_button = Button(root, text="Show Choropleth Map", command=show_map)

# Create the button to show the histogram
show_histogram_button = Button(root, text="Show Histogram", command=show_bar_chart)
show_histogram_button.pack()

# Create the button to predict 2024 winners
predict_button = Button(root, text="Predict 2024 Winner", command=predict_2024_winners)

# Create the treeview to display data
tree = ttk.Treeview(root, columns=("Country", "Bronze", "Gold", "Silver", "Total Medals"), show='headings')
for col in tree['columns']:
    tree.heading(col, text=col)
tree.pack(expand=True, fill='both')

# Run the main loop
root.mainloop()
