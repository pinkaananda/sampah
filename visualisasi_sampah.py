# app.py
# Dashboard Lengkap Prediksi Sampah 2025–2030 + Prediksi Real-Time

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import plotly.express as px
import plotly.graph_objects as go

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Prediksi Sampah", layout="wide", page_icon="🗑️")

# --- GAYA TAMBAHAN ---
st.markdown("""
    <style>
        .hero {
            background: linear-gradient(120deg, #00afb9, #006d77);
            padding: 2rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
        }
        .hero h1 { font-family: 'Segoe UI', sans-serif; font-size: 3rem; margin-bottom: 0.2rem; }
        .metric-card {
            background-color: #e0f7fa;
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

# --- SIDEBAR ---
with st.sidebar:
    st.title("Filter Global")
    show_raw = st.checkbox("Tampilkan Data Mentah", value=False)

# --- LOAD DATA ---
data_sampah = pd.read_excel("data_sampah.xlsx")
data_cuaca = pd.read_excel("data_cuaca.xlsx")
data_sosial_ekonomi = pd.read_excel("data_sosial_ekonomi.xlsx")
data_prediksi = pd.read_excel("prediksi_sampah_2025_2030.xlsx")

# --- FORMAT TANGGAL ---
data_sampah['Tanggal'] = pd.to_datetime(data_sampah['Tanggal'])
data_cuaca['Tanggal'] = pd.to_datetime(data_cuaca['Tanggal'])
data_prediksi['Tanggal'] = pd.to_datetime(data_prediksi['Tanggal'])
data_prediksi['Tahun'] = data_prediksi['Tanggal'].dt.year
data_prediksi['Bulan'] = data_prediksi['Tanggal'].dt.month

# --- TAMBAHAN KOL --
data_sampah['TAHUN'] = data_sampah['Tanggal'].dt.year
data_cuaca['Tahun'] = data_cuaca['Tanggal'].dt.year

# --- TAB LAYOUT ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Data Sampah", "Data Cuaca", "Sosial Ekonomi", "Hasil Prediksi", "Prediksi Real Time"])

# --- TAB 1: Data Sampah ---
with tab1:
    st.subheader("Data Sampah Harian")
    tahun_pilih = st.selectbox("Pilih Tahun", sorted(data_sampah['TAHUN'].unique()), key="tahun_sampah")
    df = data_sampah[data_sampah['TAHUN'] == tahun_pilih]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='metric-card'><h4>Rata-rata Volume</h4><p>{df['Total Volume Sampah (m³)'].mean():.2f} m³</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'><h4>Maksimum Harian</h4><p>{df['Total Volume Sampah (m³)'].max():.2f} m³</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'><h4>Minimum Harian</h4><p>{df['Total Volume Sampah (m³)'].min():.2f} m³</p></div>""", unsafe_allow_html=True)

    fig = px.line(df, x='Tanggal', y='Total Volume Sampah (m³)', title=f"Volume Sampah Harian Tahun {tahun_pilih}", color_discrete_sequence=['#0081A7'])
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_sampah, use_container_width=True)

# --- TAB 2: Data Cuaca ---
with tab2:
    st.subheader("Data Cuaca Harian")
    tahun_cuaca = st.selectbox("Pilih Tahun", sorted(data_cuaca['Tahun'].unique()), key="cuaca_tahun")
    kolom_pilih = st.selectbox("Pilih Variabel Cuaca", data_cuaca.select_dtypes('number').columns.tolist())
    df = data_cuaca[data_cuaca['Tahun'] == tahun_cuaca]
    fig = px.line(df, x='Tanggal', y=kolom_pilih, title=f"{kolom_pilih} Harian Tahun {tahun_cuaca}", color_discrete_sequence=['#00AFB9'])
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_cuaca, use_container_width=True)

# --- TAB 3: Sosial Ekonomi ---
with tab3:
    st.subheader("Data Sosial Ekonomi Tahunan")
    fig = px.line(data_sosial_ekonomi, x='Tahun', y=['Jumlah Penduduk', 'PDRB Per Kapita (Rp)'], color_discrete_sequence=['#F07167', '#00AFB9'])
    st.plotly_chart(fig, use_container_width=True)
    if show_raw:
        st.dataframe(data_sosial_ekonomi, use_container_width=True)

# --- TAB 4: Hasil Prediksi ---
with tab4:
    st.subheader("Prediksi Jumlah Sampah Harian (Ton) 2025–2030")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='metric-card'><h4>Rata-Rata</h4><p>{data_prediksi['Total Volume Sampah (m³)'].mean():.2f} m³</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'><h4>Sampah Maksimum</h4><p>{data_prediksi['Total Volume Sampah (m³)'].max():.2f} m³</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'><h4>Sampah Minimum</h4><p>{data_prediksi['Total Volume Sampah (m³)'].min():.2f} m³</p></div>""", unsafe_allow_html=True)

    fig = px.line(data_prediksi, x='Tanggal', y='Total Volume Sampah (m³)', title="Prediksi Sampah Harian 2025–2030", color_discrete_sequence=['#0081A7'])
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 5: Prediksi Real Time ---
with tab5:
    st.subheader("🧠 Prediksi Jumlah Sampah Real Time Berdasarkan Input Pengguna")
    model = load_model('model_lstm.h5')
    scaler_x = joblib.load('scaler_x.save')
    scaler_y = joblib.load('scaler_y.save')

    tanggal = st.date_input("Tanggal Prediksi", value=pd.to_datetime("today"))
    is_holiday = st.checkbox("Hari Libur?")
    dayofweek = pd.to_datetime(tanggal).weekday()
    month = pd.to_datetime(tanggal).month
    dayofyear = pd.to_datetime(tanggal).day_of_year
    trend = st.slider("Nilai Trend", 0.0, 1.0, 0.5)

    input_df = pd.DataFrame([{
        'dayofweek': dayofweek,
        'month': month,
        'dayofyear': dayofyear,
        'is_holiday': int(is_holiday),
        'trend': trend
    }])

    input_scaled = scaler_x.transform(input_df)
    input_reshaped = input_scaled.reshape(1, 1, -1)

    if st.button("🔍 Prediksi Sekarang"):
        y_pred_scaled = model.predict(input_reshaped)
        y_pred = scaler_y.inverse_transform(y_pred_scaled)[0][0]
        st.success(f"📦 Prediksi Jumlah Sampah: **{y_pred:.2f} Ton** pada tanggal {tanggal.strftime('%d %B %Y')}")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=y_pred,
            title={'text': "Prediksi Sampah (Ton)"},
            gauge={'axis': {'range': [0, 500]}, 'bar': {'color': "#00AFB9"}}
        ))
        st.plotly_chart(fig_gauge)

        # Rekomendasi
        if y_pred > 200:
            st.warning("🚨 Volume tinggi! Perlu penguatan armada pengangkut.")
        elif y_pred < 100:
            st.info("✅ Volume rendah. Armada bisa dikurangi.")

        # Unduh CSV
        pred_result = pd.DataFrame([{"Tanggal": tanggal, "Prediksi Sampah (Ton)": y_pred}])
        st.download_button("⬇️ Unduh Hasil Prediksi", data=pred_result.to_csv(index=False), file_name="prediksi_sampah.csv")

# --- FOOTER ---
st.markdown("""
    ---
    <p style='text-align:center; font-size:14px;'>
        © 2025 | <strong>Nona</strong> | Skripsi Teknik Informatika – Prediksi Sampah Berbasis LSTM Autoregressive
    </p>
""", unsafe_allow_html=True)
