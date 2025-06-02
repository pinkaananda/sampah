import streamlit as st
import pandas as pd

# ===== Judul Aplikasi =====
st.set_page_config(page_title="Visualisasi Data Sampah & Eksternal", layout="wide")
st.title("📊 Data Mentah: Sampah, Cuaca, dan Sosial Ekonomi")

# ===== Load Data =====
@st.cache_data
def load_data():
    df_sampah = pd.read_excel("data_sampah.xlsx",  header=1)
    df_cuaca = pd.read_excel("data_cuaca.xlsx")
    df_ekosos = pd.read_excel("data_sosial_ekonomi.xlsx")
    return df_sampah, df_cuaca, df_ekosos

df_sampah, df_cuaca, df_ekosos = load_data()

# ======= Data SAMPAH =======
st.header("🗑 Data Sampah")
df_sampah['TANGGAL'] = pd.to_datetime(df_sampah['TANGGAL'])
st.write("Data sampah dari tahun", df_sampah['TANGGAL'].dt.year.min(), "hingga", df_sampah['TANGGAL'].dt.year.max())
st.dataframe(df_sampah, use_container_width=True)

# ======= Data CUACA =======
st.header("🌦 Data Cuaca")
if 'Tanggal' in df_cuaca.columns:
    df_cuaca['Tanggal'] = pd.to_datetime(df_cuaca['Tanggal'])
    st.write("Data cuaca dari tahun", df_cuaca['Tanggal'].dt.year.min(), "hingga", df_cuaca['Tanggal'].dt.year.max())
else:
    st.warning("Kolom 'Tanggal' tidak ditemukan di data cuaca.")
st.dataframe(df_cuaca, use_container_width=True)

# ======= Data EKONOMI & SOSIAL =======
st.header("👨‍👩‍👧‍👦📈 Data Sosial Ekonomi")
df_ekosos['Tahun'] = pd.to_datetime(df_ekosos['Tahun'])
st.write("Data dari tahun", df_ekosos['Tahun'].min(), "hingga", df_ekosos['Tahun'].max())
st.dataframe(df_ekosos, use_container_width=True)

# ========== Footer ==========
st.markdown("---")
st.caption("Data ditampilkan apa adanya sebelum dilakukan preprocessing.")
