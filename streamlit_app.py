import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Rental Sepeda : dashboard ',
    page_icon=':bike:', # This is an emoji shortcode. Could be a URL too.r
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

#@st.cache_data
def load_data():
    df = pd.read_csv('data/hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['mnth'] = df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    df['season'] = df['season'].map({
        1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
    df['weekday'] = df['weekday'].map({
        0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
    })
    df['weathersit'] = df['weathersit'].map({
        1: 'Clear/Partly Cloudy',
        2: 'Misty/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Severe Weather'
    })

    df['yr'] = df['yr'].map({
        0: '2011', 1: '2012'
    })

    df['workingday'] = df['workingday'].map({
        0: 'Holiday', 1: 'Workingday'
    })
    return df

df = load_data()




# Title of the dashboard

st.markdown("<h1 style='text-align: center;'>Dashboard Analisis <br> Rental Sepeda</h1>", unsafe_allow_html=True)
'''
Sistem berbagi sepeda merupakan generasi baru dari penyewaan sepeda tradisional di mana seluruh proses mulai dari keanggotaan, penyewaan, dan pengembalian telah menjadi otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari lokasi tertentu dan kembali lagi di lokasi lain. Saat ini, terdapat sekitar lebih dari 500 program berbagi sepeda di seluruh dunia yang terdiri dari lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena perannya yang penting dalam masalah lalu lintas, lingkungan, dan kesehatan. .
'''

# Create Tabs
tab1, tab2 ,tab3 = st.tabs(["📈 Tren Rental Sepeda", "🌦️ Pengaruh Cuaca terhadap penyewaan","⏰ Rental Sepeda berdasarkan waktu rental"])

# Visualisasi Tren  
with tab1:
    st.subheader('Tren Rental Sepeda per tahun')
    
    # Membuat figure dengan ukuran yang lebih besar
    plt.figure(figsize=(26, 7))
    
    # Menggunakan seaborn untuk plot dengan palet warna yang lebih menarik
    sns.set(style="whitegrid")  # Tema whitegrid agar tampilan lebih bersih
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=df, marker="o", 
                 palette="coolwarm",  # Menggunakan palet warna yang lebih menarik
                 linewidth=2.5)  # Membuat garis lebih tebal

    # Menambahkan judul dan label sumbu yang lebih estetis
    plt.title('Trend Rental Sepeda Per Tahun', 
              fontsize=16, fontweight='bold',)
    plt.xlabel('Bulan', fontsize=12, fontweight='bold')
    plt.ylabel('Jumlah Rental', fontsize=12, fontweight='bold')

    # Menambahkan format khusus pada ticks untuk membuat sumbu X lebih rapi
    # plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    #                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    #            fontsize=10)
    # plt.yticks(fontsize=10)

    # Menyesuaikan legenda agar lebih jelas dan tidak bertumpuk
    plt.legend(title='Tahun', title_fontsize='13', fontsize='11', loc='upper right', frameon=True)

    # Menampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader('Ringkasan Penyewaan Sepeda')

    # Buat kolom untuk metrik dan grafik batang
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center;'> Perbandingan Penyewa Sepeda <br>Hari Kerja Dan Hari Libur</p>", unsafe_allow_html=True)
        plt.figure(figsize=(10,6))
        sns.barplot(
            x='workingday',
            y='cnt',
            data=df,
            palette='coolwarm')

        plt.title('Perbandingan Penyewa Sepeda Hari Kerja Dan Hari Libur')
        plt.xlabel(None)
        plt.ylabel('Jumlah Rental Sepeda')
        st.pyplot(plt)

    with col2:
        # Hitung total penyewaan untuk seluruh data (tanpa filter musim)
        total_penyewaan = df['cnt'].sum()
        st.metric(label="Total Penyewaan Sepeda", value=total_penyewaan)

        # Total penyewaan oleh member terdaftar untuk seluruh data
        total_registered = df['registered'].sum()
        st.metric(label="Total Penyewaan oleh Member Terdaftar", value=total_registered)

        # Total penyewaan oleh non-member (casual) untuk seluruh data
        total_casual = df['casual'].sum()
        st.metric(label="Total Penyewaan oleh Non-Member", value=total_casual)

        # Rata-rata penyewaan untuk seluruh data
        avg_penyewaan = df['cnt'].mean()
        st.metric(label="Rata-rata Penyewaan Sepeda", value=round(avg_penyewaan, 2))

    


