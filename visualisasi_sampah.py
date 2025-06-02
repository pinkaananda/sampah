import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi awal Streamlit (HARUS di awal)
st.set_page_config(page_title="Visualisasi Data Sampah & Eksternal", layout="wide")

# Judul Halaman
st.title("📊 Visualisasi Data Sampah, Cuaca, dan Sosial Ekonomi")

# Load data
data_sampah = pd.read_excel("data_sampah.xlsx", header=1)
data_cuaca = pd.read_excel("data_cuaca.xlsx")
data_sosial_ekonomi = pd.read_excel("data_sosial_ekonomi.xlsx")

# Pastikan kolom tanggal benar
data_sampah['TANGGAL'] = pd.to_datetime(data_sampah['TANGGAL'])
data_cuaca['Tanggal'] = pd.to_datetime(data_cuaca['Tanggal'])

# Extract tahun jika belum ada
if 'TAHUN' not in data_sampah.columns:
    data_sampah['TAHUN'] = data_sampah['TANGGAL'].dt.year
if 'tahun' not in data_cuaca.columns:
    data_cuaca['Tahun'] = data_cuaca['Tanggal'].dt.year

# Tabs untuk memisahkan data
tab1, tab2, tab3 = st.tabs(["📦 Data Sampah", "🌦️ Data Cuaca", "📈 Data Sosial Ekonomi"])

# Tab 1: Data Sampah
with tab1:
    st.subheader("Data Sampah Harian")
    st.dataframe(data_sampah, use_container_width=True)

    # Filter berdasarkan tahun
    tahun_opsi = sorted(data_sampah['TAHUN'].unique())
    tahun_pilih = st.selectbox("Pilih Tahun", tahun_opsi, key="tahun_sampah")

    # Filter dan plot
    data_sampah_tahun = data_sampah[data_sampah['TAHUN'] == tahun_pilih]
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(data_sampah_tahun['TANGGAL'], data_sampah_tahun['VOL. SELURUH M3'], color='green')
    ax1.set_ylabel("Volume Sampah (m3)")
    ax1.set_xlabel("Tanggal")
    ax1.set_title(f"Volume Sampah Harian Tahun {tahun_pilih}")
    ax1.grid(True)
    st.pyplot(fig1)

# Tab 2: Data Cuaca
with tab2:
    st.subheader("Data Cuaca Harian")
    st.dataframe(data_cuaca, use_container_width=True)

    # Pilih tahun
    tahun_opsi_cuaca = sorted(data_cuaca['Tahun'].unique())
    tahun_pilih_cuaca = st.selectbox("Pilih Tahun", tahun_opsi_cuaca, key="tahun_cuaca")

    # Filter dan pilih kolom
    data_cuaca_tahun = data_cuaca[data_cuaca['Tahun'] == tahun_pilih_cuaca]
    kolom_numerik = data_cuaca_tahun.select_dtypes(include='number').columns.tolist()
    kolom_pilih = st.selectbox("Pilih Variabel Cuaca", kolom_numerik, key="kolom_cuaca")

    # Plot
    fig2, ax2 = plt.subplots(figsize=(12, 4))
    ax2.plot(data_cuaca_tahun['Tanggal'], data_cuaca_tahun[kolom_pilih], color='orange')
    ax2.set_ylabel(kolom_pilih.replace('_', ' ').title())
    ax2.set_xlabel("Tanggal")
    ax2.set_title(f"{kolom_pilih.replace('_', ' ').title()} Harian Tahun {tahun_pilih_cuaca}")
    ax2.grid(True)
    st.pyplot(fig2)

# Tab 3: Data Sosial Ekonomi
with tab3:
    st.subheader("Data Sosial Ekonomi Tahunan")
    st.dataframe(data_sosial_ekonomi, use_container_width=True)

    # Grafik gabungan
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(data_sosial_ekonomi['Tahun'], data_sosial_ekonomi['Jumlah Penduduk'],
             label='Jumlah Penduduk', marker='o', color='blue')
    ax3.set_ylabel("Jumlah Penduduk", color='blue')
    ax3.set_xlabel("Tahun")
    ax3.tick_params(axis='y', labelcolor='blue')
    ax3.set_title("Tren Jumlah Penduduk dan PDRB Per Kapita")

    # Twin axis untuk PDRB per kapita
    ax4 = ax3.twinx()
    ax4.plot(data_sosial_ekonomi['Tahun'], data_sosial_ekonomi['PDRB Per Kapita (Rp)'],
             label='PDRB Per Kapita (Rp)' color='red', marker='s')
    ax4.set_ylabel("PDRB Per Kapita (Rp)", color='red')
    ax4.tick_params(axis='y', labelcolor='red')

    st.pyplot(fig3)
