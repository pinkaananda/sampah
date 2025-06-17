import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURASI AWAL ---
st.set_page_config(page_title="Dashboard Prediksi Sampah", layout="wide")

# --- GAYA VISUAL ---
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .block-container {padding: 2rem 2rem;}
    h1, h2, h3, h4 {color: #004d4d;}
    </style>
""", unsafe_allow_html=True)

# --- JUDUL UTAMA ---
st.title("📊 Dashboard Prediksi Jumlah Sampah TPA Bumi Ayu")

# --- SIDEBAR ---
st.sidebar.header("🔍 Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Data Sampah", "Data Cuaca", "Data Sosial Ekonomi", "Hasil Prediksi"])

# --- LOAD DATA ---
data_sampah = pd.read_excel("data_sampah.xlsx")
data_cuaca = pd.read_excel("data_cuaca.xlsx")
data_sosial_ekonomi = pd.read_excel("data_sosial_ekonomi.xlsx")
data_prediksi = pd.read_excel("prediksi_sampah_2025_2030.xlsx")

# Format tanggal
data_sampah['Tanggal'] = pd.to_datetime(data_sampah['Tanggal'])
data_cuaca['Tanggal'] = pd.to_datetime(data_cuaca['Tanggal'])
data_prediksi['Tanggal'] = pd.to_datetime(data_prediksi['Tanggal'])
data_prediksi['Tahun'] = data_prediksi['Tanggal'].dt.year
data_prediksi['Bulan'] = data_prediksi['Tanggal'].dt.month

# --- TAHUN EKSTRAKSI ---
data_sampah['TAHUN'] = data_sampah['Tanggal'].dt.year
data_cuaca['Tahun'] = data_cuaca['Tanggal'].dt.year

# --- HALAMAN DATA SAMPAH ---
if menu == "Data Sampah":
    st.subheader("📦 Data Sampah Harian")
    st.dataframe(data_sampah, use_container_width=True)

    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_sampah['TAHUN'].unique()))
    data_tahun = data_sampah[data_sampah['TAHUN'] == tahun_pilih]

    st.markdown("### 📈 Volume Sampah Harian")
    fig = px.line(data_tahun, x='Tanggal', y='Total Volume Sampah (m³)', markers=True,
                  title=f"Volume Sampah Tahun {tahun_pilih}", template='plotly_white', color_discrete_sequence=['green'])
    st.plotly_chart(fig, use_container_width=True)

    # Kartu statistik
    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata", f"{data_tahun['Total Volume Sampah (m³)'].mean():.2f} m³")
    col2.metric("Tertinggi", f"{data_tahun['Total Volume Sampah (m³)'].max():.2f} m³")
    col3.metric("Terendah", f"{data_tahun['Total Volume Sampah (m³)'].min():.2f} m³")

# --- HALAMAN CUACA ---
elif menu == "Data Cuaca":
    st.subheader("🌦️ Data Cuaca Harian")
    st.dataframe(data_cuaca, use_container_width=True)

    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_cuaca['Tahun'].unique()))
    data_tahun = data_cuaca[data_cuaca['Tahun'] == tahun_pilih]
    kolom_numerik = data_tahun.select_dtypes(include='number').columns.tolist()
    fitur_pilih = st.selectbox("Pilih Variabel Cuaca", kolom_numerik)

    fig = px.line(data_tahun, x='Tanggal', y=fitur_pilih, markers=True,
                  title=f"{fitur_pilih} Tahun {tahun_pilih}", template='plotly_white', color_discrete_sequence=['orange'])
    st.plotly_chart(fig, use_container_width=True)

# --- HALAMAN SOSIAL EKONOMI ---
elif menu == "Data Sosial Ekonomi":
    st.subheader("📈 Data Sosial Ekonomi Tahunan")
    st.dataframe(data_sosial_ekonomi, use_container_width=True)

    fig = px.line(data_sosial_ekonomi, x='Tahun', y=['Jumlah Penduduk', 'PDRB Per Kapita (Rp)'],
                  markers=True, title="Tren Jumlah Penduduk dan PDRB", template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# --- HALAMAN PREDIKSI ---
elif menu == "Hasil Prediksi":
    st.subheader("🔮 Prediksi Sampah Harian 2025–2030")
    st.dataframe(data_prediksi, use_container_width=True)

    fig_all = px.line(data_prediksi, x='Tanggal', y='Total Volume Sampah (m³)',
                      title="Prediksi Harian 2025–2030", template='plotly_white', color_discrete_sequence=['teal'])
    st.plotly_chart(fig_all, use_container_width=True)

    # Rata-rata bulanan
    st.markdown("### 📊 Rata-Rata Bulanan")
    rata_bulanan = data_prediksi.groupby(['Tahun', 'Bulan'])['Total Volume Sampah (m³)'].mean().reset_index()
    st.dataframe(rata_bulanan.pivot(index='Bulan', columns='Tahun', values='Total Volume Sampah (m³)'), use_container_width=True)

    # Visualisasi bulanan
    st.markdown("### 📆 Visualisasi Bulanan")
    tahun = st.selectbox("Pilih Tahun", sorted(data_prediksi['Tahun'].unique()))
    bulan = st.selectbox("Pilih Bulan", list(range(1,13)))
    data_bulanan = data_prediksi[(data_prediksi['Tahun'] == tahun) & (data_prediksi['Bulan'] == bulan)]

    fig_bulan = px.line(data_bulanan, x='Tanggal', y='Total Volume Sampah (m³)', markers=True,
                        title=f"Prediksi Sampah Bulan {bulan} Tahun {tahun}", template='plotly_white', color_discrete_sequence=['purple'])
    st.plotly_chart(fig_bulan, use_container_width=True)

    # Statistik tahunan
    st.markdown("### 📘 Rata-Rata Tahunan")
    rata_tahunan = data_prediksi.groupby('Tahun')['Total Volume Sampah (m³)'].mean().reset_index()
    st.dataframe(rata_tahunan, use_container_width=True)

    # Visualisasi tahunan
    fig_year = px.line(rata_tahunan, x='Tahun', y='Total Volume Sampah (m³)', markers=True,
                       title="Prediksi Rata-Rata Sampah per Tahun", template='plotly_white', color_discrete_sequence=['navy'])
    st.plotly_chart(fig_year, use_container_width=True)
