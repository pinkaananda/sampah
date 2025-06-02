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
data_prediksi = pd.read_csv("prediksi_sampah_2025_2030.csv")

# Pastikan kolom tanggal benar
data_sampah['TANGGAL'] = pd.to_datetime(data_sampah['TANGGAL'])
data_cuaca['Tanggal'] = pd.to_datetime(data_cuaca['Tanggal'])
data_prediksi['Tanggal'] = pd.to_datetime(data_prediksi['Tanggal'])
data_prediksi['Tahun'] = data_prediksi['Tanggal'].dt.year
data_prediksi['Bulan'] = data_prediksi['Tanggal'].dt.month

# Extract tahun jika belum ada
if 'TAHUN' not in data_sampah.columns:
    data_sampah['TAHUN'] = data_sampah['TANGGAL'].dt.year
if 'tahun' not in data_cuaca.columns:
    data_cuaca['Tahun'] = data_cuaca['Tanggal'].dt.year

# Tabs untuk memisahkan data
tab1, tab2, tab3, tab4 = st.tabs(["📦 Data Sampah", "🌦️ Data Cuaca", "📈 Data Sosial Ekonomi", "🔮 Hasil Prediksi"])

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
    st.write("Kolom dalam data sosial ekonomi:", data_sosial_ekonomi.columns.tolist())

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
             label='PDRB Per Kapita (Rp)', color='red', marker='s')
    ax4.set_ylabel("PDRB Per Kapita (Rp)", color='red')
    ax4.tick_params(axis='y', labelcolor='red')

    st.pyplot(fig3)
    
# Tab 4: Hasil Prediksi
with tab4:
    st.subheader("Prediksi Jumlah Sampah Harian (Ton) untuk 2025–2030")
    st.dataframe(data_prediksi, use_container_width=True)

    # Filter tahun dan bulan
    tahun_opsi_pred = sorted(data_prediksi['Tahun'].unique())
    tahun_pilih_pred = st.selectbox("Pilih Tahun", tahun_opsi_pred, key="tahun_prediksi")

    bulan_opsi_pred = list(range(1, 13))
    bulan_nama = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    bulan_dict = dict(zip(bulan_opsi_pred, bulan_nama))
    bulan_pilih_pred = st.selectbox("Pilih Bulan", bulan_opsi_pred, format_func=lambda x: bulan_dict[x], key="bulan_prediksi")

    # Filter data sesuai pilihan
    data_filtered = data_prediksi[
        (data_prediksi['Tahun'] == tahun_pilih_pred) & 
        (data_prediksi['Bulan'] == bulan_pilih_pred)
    ]

    # Plot data harian
    fig4, ax4 = plt.subplots(figsize=(12, 4))
    ax4.plot(data_filtered['Tanggal'], data_filtered['Jumlah Sampah (Ton)'],
             marker='o', linestyle='-', color='purple')
    ax4.set_title(f"Prediksi Jumlah Sampah Harian - {bulan_dict[bulan_pilih_pred]} {tahun_pilih_pred}")
    ax4.set_xlabel("Tanggal")
    ax4.set_ylabel("Sampah (Ton)")
    ax4.grid(True)
    st.pyplot(fig4)

    # Rata-rata bulanan dan tahunan
    st.markdown("### 📊 Statistik Rata-Rata")

    rata_bulanan = data_prediksi.groupby(['Tahun', 'Bulan'])['Jumlah Sampah (Ton)'].mean().reset_index()
    rata_tahunan = data_prediksi.groupby('Tahun')['Jumlah Sampah (Ton)'].mean().reset_index()

    st.write("📅 Rata-Rata per Bulan")
    bulan_nama = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 
              'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    bulan_dict = dict(zip(range(1, 13), bulan_nama))
    
    rata_bulanan['Bulan'] = rata_bulanan['Bulan'].map(bulan_dict)
    rata_bulanan['Bulan'] = pd.Categorical(
        rata_bulanan['Bulan'],
        categories=bulan_nama,
        ordered=True
    )
    # Tampilkan data pivot dengan bulan berurutan
    rata_bulanan_pivot = rata_bulanan.pivot(index='Bulan', columns='Tahun', values='Jumlah Sampah (Ton)')
    st.dataframe(rata_bulanan_pivot, use_container_width=True)

    st.write("📅 Rata-Rata per Tahun")
    st.dataframe(rata_tahunan, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Visualisasi Prediksi Sampah Seluruh Periode (2025-2030)")
    fig_all, ax_all = plt.subplots(figsize=(14, 5))
    ax_all.plot(data_prediksi['Tanggal'], data_prediksi['Jumlah Sampah (Ton)'], color='teal')
    ax_all.set_title("Prediksi Jumlah Sampah Harian 2025-2030")
    ax_all.set_xlabel("Tanggal")
    ax_all.set_ylabel("Jumlah Sampah (Ton)")
    ax_all.grid(True)
    st.pyplot(fig_all)
    
    # Visualisasi rata-rata prediksi per tahun dengan filter
    st.markdown("---")
    st.subheader("Visualisasi Rata-Rata Prediksi per Tahun")
    
    # Pilih tahun untuk visualisasi rata-rata
    tahun_opsi_rata = sorted(data_prediksi['Tahun'].unique())
    tahun_pilih_rata = st.selectbox("Pilih Tahun untuk Visualisasi Rata-Rata Harian", tahun_opsi_rata, key="tahun_rata_prediksi")
    
    data_rata_tahun = data_prediksi[data_prediksi['Tahun'] == tahun_pilih_rata]
    rata_harian = data_rata_tahun.groupby('Tanggal')['Jumlah Sampah (Ton)'].mean()
    
    fig_year, ax_year = plt.subplots(figsize=(12, 4))
    ax_year.plot(rata_harian.index, rata_harian.values, marker='o', color='navy')
    ax_year.set_title(f"Rata-Rata Prediksi Jumlah Sampah Harian Tahun {tahun_pilih_rata}")
    ax_year.set_xlabel("Tanggal")
    ax_year.set_ylabel("Jumlah Sampah (Ton)")
    ax_year.grid(True)
    st.pyplot(fig_year)
    
        
