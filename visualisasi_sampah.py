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
