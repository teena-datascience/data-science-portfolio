# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:48:07 2024

@author: 17323
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

"""Load the data set """
athlete_df=pd.read_csv('athlete_events.csv')
regions_df=pd.read_csv('noc_regions.csv')
# Display the shape of the data
print(athlete_df.head)


"""I want to work only on the summer season"""
#Filter data to include only Summer Olympics
athlete_df=athlete_df[athlete_df['Season']=='Summer']
print('Data including only Summer season:')
print(athlete_df.head())

"""Merge the athlete data with region data based on NOC"""
olympics_df=pd.merge(athlete_df,regions_df,on='NOC',how='left')
#convert all the column names in capitalized format
olympics_df.columns=olympics_df.columns.str.capitalize()
print(olympics_df.columns)

#Finding and removing duplicate rows
olympics_df.duplicated().sum() 
print("Number of duplicate rows:", olympics_df.duplicated().sum())
olympics_df.drop_duplicates(inplace=True)
print("Number of rows after removing duplicates:", len(olympics_df))

# Create dummy variables for medal types and concatenate them to the main dataframe
medal_count=pd.get_dummies(olympics_df['Medal'])
medal_count=medal_count.astype(int)
print("medal count:",medal_count)
#concatinate the  three new columns to my dataframe
olympics_df=pd.concat([olympics_df,medal_count],axis=1)
print(f"new dataframe with three added columns:\n{olympics_df.head(2)}")
olympics_df.groupby("Noc").sum()[['Gold','Silver','Bronze']].sort_values("Gold",ascending=False).reset_index()

"""Calculating the medal for every country"""
def medal_tally(olympics_df):
    # Drop duplicate rows based on relevant columns
    medal_tally=olympics_df.drop_duplicates(subset=['Team','Noc','Games','Year','City','Sport','Event','Medal'])
    # Create binary columns for each medal type
    medal_tally['Gold'] = (medal_tally['Medal'] == 'Gold').astype(int)
    medal_tally['Silver'] = (medal_tally['Medal'] == 'Silver').astype(int)
    medal_tally['Bronze'] = (medal_tally['Medal'] == 'Bronze').astype(int)
    # Group by region and sum medal counts
    medal_tally=medal_tally.groupby("Region").sum()[['Gold','Silver','Bronze']].sort_values("Gold",ascending=False).reset_index()
    # Calculate total medals
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally
print(f"Medal tally:\n {medal_tally(olympics_df)}")

"""Bar Plot for the top 10 countries by gold medals"""
# Get the medal tally DataFrame
tally_df = medal_tally(olympics_df)
# Sort and select top 10 regions by gold medals
top_10_gold = tally_df[['Region', 'Gold']].sort_values('Gold', ascending=False).head(10)
print(f"Top 10 countries with Gold medals:\n{top_10_gold}")
# Plot the chart
plt.figure(figsize=(12, 8))
sns.barplot(data=top_10_gold, x='Region', y='Gold', color="yellow")
# Add titles and labels
plt.title('Top 10 Countries by Gold Medals')
plt.xlabel('Region')
plt.ylabel('Number of Gold Medals')
plt.xticks(rotation=45)
plt.savefig('Gold_medal_plot_olympics.png',dpi=300)
plt.show()

"""Bar plot for top 5 countries by Gold Silver and Bronze medals"""
# Define a function to get top N countries for a specific medal type
def get_top_countries(tally_df, medal_type, top_n=5):
    return tally_df[['Region', medal_type]].sort_values(medal_type, ascending=False).head(top_n)

# Define a function to plot top countries for different medal types
def plot_medal_tally(tally_df, medal_types, top_n=5):
    # Create a subplot grid
    fig, axes = plt.subplots(nrows=1, ncols=len(medal_types), figsize=(20, 6), sharey=True)
    fig.suptitle(f'Top {top_n} Countries by Medals', fontsize=16)
    
    # Iterate over each medal type and plot
    for ax, medal_type in zip(axes, medal_types):
        top_countries = get_top_countries(tally_df, medal_type, top_n)
        sns.barplot(data=top_countries, x='Region', y=medal_type, palette='coolwarm', ax=ax)
        ax.set_title(f'Top {top_n} by {medal_type}')
        ax.set_xlabel('Country')
        ax.set_ylabel(f'{medal_type} Medals')
        ax.tick_params(axis='x', rotation=45)  # Rotate x labels for better readability

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('Medal_tally_plot_olympics2.png',dpi=300)
    plt.show()
