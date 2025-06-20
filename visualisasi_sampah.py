# --- 🎞 LIBRARY SETUP ---
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder

# --- 🧱 KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Prediksi Sampah", 
    layout="wide", 
    page_icon="🗑️"
)

# --- 🎨 CUSTOM STYLE ---
st.markdown("""
    <style>
        .hero {
            background: linear-gradient(120deg, #00afb9, #006d77);
            padding: 2rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
        }
        .hero h1 {
            font-family: 'Segoe UI', sans-serif;
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
    st.title("Filter Global")
    show_raw = st.checkbox("Tampilkan Data Mentah", value=False)

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
    """)

# --- 📊 TAB TUNGGAL: Data & Analisis ---
st.markdown("## 📊 Data & Analisis")

# --- 📦 DATA SAMPAH ---
with st.expander("📦 Data Sampah Harian"):
    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_sampah['TAHUN'].unique()), key="tahun_sampah")
    df = data_sampah[data_sampah['TAHUN'] == tahun_pilih]

    start_date, end_date = st.slider("Pilih Rentang Tanggal", 
        min_value=df['Tanggal'].min(), 
        max_value=df['Tanggal'].max(),
        value=(df['Tanggal'].min(), df['Tanggal'].max())
    )
    df = df[(df['Tanggal'] >= start_date) & (df['Tanggal'] <= end_date)]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rata-rata", f"{df['Total Volume Sampah (m³)'].mean():.2f} m³")
    with col2:
        st.metric("Jumlah Maksimum", f"{df['Total Volume Sampah (m³)'].max():.2f} m³")
    with col3:
        st.metric("Jumlah Minimum", f"{df['Total Volume Sampah (m³)'].min():.2f} m³")

    fig = px.line(df, x='Tanggal', y='Total Volume Sampah (m³)', title=f"Volume Sampah Harian Tahun {tahun_pilih}",
                  labels={"Total Volume Sampah (m³)": "Volume (m³)"}, color_discrete_sequence=['#0081A7'])
    fig.update_layout(template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

    max_vol = df['Total Volume Sampah (m³)'].max()
    tgl_max = df.loc[df['Total Volume Sampah (m³)'].idxmax(), 'Tanggal']
    avg = df['Total Volume Sampah (m³)'].mean()
    st.markdown(f"""
    📌 **Insight**: Volume sampah tertinggi sebesar **{max_vol:.2f} m³** terjadi pada **{tgl_max.strftime('%d %B %Y')}**.
    Rata-rata volume sampah periode ini adalah **{avg:.2f} m³**.
    """)

    if show_raw:
        with st.expander("📋 Tampilkan Data Mentah Sampah"):
            gb = GridOptionsBuilder.from_dataframe(data_sampah)
            gb.configure_pagination()
            gb.configure_side_bar()
            gb.configure_default_column(filter=True, sortable=True, editable=False, resizable=True)
            gridOptions = gb.build()
            AgGrid(data_sampah, gridOptions=gridOptions, theme="blue")
            csv = data_sampah.to_csv(index=False).encode('utf-8')
            st.download_button("📅 Unduh Data Sampah", csv, "data_sampah.csv", "text/csv")

# --- 🌦️ DATA CUACA ---
with st.expander("🌦️ Data Cuaca Harian"):
    tahun_cuaca = st.selectbox("Pilih Tahun", sorted(data_cuaca['Tahun'].unique()), key="tahun_cuaca")
    kolom_pilih = st.selectbox("Pilih Variabel Cuaca", data_cuaca.select_dtypes('number').columns.tolist())
    df_cuaca = data_cuaca[data_cuaca['Tahun'] == tahun_cuaca]

    start_cuaca, end_cuaca = st.slider("Pilih Rentang Tanggal Cuaca", 
        min_value=df_cuaca['Tanggal'].min(), max_value=df_cuaca['Tanggal'].max(),
        value=(df_cuaca['Tanggal'].min(), df_cuaca['Tanggal'].max()))
    df_cuaca = df_cuaca[(df_cuaca['Tanggal'] >= start_cuaca) & (df_cuaca['Tanggal'] <= end_cuaca)]

    fig_cuaca = px.line(df_cuaca, x='Tanggal', y=kolom_pilih, title=f"{kolom_pilih} Tahun {tahun_cuaca}",
                        color_discrete_sequence=['#00AFB9'])
    st.plotly_chart(fig_cuaca, use_container_width=True)

    st.markdown(f"""
    📌 **Insight**: Nilai maksimum variabel **{kolom_pilih}** adalah **{df_cuaca[kolom_pilih].max():.2f}**.
    Rata-rata nilai: **{df_cuaca[kolom_pilih].mean():.2f}**.
    """)

    if show_raw:
        with st.expander("📋 Tampilkan Data Mentah Cuaca"):
            gb = GridOptionsBuilder.from_dataframe(data_cuaca)
            gb.configure_pagination()
            gb.configure_side_bar()
            gb.configure_default_column(filter=True, sortable=True, editable=False, resizable=True)
            gridOptions = gb.build()
            AgGrid(data_cuaca, gridOptions=gridOptions, theme="blue")
            csv = data_cuaca.to_csv(index=False).encode('utf-8')
            st.download_button("📅 Unduh Data Cuaca", csv, "data_cuaca.csv", "text/csv")

# --- 📈 SOSIAL EKONOMI ---
with st.expander("📈 Data Sosial Ekonomi"):
    fig_sosial = px.line(data_sosial_ekonomi, x='Tahun', y=['Jumlah Penduduk', 'PDRB Per Kapita (Rp)'],
                         title="Tren Sosial Ekonomi", color_discrete_sequence=['#F07167', '#00AFB9'])
    st.plotly_chart(fig_sosial, use_container_width=True)
    pertumbuhan_penduduk = data_sosial_ekonomi['Jumlah Penduduk'].pct_change().mean() * 100
    st.markdown(f"""
    📌 **Insight**: Rata-rata pertumbuhan jumlah penduduk adalah **{pertumbuhan_penduduk:.2f}%** per tahun.
    """)

    if show_raw:
        with st.expander("📋 Tampilkan Data Mentah Sosial Ekonomi"):
            gb = GridOptionsBuilder.from_dataframe(data_sosial_ekonomi)
            gb.configure_pagination()
            gb.configure_side_bar()
            gb.configure_default_column(filter=True, sortable=True, editable=False, resizable=True)
            gridOptions = gb.build()
            AgGrid(data_sosial_ekonomi, gridOptions=gridOptions, theme="blue")
            csv = data_sosial_ekonomi.to_csv(index=False).encode('utf-8')
            st.download_button("📅 Unduh Data Sosial Ekonomi", csv, "data_sosial_ekonomi.csv", "text/csv")

# --- 🔮 HASIL PREDIKSI ---
with st.expander("🔮 Hasil Prediksi 2025–2030"):
    df_pred = data_prediksi
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rata-Rata", f"{df_pred['Total Volume Sampah (m³)'].mean():.2f} m³")
    with col2:
        st.metric("Jumlah Maksimum", f"{df_pred['Total Volume Sampah (m³)'].max():.2f} m³")

    fig_pred = px.line(df_pred, x='Tanggal', y='Total Volume Sampah (m³)',
                       title="Prediksi Volume Sampah Harian 2025–2030",
                       color_discrete_sequence=['#0081A7'])
    fig_pred.update_layout(template="seaborn")
    st.plotly_chart(fig_pred, use_container_width=True)

    st.markdown(f"""
    📌 **Insight**: Prediksi volume sampah tertinggi adalah **{df_pred['Total Volume Sampah (m³)'].max():.2f} m³**.
    """)

    if show_raw:
        with st.expander("📋 Tampilkan Data Prediksi"):
            gb = GridOptionsBuilder.from_dataframe(df_pred)
            gb.configure_pagination()
            gb.configure_side_bar()
            gb.configure_default_column(filter=True, sortable=True, editable=False, resizable=True)
            gridOptions = gb.build()
            AgGrid(df_pred, gridOptions=gridOptions, theme="blue")
            csv = df_pred.to_csv(index=False).encode('utf-8')
            st.download_button("📅 Unduh Data Prediksi", csv, "data_prediksi.csv", "text/csv")
