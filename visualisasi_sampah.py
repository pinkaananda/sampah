import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tampilan Data Mentah", layout="wide")

st.title("📊 Tampilan Data Mentah untuk Prediksi Sampah")

# Fungsi load data
@st.cache_data
def load_data():
    data_sampah = pd.read_excel('data_sampah.xlsx')
    data_cuaca = pd.read_excel('data_cuaca.xlsx')
    data_sosial_ekonomi = pd.read_excel('data_sosial_ekonomi.xlsx')
    return data_sampah, data_cuaca, data_sosial_ekonomi

# Load data
data_sampah, data_cuaca, data_sosial_ekonomi = load_data()

# Sidebar untuk pilih dataset yang ingin ditampilkan
dataset = st.sidebar.selectbox("Pilih Dataset yang ingin ditampilkan:", 
                               ("Data Sampah", "Data Cuaca", "Data Sosial Ekonomi"))

if dataset == "Data Sampah":
    st.subheader("Data Sampah")
    st.write(f"Jumlah baris: {len(data_sampah)}")
    st.dataframe(data_sampah)

elif dataset == "Data Cuaca":
    st.subheader("Data Cuaca")
    st.write(f"Jumlah baris: {len(data_cuaca)}")
    st.dataframe(data_cuaca)

else:
    st.subheader("Data Sosial Ekonomi")
    st.write(f"Jumlah baris: {len(data_sosial_ekonomi)}")
    st.dataframe(data_sosial_ekonomi)

st.markdown("---")
st.write("📌 Gunakan sidebar untuk memilih data yang ingin kamu lihat.")

st.set_page_config(page_title="Visualisasi Volume Sampah", layout="wide")
st.title("📈 Visualisasi Volume Sampah per Tahun")

@st.cache_data
def load_data():
    data_sampah = pd.read_excel('data_sampah.xlsx')
    return data_sampah

data_sampah = load_data()

# Pastikan kolom TANGGAL dalam tipe datetime
data_sampah['TANGGAL'] = pd.to_datetime(data_sampah['TANGGAL'], errors='coerce')

# Buat kolom tahun
data_sampah['TAHUN'] = data_sampah['TANGGAL'].dt.year

# Cek apakah ada kolom volume sampah (contoh nama kolom: 'VOL. SELURUH M3')
if 'VOL. SELURUH M3' in data_sampah.columns:
    # Bisa langsung pakai ini
    data_sampah['VOLUME_TON'] = data_sampah['VOL. SELURUH M3'] * 0.25  # asumsi konversi 1 m3 = 0.25 ton
else:
    st.warning("Kolom volume sampah 'VOL. SELURUH M3' tidak ditemukan!")

# Agregasi volume sampah per tahun
vol_per_tahun = data_sampah.groupby('TAHUN')['VOLUME_TON'].sum().reset_index()

st.write("### Volume Sampah Total per Tahun (Ton)")
st.dataframe(vol_per_tahun)

# Visualisasi dengan matplotlib
fig, ax = plt.subplots()
ax.bar(vol_per_tahun['TAHUN'], vol_per_tahun['VOLUME_TON'], color='skyblue')
ax.set_xlabel('Tahun')
ax.set_ylabel('Volume Sampah (Ton)')
ax.set_title('Total Volume Sampah per Tahun')
ax.grid(axis='y')

st.pyplot(fig)