medal_types = ['Gold', 'Silver', 'Bronze']
print("Top countries by medal type:")
print(plot_medal_tally(tally_df, medal_types))

"""OVERALL ANALYSIS"""
"""Analysis for Nations over time"""
#removing all the duplicate rows where Year and Region is the same
olympics_df.drop_duplicates(['Year','Region'])
#find how many participation countries were in each year and converting into a dataframe
nations_overtime=olympics_df.drop_duplicates(['Year','Region'])["Year"].value_counts().reset_index().sort_values('Year')
print(f"Nations over time:\n{nations_overtime}")

#Analysis for events over time
events_overtime=olympics_df.drop_duplicates(['Year','Event'])["Year"].value_counts().reset_index().sort_values('Year')
print(f"Events over time:\n{events_overtime}")

#Analysis for Athletes over time
athletes_overtime=olympics_df.drop_duplicates(['Year','Name'])["Year"].value_counts().reset_index().sort_values('Year')
print(f"Athlete over time:\n{athletes_overtime}")

"""Plotting with subplots for Overall Analysis"""
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 18), sharex=True)

# Plot for Nations over time
sns.lineplot(data=nations_overtime, x='Year', y='count', marker='o', color='blue', ax=axes[0])
axes[0].set_title('Number of Participating Countries Each Year')
axes[0].set_ylabel('Number of Countries')
axes[0].set_xlabel('')
axes[0].tick_params(axis='x', rotation=45)

# Plot for Events over time
sns.lineplot(data=events_overtime, x='Year', y='count', marker='o', color='green', ax=axes[1])
axes[1].set_title('Number of Events Each Year')
axes[1].set_ylabel('Number of Events')
axes[1].set_xlabel('')
axes[1].tick_params(axis='x', rotation=45)

# Plot for Athletes over time
sns.lineplot(data=athletes_overtime, x='Year', y='count', marker='o', color='red', ax=axes[2])
axes[2].set_title('Number of Athletes Each Year')
axes[2].set_ylabel('Number of Athletes')
axes[2].set_xlabel('Year')
axes[2].tick_params(axis='x', rotation=45)

# Adjust layout
plt.tight_layout()
plt.savefig('Lineplot_over_time.png', dpi=300)
plt.show()

"""Plotting a heatmap for number of events per Sport over the Years"""
# Create a pivot table for the heatmap
heatmap_data=olympics_df.drop_duplicates(["Year","Sport","Event"])
pivot_table=heatmap_data.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int)
print("Pivot Table Data:")
print(pivot_table.head())

# Plotting
plt.figure(figsize=(12,10))
heatmap = sns.heatmap(pivot_table, annot=True, annot_kws={"size": 10} )

# Add titles and labels
plt.title('Number of Events per Sport over the Years')
plt.xlabel('Year')
plt.ylabel('Sport')
# Adjust layout
plt.tight_layout(pad=2.0)
plt.savefig('Heatmapplot_events_per_sport.png', dpi=300)
plt.show()




"""COUNTRY WISE ANALYSIS"""

temp_df=olympics_df.dropna(subset='Medal')
print(temp_df)
temp_df.drop_duplicates(subset=['Team','Noc','Games','Year','City','Sport','Event','Medal'],inplace=True)

"""Country's Performance over the years"""
def plot_region_performance(olympics_df, region):
    
    new_df=temp_df[temp_df['Region']==region]
    final_df=new_df.groupby('Year').count()["Medal"].reset_index()
    final_df.rename(columns={'Medal': 'Medal Count'}, inplace=True)
    print(final_df)
    # Generate a complete list of years
    all_years = pd.DataFrame({'Year': range(final_df['Year'].min(), final_df['Year'].max() + 1)})
    # Merge with the performance data to include years with zero medals
    final_df = pd.merge(all_years, final_df, on='Year', how='left').fillna(0)
    print(final_df)
    """plotting"""
    sns.lineplot(data=final_df, x='Year', y='Medal Count', color='blue')
    plt.title(f'{region}\'s Overall Performance')
    plt.savefig(f'{region}_overall_performance.png', dpi=300)
    plt.show()
    return final_df
final_df = plot_region_performance(olympics_df, 'India')


