import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset day.csv dan hour.csv
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Helper function untuk menyiapkan berbagai dataframe

def create_daily_rentals_df(df):
    daily_rentals_df = df[['dteday', 'cnt']].groupby('dteday').sum().reset_index()
    return daily_rentals_df

def create_temp_rentals_df(df):
    temp_rentals_df = df.groupby("temp").cnt.sum().reset_index()
    return temp_rentals_df

def create_weather_rentals_df(df):
    weather_rentals_df = df.groupby("weathersit").cnt.sum().reset_index()
    return weather_rentals_df

def create_byusertype_df(df):
    byusertype_df = df.groupby(by="yr").agg({
        "casual": "sum",
        "registered": "sum"
    }).reset_index()
    
    return byusertype_df

# Convert 'dteday' to datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.sort_values(by='dteday', inplace=True)

# Sidebar untuk filter rentang waktu
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("https://th.bing.com/th/id/OIP.dzY5iX1-aq4Y1383yHoGrQAAAA?rs=1&pid=ImgDetMain")
    
    # Pilih rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & 
                 (day_df["dteday"] <= pd.to_datetime(end_date))]

# Menyiapkan berbagai dataframe
daily_rentals_df = create_daily_rentals_df(main_df)
temp_rentals_df = create_temp_rentals_df(main_df)
weather_rentals_df = create_weather_rentals_df(main_df)
byusertype_df = create_byusertype_df(main_df)

# Dashboard Header
st.header('Bike Sharing Dashboard')
st.subheader('Daily Rentals')

# Menampilkan metrik total dan rata-rata rentals
col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df.cnt.sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    avg_rentals = round(daily_rentals_df.cnt.mean(), 2)
    st.metric("Average Rentals per Day", value=avg_rentals)

# Plot total daily rentals
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Total Daily Rentals", fontsize=25)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Plot rentals by temperature
st.subheader("Rentals by Temperature")

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="temp", y="cnt", data=temp_rentals_df, ax=ax, color="#90CAF9")
ax.set_title("Total Rentals by Temperature", fontsize=25)
st.pyplot(fig)

# Plot rentals by weather condition
st.subheader("Rentals by Weather Condition")

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x="weathersit", y="cnt", data=weather_rentals_df, hue="weathersit",palette="Blues", ax=ax, legend=False)
ax.set_title("Total Rentals by Weather Condition", fontsize=25)
st.pyplot(fig)

# Usertype analysis
st.subheader("Rentals by User Type")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x="yr", y="casual", data=byusertype_df, hue="casual", palette="Blues", ax=ax, legend=False)
    ax.set_title("Rentals by Casual Users", fontsize=25)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x="yr", y="registered", data=byusertype_df, hue="registered", palette="Greens", ax=ax, legend=False)
    ax.set_title("Rentals by Registered Users", fontsize=25)
    st.pyplot(fig)

# Load dataset hour.csv for hourly analysis
st.subheader("Hourly Rentals")

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df.sort_values(by=['dteday', 'hr'], inplace=True)

hourly_rentals_df = hour_df.groupby(['dteday', 'hr']).cnt.sum().reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="hr", y="cnt", data=hourly_rentals_df, ax=ax, marker="o", color="#90CAF9")
ax.set_title("Hourly Rentals", fontsize=25)
ax.set_xlabel("Hour of Day", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
st.pyplot(fig)