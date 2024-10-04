import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load Data
day_df = pd.read_csv('day_data.csv')  # Sesuaikan dengan path dataset kamu

# Mapping untuk season dan weathersit
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weathersit_mapping = {
    1: 'Cuaca Cerah',
    2: 'Cuaca Berawan',
    3: 'Cuaca Hujan Ringan atau Bersalju',
    4: 'Cuaca Buruk'
}

day_df['season'] = day_df['season'].replace(season_mapping)
day_df['weathersit'] = day_df['weathersit'].replace(weathersit_mapping)

# Title and description
st.title('Dashboard Penyewaan Sepeda')
st.write('Dashboard ini menampilkan data penyewaan sepeda berdasarkan cuaca dan tren musiman untuk tahun 2011 dan 2012.')

# Filter by Year
year_filter = st.selectbox('Pilih Tahun:', ['2011', '2012'])
year_mapping = {'2011': 0, '2012': 1}
filtered_data = day_df[day_df['yr'] == year_mapping[year_filter]]

# Visualization 1: Pengaruh Cuaca Terhadap Penyewaan
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
day_type = filtered_data['workingday'].apply(lambda x: 'Weekday' if x == 1 else 'Weekend')
filtered_data['day_type'] = day_type

avg_rentals = filtered_data.groupby(['weathersit', 'day_type'])['cnt'].mean().reset_index()

# Plot 1
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=avg_rentals, x='weathersit', y='cnt', hue='day_type', palette='husl', ax=ax1)
ax1.set_title(f'Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda ({year_filter})', fontsize=14)
ax1.set_xlabel('Kondisi Cuaca', fontsize=12)
ax1.set_ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
plt.xticks(rotation=0)
st.pyplot(fig1)

# Visualization 2: Rata-rata Penyewaan Berdasarkan Musim
st.subheader('Rata-rata Penyewaan Berdasarkan Musim')

avg_seasonal_rentals = day_df.groupby(['season', 'yr'])['cnt'].mean().reset_index()
avg_seasonal_rentals['yr'] = avg_seasonal_rentals['yr'].replace({0: '2011', 1: '2012'})

# Plot 2
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=avg_seasonal_rentals, x='season', y='cnt', hue='yr', palette='husl', ax=ax2)
ax2.set_title('Rata-rata Penyewaan Sepeda per Musim (2011 dan 2012)', fontsize=14)
ax2.set_xlabel('Musim', fontsize=12)
ax2.set_ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
plt.xticks(rotation=0)
st.pyplot(fig2)

# Summary
st.subheader('Analisis dan Kesimpulan')
st.write("""
- **Grafik 1**: Dari hasil analisis, dapat disimpulkan bahwa cuaca memiliki pengaruh yang signifikan terhadap jumlah penyewaan sepeda, dengan cuaca cerah menjadi faktor pendukung utama untuk penyewaan yang tinggi, terutama di akhir pekan. Secara umum, lebih banyak sepeda disewa pada akhir pekan dibandingkan hari kerja, terutama saat cuaca cerah atau berawan. Pada kondisi cuaca buruk, jumlah penyewaan turun drastis baik di hari kerja maupun akhir pekan. Hal ini menunjukkan bahwa pengguna lebih memilih menyewa sepeda di cuaca yang lebih baik, terutama di akhir pekan ketika mereka memiliki lebih banyak waktu luang.
- **Grafik 2**: Dari hasil analisis, dapat disimpulkan bahwa tren musiman memang mempengaruhi jumlah penyewaan sepeda secara signifikan. Musim panas dan gugur menunjukkan jumlah penyewaan yang jauh lebih tinggi dibandingkan musim semi dan musim dingin. Selain itu, terdapat peningkatan umum dalam penyewaan sepeda pada tahun 2012 dibandingkan dengan tahun 2011, terutama pada musim panas dan gugur, yang menunjukkan bahwa penyewaan sepeda lebih populer pada periode tersebut.
""")