"""Analysing the Best Performing Sport for Each Country"""
def plot_sport_performance_by_region(temp_df, region):
    
    new_df=temp_df[temp_df['Region']==region]
    performance=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    print(f"Best performing sport for {region}:\n {performance}")
    #plotting
    plt.figure(figsize=(12,10))
    sns.heatmap(performance, annot=True, annot_kws={"size": 10} )
    plt.title(f'Best Performing Sport for {region}')
    plt.savefig('Heatmap_best_sport.png', dpi=300)
    plt.show()
    return performance
performance_df = plot_sport_performance_by_region(temp_df, 'India')


"""ATHLETE WISE ANALYSIS"""

"""Age Distribution of Athletes by Medal Type"""
athlete_df=olympics_df.drop_duplicates(subset=['Name','Region'])
x1=athlete_df["Age"].dropna()
x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
plot_data = pd.DataFrame({
        'Age': pd.concat([x1, x2, x3, x4]),
        'Medal': ['All'] * len(x1) + ['Gold'] * len(x2) + ['Silver'] * len(x3) + ['Bronze'] * len(x4)
    })
 # Plotting
plt.figure(figsize=(14, 8))
sns.kdeplot(data=plot_data,x='Age',hue='Medal',multiple='stack',common_norm=False, )

plt.title('Age Distribution of Athletes by Medal Type')
plt.xlabel('Age')
plt.ylabel('Frequency')
    
    # Save and show the plot
plt.savefig('athlete_age_distribution_histogram.png', dpi=300)
plt.show()

"""weight and Height Distribution of Athletes by Medal Type"""
def plot_weight_height_distribution(olympics_df, sport_name):
    
    olympics_df["Medal"].fillna("No Medal",inplace=True)
    plt.figure(figsize=(12,10))
    temp_df=olympics_df[olympics_df["Sport"]==sport_name]
    scatter=sns.scatterplot(data=temp_df,x='Weight',y="Height",hue='Medal',style=temp_df['Sex'],s=100,alpha=0.5)
    plt.title(f'Weight and Height Distribution of Athletes in {sport_name}')
    plt.xlabel('Weight (in kg)')
    handles, labels = scatter.get_legend_handles_labels()
    plt.legend(
        handles=handles,
        labels=labels,
        title='Medal Type & Sex',
        bbox_to_anchor=(1.05, 0),  # Position legend to the lower right
        loc='lower left'
    )
    
    plt.savefig('weight_height_distribution_histogram.png', dpi=300,bbox_inches='tight')
    plt.show()
    return temp_df
plot_weight_height_distribution(olympics_df, "Weightlifting")

"""Gender diatribution over a pie chart"""
# Count the number of male and female athletes
gender_counts = olympics_df['Sex'].value_counts()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['#1f77b4', '#ff7f0e'])
plt.title('Distribution of Male and Female Athletes')
plt.axis('equal')

# Save and show the plot
plt.savefig('gender_distribution_pie_chart.png', dpi=300)
plt.show()

"""Men vs Women Participation"""
# Filter and group data by gender
men=olympics_df[olympics_df['Sex']=="M"].groupby('Year').count()['Name'].reset_index()
women=olympics_df[olympics_df['Sex']=="F"].groupby('Year').count()['Name'].reset_index()
# Rename columns for clarity
men.columns = ['Year', 'Number of Male Athletes']
women.columns = ['Year', 'Number of Female Athletes']
# Merge the data for plotting
final = men.merge( women, on='Year')
# Melt the DataFrame to long format for Seaborn
final_melted = final.melt(id_vars='Year', var_name='Gender', value_name='Number of Athletes')
plt.figure(figsize=(10, 8))
sns.lineplot(data=final_melted, x='Year', y='Number of Athletes', hue='Gender',marker='o')
plt.title('Men vs Women Participation in the Olympics')
plt.xticks(rotation=45)  # Rotate x labels for better readability
plt.legend(title='Gender')
plt.savefig('men_vs_women.png', dpi=300)
plt.show()


