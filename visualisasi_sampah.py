# --- 📦 LIBRARY SETUP ---
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 🧱 KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Prediksi Sampah", layout="wide", page_icon="🗑️")

# --- 💡 CUSTOM STYLING ---
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(to right, #00796B, #004D40);
            padding: 2rem;
            border-radius: 0.5rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .main-header p {
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
""", unsafe_allow_html=True)

# --- 🧭 SIDEBAR GLOBAL FILTER ---
with st.sidebar:
    st.title("Filter Global")
    show_raw = st.checkbox("Tampilkan Data Mentah", value=False)

# --- 📊 JUDUL UTAMA ---
st.markdown("""
    <div class='main-header'>
        <h1>Prediksi Jumlah Sampah Harian TPA Bumi Ayu</h1>
        <p>Skripsi Teknik Informatika | Prediksi LSTM Autoregressive | 2021–2030</p>
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

# --- 🧭 TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Sampah", "Data Cuaca", "Sosial Ekonomi", "Hasil Prediksi", "Simulasi Real-Time"])

# --- TAB 1 ---
with tab1:
    st.markdown("## Data Sampah Harian")
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
                  labels={"Total Volume Sampah (m³)": "Volume (m³)"}, markers=True)
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_sampah, use_container_width=True)

# --- TAB 2 ---
with tab2:
    st.markdown("## Data Cuaca Harian")
    tahun_cuaca = st.selectbox("Pilih Tahun", sorted(data_cuaca['Tahun'].unique()), key="cuaca_tahun")
    kolom_pilih = st.selectbox("Pilih Variabel Cuaca", data_cuaca.select_dtypes('number').columns.tolist())
    df = data_cuaca[data_cuaca['Tahun'] == tahun_cuaca]
    fig = px.line(df, x='Tanggal', y=kolom_pilih, title=f"{kolom_pilih} Harian Tahun {tahun_cuaca}", markers=True)
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_cuaca, use_container_width=True)

# --- TAB 3 ---
with tab3:
    st.markdown("## Data Sosial Ekonomi Tahunan")
    fig = px.line(data_sosial_ekonomi, x='Tahun', y=['Jumlah Penduduk', 'PDRB Per Kapita (Rp)'], markers=True,
                  title="Tren Jumlah Penduduk dan PDRB Per Kapita")
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_sosial_ekonomi, use_container_width=True)

# --- TAB 4 ---
with tab4:
    st.markdown("## Prediksi Jumlah Sampah Harian (Ton) 2025–2030")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-Rata", f"{data_prediksi['Total Volume Sampah (m³)'].mean():.2f} m³")
    col2.metric("Sampah Maksimum", f"{data_prediksi['Total Volume Sampah (m³)'].max():.2f} m³")
    col3.metric("Sampah Minimum", f"{data_prediksi['Total Volume Sampah (m³)'].min():.2f} m³")

    fig = px.line(data_prediksi, x='Tanggal', y='Total Volume Sampah (m³)',
                  title="Prediksi Sampah Harian 2025–2030", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Rata-Rata Bulanan")
    bulanan = data_prediksi.groupby(['Tahun', 'Bulan'])['Total Volume Sampah (m³)'].mean().reset_index()
    bulanan['BulanStr'] = pd.to_datetime(bulanan['Bulan'], format='%m').dt.strftime('%b')
    pivot_bulanan = bulanan.pivot(index='BulanStr', columns='Tahun', values='Total Volume Sampah (m³)')
    st.dataframe(pivot_bulanan, use_container_width=True)

    st.markdown("### Visualisasi Harian per Bulan")
    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_prediksi['Tahun'].unique()))
    bulan_pilih = st.selectbox("Pilih Bulan", list(range(1, 13)), format_func=lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
    df_bulan = data_prediksi[(data_prediksi['Tahun'] == tahun_pilih) & (data_prediksi['Bulan'] == bulan_pilih)]
    fig = px.line(df_bulan, x='Tanggal', y='Total Volume Sampah (m³)',
                  title=f"Prediksi Sampah Harian - {pd.to_datetime(str(bulan_pilih), format='%m').strftime('%B')} {tahun_pilih}", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Rata-Rata Tahunan")
    rata_tahunan = data_prediksi.groupby('Tahun')['Total Volume Sampah (m³)'].mean().reset_index()
    fig_tahunan = px.bar(rata_tahunan, x='Tahun', y='Total Volume Sampah (m³)',
                         title="Rata-Rata Prediksi Tahunan", text_auto='.2s')
    st.plotly_chart(fig_tahunan, use_container_width=True)
    if show_raw:
        st.dataframe(data_prediksi, use_container_width=True)

# --- TAB 5: SIMULASI REAL-TIME ---
with tab5:
    st.markdown("## 🚀 Simulasi Real-Time Harian")
    selected_date = st.slider("Pilih Tanggal", 
                              min_value=data_prediksi['Tanggal'].min().date(), 
                              max_value=data_prediksi['Tanggal'].max().date(), 
                              value=data_prediksi['Tanggal'].min().date(),
                              format="DD MMM YYYY")

    df_today = data_prediksi[data_prediksi['Tanggal'] == pd.to_datetime(selected_date)]
    if not df_today.empty:
        vol_today = df_today['Total Volume Sampah (m³)'].values[0]
        mean_vol = data_prediksi['Total Volume Sampah (m³)'].mean()
        high_thresh = data_prediksi['Total Volume Sampah (m³)'].quantile(0.95)

        if vol_today < mean_vol:
            status = "🟢 Normal"
        elif vol_today < high_thresh:
            status = "🟡 Waspada"
        else:
            status = "🔴 Kritis"

        st.metric("Volume Hari Ini", f"{vol_today:.2f} m³")
        st.markdown(f"### Status Hari Ini: {status}")

        fig_sim = px.bar(df_today, x='Tanggal', y='Total Volume Sampah (m³)',
                         title="Simulasi Volume Sampah Harian", color_discrete_sequence=['#00796B'])
        st.plotly_chart(fig_sim, use_container_width=True)
    else:
        st.warning("Data tidak tersedia untuk tanggal ini.")

# --- 📘 FOOTER ---
st.markdown("---")
st.caption("© 2025 | Nona | Skripsi Teknik Informatika – Prediksi Sampah Berbasis LSTM Autoregressive")
