import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Visualisasi Data Sampah", layout="wide")

st.title("📊 Visualisasi Data Sampah, Cuaca, dan Sosial Ekonomi")

# Load data
@st.cache_data
def load_data():
    data_sampah = pd.read_excel("data_sampah.xlsx", header=1)
    data_cuaca = pd.read_excel("data_cuaca.xlsx")
    data_ekonomi = pd.read_excel("data_sosial_ekonomi.xlsx")
    return data_sampah, data_cuaca, data_ekonomi

data_sampah, data_cuaca, data_ekonomi = load_data()

# Preprocessing waktu
data_sampah['TANGGAL'] = pd.to_datetime(data_sampah['TANGGAL'])
data_sampah['TAHUN'] = data_sampah['TANGGAL'].dt.year

if 'tanggal' in data_cuaca.columns:
    data_cuaca['tanggal'] = pd.to_datetime(data_cuaca['tanggal'])
    data_cuaca['tahun'] = data_cuaca['tanggal'].dt.year

# Tabs untuk masing-masing data
tab1, tab2, tab3 = st.tabs(["🗑️ Data Sampah", "🌧️ Data Cuaca", "👥📈 Data Sosial Ekonomi"])

with tab1:
    st.subheader("Data Sampah Harian")
    st.dataframe(data_sampah, use_container_width=True)

    tahun_opsi = sorted(data_sampah['TAHUN'].unique())
    tahun_pilih = st.selectbox("Pilih Tahun untuk Visualisasi", tahun_opsi)

    data_tahun = data_sampah[data_sampah['TAHUN'] == tahun_pilih]

    st.markdown(f"### Grafik Volume Sampah Tahun {tahun_pilih}")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(data_tahun['TANGGAL'], data_tahun['VOL. SELURUH M3'], color='green')
    ax.set_ylabel("Volume (m³)")
    ax.set_xlabel("Tanggal")
    ax.set_title(f"Volume Sampah Harian - {tahun_pilih}")
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.subheader("Data Cuaca Harian")
    st.dataframe(data_cuaca, use_container_width=True)

    if 'tahun' in data_cuaca.columns:
        tahun_opsi_cuaca = sorted(data_cuaca['tahun'].unique())
        tahun_pilih_cuaca = st.selectbox("Pilih Tahun untuk Visualisasi Cuaca", tahun_opsi_cuaca)

        data_cuaca_tahun = data_cuaca[data_cuaca['tahun'] == tahun_pilih_cuaca]

        # Contoh grafik cuaca jika kolom curah hujan ada
        if 'curah_hujan' in data_cuaca_tahun.columns:
            st.markdown(f"### Grafik Curah Hujan Tahun {tahun_pilih_cuaca}")
            fig2, ax2 = plt.subplots(figsize=(12, 4))
            ax2.plot(data_cuaca_tahun['tanggal'], data_cuaca_tahun['curah_hujan'], color='blue')
            ax2.set_ylabel("Curah Hujan")
            ax2.set_xlabel("Tanggal")
            ax2.set_title(f"Curah Hujan Harian - {tahun_pilih_cuaca}")
            ax2.grid(True)
            st.pyplot(fig2)

with tab3:
    st.subheader("Data Sosial Ekonomi Tahunan")
    st.dataframe(data_ekonomi, use_container_width=True)

    tahun_pilih_ekonomi = st.selectbox("Pilih Tahun untuk Sorotan Ekonomi", sorted(data_ekonomi['tahun'].unique()))

    data_terpilih = data_ekonomi[data_ekonomi['tahun'] == tahun_pilih_ekonomi].iloc[0]
    st.markdown(f"### Ringkasan Tahun {tahun_pilih_ekonomi}")
    st.metric("Jumlah Penduduk", f"{data_terpilih['jumlah_penduduk']:,}")
    st.metric("PDRB per Kapita", f"Rp {data_terpilih['PDRB_per_kapita']:,}")