with tab2:
    st.subheader("Pengaruh Cuaca terhadap Rental Sepeda")

    st.write("**Rata-rata Penyewaan Berdasarkan Kondisi Cuaca**")
    
    # Membuat figur baru untuk line chart
    plt.figure(figsize=(28, 6)) 
    avg_rentals_per_weather = df.groupby('weathersit')['cnt'].mean()
    print(avg_rentals_per_weather)
    sns.barplot(x=avg_rentals_per_weather.index, y=avg_rentals_per_weather.values, palette='viridis')
    plt.title('Pengaruh Kondisi Cuaca terhadap rata-rata Penyewaan sepeda')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan')
    # plt.xticks(rotation=45)
    st.pyplot(plt)  # Menampilkan plot

    # Kolom untuk metrik dan bar chart yang sederhana
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div style="text-align: justify;">Korelasi kondisi cuaca (seperti temperatur, kelembapan, dan kecepatan angin), casual dan registered terhadap jumlah Rental Sepeda</div>', unsafe_allow_html=True)
        plt.figure(figsize=(20, 6))
        corrMatt = df[["temp","atemp",
        "hum","windspeed",
        "casual","registered",
        "cnt"]].corr()
        mask = np.array(corrMatt)
        mask[np.tril_indices_from(mask)] = False

        sns.heatmap(corrMatt, annot=True, cmap='coolwarm', vmin=-1, vmax=1,square=True, mask=mask)
        
        st.pyplot(plt)
    with col2:
        
        total_clear = df[df['weathersit'] == 'Clear/Partly Cloudy']['cnt'].sum()
        st.metric(label="Total Penyewaan Cuaca Cerah", value=total_clear)

        total_mist = df[df['weathersit'] == 'Misty/Cloudy']['cnt'].sum()
        st.metric(label="Total Penyewaan Cuaca Berkabut", value=total_mist)

        total_rain_snow = df[df['weathersit'] == 'Misty/Cloudy']['cnt'].sum()
        st.metric(label="Total Penyewaan Hujan/Salju", value=total_rain_snow)

        total_rain_snow = df[df['weathersit'] == 'Misty/Cloudy']['cnt'].sum()
        st.metric(label="Total Penyewaan Cuaca Ekstream", value=total_rain_snow)

    # Tambahkan interpretasi
    st.write("""
    **Kesimpulan:**
    - Cuaca cerah (Clear/Partly Cloudy) berdampak positif terhadap jumlah penyewaan sepeda
    - Cuaca Ekstrim (Severe Weather) cukup berdampak buruk / negatif terhadap jumlah penyewaan sepdah
    - terdapat 2 variabel yang memiliki tingkat korelasi tinggi dengan jumlah rental sepeda yaitu variabel casual dan registered
    """)
    
with tab3:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='hr', y='cnt', hue='workingday', palette='coolwarm')
    plt.title('Rental Sepedah berdasarkan waktu dan status hari')
    plt.xlabel('Jam')
    plt.ylabel('Total rental sepedah')
    plt.legend(title='Day Status')
    st.pyplot(plt)
    st.write("""
    Terdapat pola peminjamaan yang meningkat:
    - Pada hari kerja, yaitu di jam-jam berangkat kerja (antara pukul 05.00 - 10.00 ) dan jam pulang kerja (antara pukul 15.00 - 20.00)
    - Pada hari libur, yaitu pada sore sampai malam hari sekitar pukul 15.00 sampai dengan 20.00
    """)