"""PART 3"""
"""Detailed Country Comparison"""
#using the medal_tally function for further analysis on top countries the basis 
#of Gold,Silver and Bronze medal
medal_counts = medal_tally(olympics_df)
# Print the medal counts for inspection
print(medal_counts)
# Select the top 10 countries based on the total number of medals
top_countries = medal_counts.head(10)
# Plotting
plt.figure(figsize=(14, 8))
top_countries_melted = top_countries.melt(id_vars='Region', value_vars=['Gold', 'Silver', 'Bronze'])
sns.barplot(data=top_countries_melted, x='Region', y='value', hue='variable', palette='viridis')
plt.title('Top 10 Countries by Total Medals (Broken Down by Medal Type)')
plt.xlabel('Country')
plt.ylabel('Number of Medals')
plt.xticks(rotation=45)
plt.legend(title='Medal Type')
plt.tight_layout()
plt.savefig('top_countries_medals.png', dpi=300)
plt.show()

"""Detailed Performance Analysis for India"""

# Filter data for India
india_df = olympics_df[olympics_df['Region'] == 'India']

# Aggregate medal counts by year and medal type
medal_counts_india = india_df.groupby(['Year', 'Medal']).size().unstack(fill_value=0).reset_index()
medal_counts_india.columns.name = None  # Remove columns name

print(medal_counts_india)
# Plotting
plt.figure(figsize=(12, 8))
plt.stackplot(medal_counts_india['Year'], 
              medal_counts_india['Gold'], 
              medal_counts_india['Silver'], 
              medal_counts_india['Bronze'],
              labels=['Gold', 'Silver', 'Bronze'],
              alpha=0.7)

# Adding titles and labels
plt.title('Distribution of Medal Types for India Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Medals')
plt.legend(loc='upper left')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.savefig('india_medal_distribution.png', dpi=300)
plt.show()


"""Top 10 athlete """
def analyze_top_athletes(olympics_df, top_n):

    # Filter for athletes with Gold medals
    gold_medals = olympics_df[olympics_df['Medal'] == 'Gold']
    # Count gold medals won by each athlete
    athlete_gold_count = gold_medals.groupby('Name').size().reset_index(name='Gold Medals')
    # Find top athletes with most gold medals
    top_athletes = athlete_gold_count.nlargest(top_n, 'Gold Medals')
    print(top_athletes)
# Detailed analysis of top athletes
    for athlete in top_athletes['Name']:
        athlete_data = gold_medals[gold_medals['Name'] == athlete]
        print(f"Details for {athlete}:")
        print(athlete_data[['Year', 'Sport', 'Event']])
        print("\n")
    return top_athletes
top_athletes_df = analyze_top_athletes(olympics_df, top_n=10)

#Bar chart for top athletes
plt.figure(figsize=(12, 8))
sns.barplot(data=top_athletes_df, x='Name', y='Gold Medals', palette='viridis')
plt.title('Top 10 Athletes with Most Gold Medals')
plt.xlabel('Athlete')
plt.ylabel('Number of Gold Medals')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_gold_medalists.png', dpi=300)
plt.show()

"""Individual athlete performance"""
def analyze_and_plot_athlete_medals(olympics_df, athlete_name):
    # Filter the dataset for the specified athlete
    athlete_data = olympics_df[olympics_df['Name'] == athlete_name]
    if athlete_data.empty:
        print(f"No data found for athlete: {athlete_name}")
        return None

    # Aggregate medal counts by year
    medal_counts = athlete_data.groupby(['Year', 'Medal']).size().unstack(fill_value=0).reset_index()
    medal_counts.columns.name = None  # Remove columns name
    # Ensure that all expected medal columns are present
    for medal_type in ['Gold', 'Silver', 'Bronze']:
        if medal_type not in medal_counts.columns:
            medal_counts[medal_type] = 0
    # Print medal counts
    print(f"Medal Counts for {athlete_name}:")
    print(medal_counts)
    
    # Plotting
    plt.figure(figsize=(14, 8))
    
    # Plot bars for each type of medal
    medal_counts.set_index('Year')[['Gold', 'Silver', 'Bronze']].plot(kind='bar', stacked=True, color=['gold', 'silver', '#cd7f32'])
    
    plt.title(f'{athlete_name}\'s Medal Counts by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.xticks(rotation=45)
    plt.legend(title='Medal Type')
    plt.tight_layout()
    
    # Save and show the plot
    plt.savefig(f'{athlete_name}_medal_counts_by_year.png', dpi=300)
    plt.show()

    return medal_counts

# Example usage
athlete_name = 'Michael Fred Phelps, II'  # Replace with the athlete's name you want to analyze
athlete_medal_counts_df = analyze_and_plot_athlete_medals(olympics_df, athlete_name)

##saving the processed/final results dataframe to csv
olympics_df.to_csv("result_data_file.csv")