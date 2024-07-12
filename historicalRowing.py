from time import sleep
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px
import re 
import os

# Specify the directory where your input data files are stored
# input_directory = './input'  # Update this to the correct path on your local machine

# import CSV file 'results'
medals = pd.read_csv('olympic_results.csv') # Update this to the correct path on your local machine
#print(medals)

#retriving Rowing from all discipline
rowing = medals[medals['discipline_title']=='Rowing']

#creating df with relevant columns
rowing = rowing[['event_title',
                 'slug_game',
                 'medal_type',
                 'rank_position',
                 'country_name',
                 'country_code',
                 'athlete_full_name']]

#resetting index
rowing.reset_index()

#extracting host city
rowing['Host City'] = rowing['slug_game'].str.rsplit('-').str[0]
rowing['Host City'] = rowing['Host City'].str.title()

#extracting gender
rowing['Gender'] = rowing['event_title'].str.extract(r'(women|men)', flags=re.IGNORECASE)
rowing['Gender'] = rowing['Gender'].str.title()
#extracting host year
rowing['Year'] = rowing['slug_game'].str[-4:].astype(int)

#dropping slug_game
rowing.drop(columns='slug_game', inplace=True)

#cleaning the athlete_full_names
rowing['athlete_full_name'] = rowing['athlete_full_name'].fillna('Team ' + rowing['country_name'])

#cleaning the event name
rowing.loc[rowing['event_title'].isin(['eight with coxswain 8 men', 'Coxed Eights Men', "Men's Eight"]), 'event_title']="Men's Eight 8+"
rowing.loc[rowing['event_title'].isin(['four-oared shell with coxswain men','four-oared shell with coxswain men - Final 1','four-oared shell with coxswain men - Final 2',"Men's Four"]), 'event_title']= "Men's Four 4+"
rowing.loc[rowing['event_title'].isin(['four without coxswain 4 men','Coxless Fours Men']), 'event_title']= "Men's Coxless Four 4-"
rowing.loc[rowing['event_title'].isin(['single sculls 1x men', "Men's Single Sculls"]), 'event_title']= "Men's Single Sculls 1x"
rowing.loc[rowing['event_title'].isin(['double sculls 2x men', 'Double Sculls Men',"Men's Double Sculls"]), 'event_title']="Men's Double Sculls 2x"
rowing.loc[rowing['event_title'].isin(['pair without coxswain 2 men','pair-oared shell with coxswain men', 'Coxless Pairs Men',"Men's Pair"]), 'event_title']="Men's Pair 2-"
rowing.loc[rowing['event_title'].isin(['double sculls 2x women', 'Double Sculls Women',"Women's Double Sculls"]), 'event_title']="Women's Double Sculls 2x"
rowing.loc[rowing['event_title'].isin(['pair without coxswain 2 women', "Women's Pair"]), 'event_title']="Women's Pair 2-"
rowing.loc[rowing['event_title'].isin(['quadruple sculls without coxsw women','quadruple sculls without coxswain women','quadruple sculls without coxswain (4x) women', "Women's Quadruple Sculls"]), 'event_title']="Women's Quadruple Sculls 4x"
rowing.loc[rowing['event_title'].isin(['quadruple sculls without coxsw men','quadruple sculls without coxswain women','Quadruple Sculls Men', "Men's Quadruple Sculls", 'quadruple sculls without coxswain (4x) men']), 'event_title']= "Men's Quadruple Sculls 4x"
rowing.loc[rowing['event_title'].isin(['single sculls 1x women', "Women's Single Sculls"]), 'event_title']="Women's Single Sculls 1x"
rowing.loc[rowing['event_title'].isin(['eight with coxswain 8 women',"Women's Eight"]), 'event_title']="Women's Eight 8+"
rowing.loc[rowing['event_title'].isin(['lightweight coxless four 4 men']), 'event_title']="Lightweight Men's Coxless Four 4-"
rowing.loc[rowing['event_title'].isin(['lightweight double sculls 2x women',"Lightweight Women's Double Sculls"]), 'event_title']="Lightweight Women's Double Sculls 2x"
rowing.loc[rowing['event_title'].isin(['quadruple sculls with coxswain women','quadruple sculls with coxswain (4x) women' ]), 'event_title']= "Women's Coxed Quad Sculls 4x+"
rowing.loc[rowing['event_title'].isin(['lightweight double sculls 2x men',"Lightweight Men's Double Sculls"]), 'event_title']="Lightweight Men's Double Sculls 2x"
rowing.loc[rowing['event_title'].isin(['quadruple sculls with coxswain 4x men']), 'event_title']= "Men's Coxed Quad Sculls 4x+"
rowing.loc[rowing['event_title'].isin(['coxless four 4 women']), 'event_title']= "Women's Coxless Four 4-"
rowing.loc[rowing['event_title'].isin(['fouroared shell with coxswain 4 women', "Women's Four"]), 'event_title']= "Women's Four 4+"

