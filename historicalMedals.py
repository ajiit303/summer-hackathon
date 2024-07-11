import re
import pandas as pd
import numpy as np
import plotly.express as px

# Load the data

medals = pd.read_csv('olympic_medals.csv') # Load the data

# print(medals)

# extract year from slug_game
medals["year"] = medals["slug_game"].apply(lambda x: int(re.search(r'\d{4}', x).group()))

# print(medals)

olympic_medals = medals[medals["year"] % 4 == 0] # Filter the data to only include years divisible by 4

# drop the temporary column
olympic_medals = olympic_medals.drop(columns=["year"], axis=1)

# print(olympic_medals[olympic_medals["country_name"] == "United States of America"])

medals_by_country = olympic_medals.groupby(["country_name", "discipline_title", "medal_type"]).size().reset_index(name="medals")

# print(medals_by_country[medals_by_country["country_name"] == "United States of America"])