import streamlit as st
import pandas as pd

# Judul aplikasi
st.set_page_config(page_title="Visualisasi Data Sampah", layout="wide")
st.title("Visualisasi Data Mentah Sampah, Cuaca, dan Sosial Ekonomi")

# Fungsi untuk load dan tampilkan data
@st.cache_data
def load_data():
    data_sampah = pd.read_excel('data_sampah.xlsx', header=1)
    data_cuaca = pd.read_excel('data_cuaca.xlsx')
    data_ekonomi = pd.read_excel('data_sosial_ekonomi.xlsx')
    return data_sampah, data_cuaca, data_ekonomi

data_sampah, data_cuaca, data_ekonomi = load_data()

# Tampilkan data sampah
st.header("Data Sampah")
st.write("Tampilan 10 baris pertama data sampah")
st.dataframe(data_sampah.head(10))

# Tampilkan data cuaca
st.header("Data Cuaca")
st.write("Tampilan 10 baris pertama data cuaca")
st.dataframe(data_cuaca.head(10))

# Tampilkan data sosial ekonomi
st.header("Data Sosial Ekonomi")
st.write("Tampilan 10 baris pertama data sosial ekonomi")
st.dataframe(data_ekonomi.head(10))

# Tambah fitur filter tahun pada data sampah jika kolom TANGGAL ada
if 'TANGGAL' in data_sampah.columns:
    data_sampah['TANGGAL'] = pd.to_datetime(data_sampah['TANGGAL'])
    data_sampah['TAHUN'] = data_sampah['TANGGAL'].dt.year

    tahun_list = sorted(data_sampah['TAHUN'].unique())
    selected_year = st.sidebar.selectbox("Pilih Tahun untuk Data Sampah", tahun_list)

    st.subheader(f"Data Sampah Tahun {selected_year}")
    st.dataframe(data_sampah[data_sampah['TAHUN'] == selected_year])

# Filter tahun untuk data cuaca jika kolom tanggal ada
if 'Tanggal' in data_cuaca.columns:
    data_cuaca['Tanggal'] = pd.to_datetime(data_cuaca['Tanggal'])
    data_cuaca['Tahun'] = data_cuaca['tanggal'].dt.year

    tahun_list_cuaca = sorted(data_cuaca['Tahun'].unique())
    selected_year_cuaca = st.sidebar.selectbox("Pilih Tahun untuk Data Cuaca", tahun_list_cuaca)

    st.subheader(f"Data Cuaca Tahun {selected_year_cuaca}")
    st.dataframe(data_cuaca[data_cuaca['Tahun'] == selected_year_cuaca])

# Filter tahun untuk data sosial ekonomi jika kolom tahun ada
if 'Tahun' in data_ekonomi.columns:
    tahun_list_ekonomi = sorted(data_ekonomi['Tahun'].unique())
    selected_year_ekonomi = st.sidebar.selectbox("Pilih Tahun untuk Data Sosial Ekonomi", tahun_list_ekonomi)

    st.subheader(f"Data Sosial Ekonomi Tahun {selected_year_ekonomi}")
    st.dataframe(data_ekonomi[data_ekonomi['Tahun'] == selected_year_ekonomi])