#giving a more readable name
rowing.rename(columns={
    'event_title':'Event',
    'medal_type': 'Medal',
    'rank_position': 'Rank',
    'country_name': 'Country',
    'country_code': 'Country Code',
    'athlete_full_name': 'Athlete',
    },inplace=True)

rowing_rank=rowing.copy()

#cleaning the medal_type 
rowing = rowing[rowing['Medal'].notna()]



'''
@TODO: pic did not show up
Top 10 Medal Winning Athlete In Single Sculling
As the dataset do not provide the athlete names for the Team event, 
the single sculling event is the only event we can study.

From the bar chart, we can observe that 
Yekaterina Khodotovich_Karsten is top medal winner in single sculling with have 4 medals in total.

However, we can also observe that Vyacheslav IVANOV and Pertti KARPPINEN 
are the athlete winning most Gold medal in single sculling.
'''
#removing all team game 
df2 = rowing.drop(rowing[rowing['Athlete'].str.contains('Team')].index)
#getting the plot
sort_order=['BRONZE','SILVER','GOLD']
df2_temp = df2.groupby(['Athlete']).agg(Total_medal_count=('Medal', 'count')).sort_values('Total_medal_count',ascending=False).head(10).reset_index()
df2 = df2.groupby(['Athlete','Medal']).agg(Medal_count=('Medal','count')).sort_values('Medal',key=lambda x: x.map({v: i for i, v in enumerate(sort_order)}),ascending=False).reset_index()
df2 = df2_temp.merge(df2)
#print(df2)

fig = px.bar(df2, orientation='h', x='Medal_count', y='Athlete', color='Medal', title='Top 10 Medal Winning Athletes In Single Sculling')
fig.update_yaxes(categoryorder='total descending')
fig.update_layout(legend_title_text='Number of Medals')
#fig.show()

del df2, df2_temp

##############################
#Top Medal Winning Countries#
##############################
df3 = rowing.groupby(['Country','Medal']).agg(Medal_count=('Medal','size')).sort_values('Medal_count',ascending=False).reset_index()
#print(df3)

'''
@TODO: pic did not show up
USA is the top medal winning country
1st: USA 
2nd: UK 
3rd: East Germany
However, we can obseve that Germany is in 3rd place, 
Germany Democratic Republic (East Germany) is in 4th place 
Federal Republic of Germany (West Germany) is in 18th place.
'''
#producing histogram for top winning country.
sleep(5)
fig = px.histogram(df3, x='Country', y='Medal_count',hover_name='Country',  color='Medal', title='Top Medal Winning Countries In Olympics Rowing')
fig.update_xaxes(categoryorder='total descending')
fig.update_layout(legend_title_text='Medal')
fig.show()

del df3

