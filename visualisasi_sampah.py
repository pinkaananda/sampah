# --- 📦 LIBRARY SETUP ---
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO

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
        .metric-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        .metric-card {
            flex: 1 1 30%;
            background-color: #f5f5f5;
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        }
        @media (max-width: 768px) {
            .metric-card {
                flex: 1 1 100%;
            }
        }
    </style>
    <div class='hero'>
        <h1>Prediksi Sampah Harian 2025–2030</h1>
    </div>
""", unsafe_allow_html=True)

# --- 🧭 SIDEBAR GLOBAL FILTER ---
with st.sidebar:
    st.title("Filter Global")
    show_raw = st.checkbox("Tampilkan Data Mentah", value=False)

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

# --- 🧭 TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["Data Sampah", "Data Cuaca", "Sosial Ekonomi", "Hasil Prediksi"])

# --- TAB 1 ---
with tab1:
    st.subheader("Data Sampah Harian")
    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_sampah['TAHUN'].unique()), key="tahun_sampah")
    df = data_sampah[data_sampah['TAHUN'] == tahun_pilih]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Rata-rata Volume</h4>
            <p>{df['Total Volume Sampah (m³)'].mean():.2f} m³</p>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Maksimum Harian</h4>
            <p>{df['Total Volume Sampah (m³)'].max():.2f} m³</p>
        </div>""", unsafe_allow_html=True)

    fig = px.line(df, x='Tanggal', y='Total Volume Sampah (m³)', title=f"Volume Sampah Harian Tahun {tahun_pilih}",
                  labels={"Total Volume Sampah (m³)": "Volume (m³)"}, color_discrete_sequence=['#0081A7'])
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_sampah, use_container_width=True)

# --- TAB 2 ---
with tab2:
    st.subheader("Data Cuaca Harian")
    tahun_cuaca = st.selectbox("Pilih Tahun", sorted(data_cuaca['Tahun'].unique()), key="cuaca_tahun")
    kolom_pilih = st.selectbox("Pilih Variabel Cuaca", data_cuaca.select_dtypes('number').columns.tolist())
    df = data_cuaca[data_cuaca['Tahun'] == tahun_cuaca]
    fig = px.line(df, x='Tanggal', y=kolom_pilih, title=f"{kolom_pilih} Harian Tahun {tahun_cuaca}", color_discrete_sequence=['#00AFB9'])
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_cuaca, use_container_width=True)

# --- TAB 3 ---
with tab3:
    st.subheader("Data Sosial Ekonomi Tahunan")
    fig = px.line(data_sosial_ekonomi, x='Tahun', y=['Jumlah Penduduk', 'PDRB Per Kapita (Rp)'], color_discrete_sequence=['#F07167', '#00AFB9'],
                  title="Tren Jumlah Penduduk dan PDRB Per Kapita")
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_sosial_ekonomi, use_container_width=True)

# --- TAB 4 ---
with tab4:
    st.subheader("Prediksi Jumlah Sampah Harian (Ton) 2025–2030")

    col1, col2, col3 = st.columns(3)
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <h4>Rata-Rata</h4>
            <p>{data_prediksi['Total Volume Sampah (m³)'].mean():.2f} m³</p>
        </div>
        <div class="metric-card">
            <h4>Tahun Maksimum</h4>
            <p>{data_prediksi.groupby('Tahun')['Total Volume Sampah (m³)'].mean().idxmax()}</p>
        </div>
        <div class="metric-card">
            <h4>Tanggal Tertinggi</h4>
            <p>{data_prediksi.loc[data_prediksi['Total Volume Sampah (m³)'].idxmax(), 'Tanggal'].strftime('%d %b %Y')}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.line(data_prediksi, x='Tanggal', y='Total Volume Sampah (m³)',
                  title="Prediksi Sampah Harian 2025–2030", color_discrete_sequence=['#0081A7'])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Rata-Rata Bulanan")
    bulanan = data_prediksi.groupby(['Tahun', 'Bulan'])['Total Volume Sampah (m³)'].mean().reset_index()
    bulanan['BulanStr'] = pd.to_datetime(bulanan['Bulan'], format='%m').dt.strftime('%b')
    pivot_bulanan = bulanan.pivot(index='BulanStr', columns='Tahun', values='Total Volume Sampah (m³)')
    st.dataframe(pivot_bulanan, use_container_width=True)

    st.markdown("### 📈 Visualisasi Harian per Bulan")
    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_prediksi['Tahun'].unique()))
    bulan_pilih = st.selectbox("Pilih Bulan", list(range(1, 13)), format_func=lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
    df_bulan = data_prediksi[(data_prediksi['Tahun'] == tahun_pilih) & (data_prediksi['Bulan'] == bulan_pilih)]
    fig = px.line(df_bulan, x='Tanggal', y='Total Volume Sampah (m³)',
                  title=f"Prediksi Sampah Harian - {pd.to_datetime(str(bulan_pilih), format='%m').strftime('%B')} {tahun_pilih}", color_discrete_sequence=['#F07167'])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Rata-Rata Tahunan")
    rata_tahunan = data_prediksi.groupby('Tahun')['Total Volume Sampah (m³)'].mean().reset_index()
    fig_tahunan = px.bar(rata_tahunan, x='Tahun', y='Total Volume Sampah (m³)',
                         title="Rata-Rata Prediksi Tahunan", text_auto='.2s', color_discrete_sequence=['#00AFB9'])
    st.plotly_chart(fig_tahunan, use_container_width=True)
    if show_raw:
        st.dataframe(data_prediksi, use_container_width=True)

# --- 📘 FOOTER ---
st.markdown("""
    ---
    <p style='text-align:center; font-size:14px;'>
        © 2025 | <strong>Nona</strong> | Skripsi Teknik Informatika – Prediksi Sampah Berbasis LSTM Autoregressive
    </p>
""", unsafe_allow_html=True)
