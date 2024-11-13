import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
housing_data = pd.read_csv("housing_data.csv") # Contains columns "Year", "AvgHomePrice", "AdjForInflation"
nasdaq_data = pd.read_csv("nasdaq_annual_data.csv") # Contains columns "Year" and "NASDAQ"
presidents_data = pd.read_csv("presidents.csv") # Contains columns "President", "Start Year", "End Year", "Party"

# Print the DataFrames to verify data loading
print(housing_data.head())
print(nasdaq_data.head())
print(presidents_data.head())

# Merge datasets on Year
merged_data = pd.merge(housing_data, nasdaq_data, on='Year', how='inner')

# Add party information for presidents
for index, row in presidents_data.iterrows():
    start_year = row['Start Year']
    end_year = row['End Year'] if str(row['End Year']) != '-' else 2024
    merged_data.loc[(merged_data['Year'] >= start_year) & (merged_data['Year'] <= end_year), 'Party'] = row['Party']

# Plotting
plt.figure(figsize=(14, 10))

# Subplot 1: NASDAQ
plt.subplot(2, 1, 1)
sns.lineplot(data=merged_data, x='Year', y='NASDAQ', label='NASDAQ', color='blue')
plt.title('NASDAQ Over Years')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

# Subplot 2: Average Home Price and Home Price Adjusted for Inflation with Party Background
plt.subplot(2, 1, 2)
sns.lineplot(data=merged_data, x='Year', y='AvgHomePrice', label='Average Home Price', color='orange')
sns.lineplot(data=merged_data, x='Year', y='AdjForInflation', label='Home Price Adjusted for Inflation', color='green')

# Create a palette for party colors
party_colors = {'Republican': 'red', 'Democrat': 'blue'}
# Plot the party information as background
for year, group in merged_data.groupby('Year'):
    party = group['Party'].iloc[0]
    if party in party_colors:
        plt.axvspan(year - 0.5, year + 0.5, color=party_colors[party], alpha=0.2)

plt.title('Average Home Price and Home Price Adjusted for Inflation with Party Background')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("output.png")