new_rowing = rowing.copy()
new_rowing['Country'] = new_rowing['Country'].replace('German Democratic Republic (Germany)', 'Germany')
new_rowing['Country'] = new_rowing['Country'].replace('Federal Republic of Germany', 'Germany')
new_rowing['Country'] = new_rowing['Country'].replace('Soviet Union', 'Russian Federation')
new_rowing['Country'] = new_rowing['Country'].replace('ROC', 'Russian Federation')

df4 = new_rowing.groupby(['Country','Medal']).agg(Medal_count=('Medal','size')).sort_values('Medal_count',ascending=False).reset_index()
#print(df4)
'''
Germany become the **top** medal winning country
1st: Germany 
2nd: USA 
3rd: UK
'''

#producing histogram for top winning country.
fig = px.histogram(df4, x='Country', y='Medal_count',hover_name='Country',  color='Medal', title='Top Medal Winning Countries In Olympics Rowing')
fig.update_xaxes(categoryorder='total descending')
fig.update_layout(legend_title_text='Medal')
#fig.show()

del df4
df5 = new_rowing.groupby(['Country','Medal','Event']).agg(Medal_count=('Medal','size')).sort_values('Medal_count',ascending=False).reset_index()
#print(df5)

fig = px.histogram(df5, x='Country', y='Medal_count',hover_name='Country',  color='Event', title='Top Medal Winning Countries and Event')
fig.update_layout(legend_title_text='Sport')

del df5

'''
Distribution of Overall Medal Winning on World Map
Eroupe is continent that get the most medals in Olypmics Rowing
It might imply that Eroupean countries have the advantage of rowing.
'''

df6 = new_rowing.groupby(['Country']).agg(Medal_count=('Medal','size')).sort_values('Medal_count',ascending=False).reset_index()
print(df6)
fig= px.choropleth(
    df6,
    locations="Country",
    locationmode='country names',
    color='Medal_count',
    hover_name='Medal_count', 
    title="Distribution of Overall Medal Winning on World Map",
    color_continuous_scale=px.colors.sequential.Darkmint)
fig.show() 

del df6


'''
The Trend of Overall Medal Winning Among Countries
'''
df7 = new_rowing.groupby(['Country','Year']).agg(Medal_count=('Medal','size')).sort_values('Year',ascending=True).reset_index()
pivot_data = df7.pivot(index='Year', columns='Country', values='Medal_count')
pivot_data = pivot_data.fillna(0)

import plotly.graph_objects as go
# Create the interactive plot
fig = go.Figure()

# Add a trace for each country
for country in pivot_data.columns:
    fig.add_trace(go.Scatter(x=pivot_data.index, y=pivot_data[country], mode='lines', name=country))

# Customize the layout
fig.update_layout(
    title='Trend of Gold Medal Counts for Each Country',
    xaxis_title='Year',
    yaxis_title='Gold Medal Count',
    xaxis_type='category',
    legend_title_text='Country',
    legend_orientation='h',
    legend_x=0,
    legend_y=-0.2
)
fig.show()

'''
The Trend of Gold Medal Winning Among Countries
'''
df7 = new_rowing.groupby(['Country','Medal','Year']).agg(Medal_count=('Medal','size')).sort_values('Year',ascending=True).reset_index()
gold = df7.loc[df7["Medal"]=="GOLD"]
pivot_data = gold.pivot(index='Year', columns='Country', values='Medal_count')
pivot_data = pivot_data.fillna(0)

import plotly.graph_objects as go
# Create the interactive plot
fig = go.Figure()

# Add a trace for each country
for country in pivot_data.columns:
    fig.add_trace(go.Scatter(x=pivot_data.index, y=pivot_data[country], mode='lines', name=country))

# Customize the layout
fig.update_layout(
    title='Trend of Gold Medal Counts for Each Country',
    xaxis_title='Year',
    yaxis_title='Gold Medal Count',
    xaxis_type='category',
    legend_title_text='Country',
    legend_orientation='h',
    legend_x=0,
    legend_y=-0.2
)

# Display the interactive plot
fig.show()
