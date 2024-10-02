import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit application title
st.title('Welcome to Rental Bike Analysis!')

# Load data
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Convert 'dteday' to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Data for pie chart
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
rentals = [471348, 918589, 1061129, 841613]  
colors = ['#72BCD4', '#FF6F61', '#93C572', '#E67F0D'] 
explode = (0.05, 0, 0, 0)  

# Section for pie chart
st.header("Proportion of Total Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    x=rentals,
    labels=seasons,
    autopct='%1.1f%%',  
    colors=colors,
    explode=explode,
    shadow=True,  
    startangle=90 
)
ax.set_title("Proportion of Total Bike Rentals by Season", fontsize=16)

# Display the pie chart in Streamlit
st.pyplot(fig)

# Filter the data for each year
df_2011 = day_df[day_df['yr'] == 0]
df_2012 = day_df[day_df['yr'] == 1]

# Set 'dteday' as the index
df_2011.set_index('dteday', inplace=True)
df_2012.set_index('dteday', inplace=True)

# Generate monthly reports
monthly_report_2011 = df_2011.resample('M').agg({
    'instant': 'nunique',
    'cnt': 'sum'
}).reset_index()

monthly_report_2012 = df_2012.resample('M').agg({
    'instant': 'nunique',
    'cnt': 'sum'
}).reset_index()

# Format the index to month names
monthly_report_2011['dteday'] = monthly_report_2011['dteday'].dt.strftime('%B')
monthly_report_2012['dteday'] = monthly_report_2012['dteday'].dt.strftime('%B')

# Rename columns for clarity
monthly_report_2011.rename(columns={'instant': 'record', 'cnt': 'total_rentals'}, inplace=True)
monthly_report_2012.rename(columns={'instant': 'record', 'cnt': 'total_rentals'}, inplace=True)

# Section for monthly rentals report
st.title("Monthly Bike Rentals Report (2011 vs 2012)")

# Plotting the monthly rentals
plt.figure(figsize=(16, 8))
plt.plot(monthly_report_2011["dteday"], monthly_report_2011["total_rentals"], 
         marker='o', linewidth=2, color="#72BCD4", label="2011")
plt.plot(monthly_report_2012["dteday"], monthly_report_2012["total_rentals"], 
         marker='o', linewidth=2, color="#FF6F61", label="2012")

plt.title("Number of Orders per Month (2011 vs 2012)", loc="center", fontsize=20)
plt.xticks(rotation=45)
plt.yticks(fontsize=10)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Rentals", fontsize=12)
plt.grid(True)
plt.legend(title="Year", fontsize=12)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)

# Hourly rentals
hourly_rentals = hour_df.groupby('hr').agg({'cnt': 'sum'}).reset_index()

# Section for hourly rentals report
st.title('Hourly Bike Rentals Report')

# Plotting the hourly bike rentals
plt.figure(figsize=(10, 6))
plt.plot(hourly_rentals['hr'], hourly_rentals['cnt'], marker='o', color='#4C72B0', linewidth=2)
plt.title('Total Bike Rentals by Hour', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.grid(True)
plt.xticks(range(0, 24))

# Display the plot in Streamlit
st.pyplot(plt)
