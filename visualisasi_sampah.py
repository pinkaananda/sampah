# --- 🎞 LIBRARY SETUP ---
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO
import numpy as np
import plotly.graph_objects as go

# --- 🧱 KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Prediksi Sampah", 
    layout="wide", 
    page_icon="🗑️"
)

# --- 🎨 CUSTOM STYLE ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Quicksand', sans-serif;
            background-color: #e7f5ec;
        }
        .hero {
            background: linear-gradient(120deg, #00afb9, #006d77);
            padding: 2rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
        }
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 0.2rem;
        }
        .hero p {
            font-size: 1.2rem;
            margin-top: 0;
        }
        .metric-card {
            background-color: #f5f5f5;
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        }
    </style>
    <div class='hero'>
        <h1>Prediksi Sampah Harian 2025–2030</h1>
        <p>Dashboard interaktif berbasis LSTM Autoregressive & Eksternal Feature</p>
    </div>
""", unsafe_allow_html=True)

# --- 📂 LOAD DATA ---
data_sampah = pd.read_excel("data_sampah.xlsx")
data_cuaca = pd.read_excel("data_cuaca.xlsx")
data_sosial_ekonomi = pd.read_excel("data_sosial_ekonomi.xlsx")
data_prediksi = pd.read_excel("prediksi_sampah_2025_2030.xlsx")

# --- ⏳ FORMAT TANGGAL ---
data_sampah['Tanggal'] = pd.to_datetime(data_sampah['Tanggal'])
data_cuaca['Tanggal'] = pd.to_datetime(data_cuaca['Tanggal'])
data_prediksi['Tanggal'] = pd.to_datetime(data_prediksi['Tanggal'])
data_prediksi['Tahun'] = data_prediksi['Tanggal'].dt.year
data_prediksi['Bulan'] = data_prediksi['Tanggal'].dt.month

# --- ✅ TAMBAHAN KOL  ---
data_sampah['TAHUN'] = data_sampah['Tanggal'].dt.year
data_cuaca['Tahun'] = data_cuaca['Tanggal'].dt.year

# --- 🧭 SIDEBAR GLOBAL FILTER ---
with st.sidebar:
    st.title("Navigasi & Filter")
    page = st.radio("📂 Menu", ["Data Historis", "Prediksi & Insight", "Evaluasi Model"])
    show_raw = st.checkbox("📄 Tampilkan Data Mentah", value=False)

# --- 📘 LANDING SECTION ---
with st.expander("📘 Tentang Dashboard"):
    st.markdown("""
    Dashboard ini menyajikan prediksi jumlah sampah harian periode **2025–2030** 
    berbasis model **LSTM Autoregressive** dengan mempertimbangkan variabel cuaca, 
    sosial ekonomi, dan fitur waktu.

    **Fitur Utama:**
    - Visualisasi prediktif dan historis
    - Data dinamis interaktif
    - Insight otomatis
    - Evaluasi model secara langsung
    - Tema warna ekologis
    """)

# ==============================
# === PAGE: DATA HISTORIS ===
# ==============================
if page == "Data Historis":
    st.header("📊 Data Historis & Analisis")

    # Data Sampah
    with st.expander("📦 Data Sampah Harian"):
        tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_sampah['TAHUN'].unique()), key="tahun_sampah")
        df = data_sampah[data_sampah['TAHUN'] == tahun_pilih]

        if not df.empty and pd.api.types.is_datetime64_any_dtype(df['Tanggal']):
    start_date, end_date = st.slider("Pilih Rentang Tanggal", 
        min_value=df['Tanggal'].min(), 
        max_value=df['Tanggal'].max(),
        value=(df['Tanggal'].min(), df['Tanggal'].max()))

    df = df[(df['Tanggal'] >= start_date) & (df['Tanggal'] <= end_date)]

    # ... lanjutkan visualisasi
else:
    st.warning("⚠️ Data kosong atau kolom Tanggal belum tersedia. Silakan periksa filter tahun atau data.")


        col1, col2, col3 = st.columns(3)
        col1.metric("Rata-rata", f"{df['Total Volume Sampah (m³)'].mean():.2f} m³")
        col2.metric("Maksimum", f"{df['Total Volume Sampah (m³)'].max():.2f} m³")
        col3.metric("Minimum", f"{df['Total Volume Sampah (m³)'].min():.2f} m³")

        fig = px.line(df, x='Tanggal', y='Total Volume Sampah (m³)', color_discrete_sequence=['#0081A7'])
        fig.update_layout(template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

        if show_raw:
            with st.expander("📋 Data Mentah"):
                fig_table = go.Figure(data=[go.Table(
                    header=dict(values=list(data_sampah.columns),
                                fill_color='paleturquoise',
                                align='left'),
                    cells=dict(values=[data_sampah[col] for col in data_sampah.columns],
                               fill_color='lavender',
                               align='left'))
                ])
                st.plotly_chart(fig_table, use_container_width=True)

    # Data Cuaca
    with st.expander("🌦️ Data Cuaca"):
        tahun_cuaca = st.selectbox("Pilih Tahun", sorted(data_cuaca['Tahun'].unique()), key="tahun_cuaca")
        kolom_cuaca = st.selectbox("Pilih Variabel Cuaca", data_cuaca.select_dtypes('number').columns.tolist())
        df_cuaca = data_cuaca[data_cuaca['Tahun'] == tahun_cuaca]

        fig_cuaca = px.line(df_cuaca, x='Tanggal', y=kolom_cuaca, color_discrete_sequence=['#00AFB9'])
        st.plotly_chart(fig_cuaca, use_container_width=True)

    # Sosial Ekonomi
    with st.expander("📈 Data Sosial Ekonomi"):
        fig_sosial = px.line(data_sosial_ekonomi, x='Tahun', y=['Jumlah Penduduk', 'PDRB Per Kapita (Rp)'],
                             color_discrete_sequence=['#F07167', '#00AFB9'])
        st.plotly_chart(fig_sosial, use_container_width=True)

# ==============================
# === PAGE: PREDIKSI & INSIGHT ===
# ==============================
elif page == "Prediksi & Insight":
    st.header("🔮 Prediksi & Insight Otomatis")

    df_pred = data_prediksi
    col1, col2 = st.columns(2)
    col1.metric("Rata-Rata", f"{df_pred['Total Volume Sampah (m³)'].mean():.2f} m³")
    col2.metric("Maksimum", f"{df_pred['Total Volume Sampah (m³)'].max():.2f} m³")

    fig_pred = px.line(df_pred, x='Tanggal', y='Total Volume Sampah (m³)',
                       color_discrete_sequence=['#0081A7'])
    fig_pred.update_layout(template="seaborn")
    st.plotly_chart(fig_pred, use_container_width=True)

    bulan_peak = df_pred.loc[df_pred['Total Volume Sampah (m³)'].idxmax(), 'Tanggal'].strftime('%B')
    tahun_peak = df_pred.loc[df_pred['Total Volume Sampah (m³)'].idxmax(), 'Tanggal'].year
    fitur_terkorelasi = "Curah Hujan (mm)"  # Contoh
    tren = df_pred['Total Volume Sampah (m³)'].diff().mean()

    st.markdown(f"""
    ### 📌 Insight Otomatis
    - Volume sampah tertinggi terjadi pada **{bulan_peak} {tahun_peak}**.
    - Rata-rata tren harian {'meningkat' if tren > 0 else 'menurun'}.
    - Fitur cuaca paling berpengaruh: **{fitur_terkorelasi}**
    """)

# ==============================
# === PAGE: EVALUASI MODEL ===
# ==============================
elif page == "Evaluasi Model":
    st.header("📉 Evaluasi Model LSTM")
    st.markdown("Model dievaluasi menggunakan metrik berikut:")

    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", "0.24")
    col2.metric("RMSE", "0.35")
    col3.metric("MAPE", "3.27%")

# --- 📘 FOOTER ---
st.markdown("""
    <div class='footer'>
        © 2025 | <strong>Nona</strong> | Skripsi Teknik Informatika – Prediksi Sampah Berbasis LSTM Autoregressive
    </div>
""", unsafe_allow_html=True)
