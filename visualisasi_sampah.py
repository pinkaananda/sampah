# visualisasi_sampah.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# --- Load Data ---
# Ganti path sesuai lokasi file kamu
DATA_PATH = 'data_sampah.xlsx'

st.title("Visualisasi Data Mentah Sampah")

data = pd.read_excel(data_sampah.xslx, header=1)
data['TANGGAL'] = pd.to_datetime(data['TANGGAL'])

# Sidebar filter tanggal
st.sidebar.header("Filter Data Berdasarkan Tanggal")
min_date = data['TANGGAL'].min()
max_date = data['TANGGAL'].max()

start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date)

if start_date > end_date:
    st.sidebar.error("Tanggal mulai harus sebelum tanggal akhir")

# Filter data berdasarkan tanggal
mask = (data['TANGGAL'] >= pd.to_datetime(start_date)) & (data['TANGGAL'] <= pd.to_datetime(end_date))
filtered_data = data.loc[mask]

# Tampilkan data mentah
st.subheader(f"Data Sampah dari {start_date} sampai {end_date}")
st.dataframe(filtered_data)

# Kolom yang akan divisualisasi
cols_volume = ['VOL. SELURUH M3', 'VOL 8M3', 'VOL 4 M3', 'VOL 1,5 M3']

# Plot Time Series Volume Sampah
st.subheader("Time Series Volume Sampah")
fig, ax = plt.subplots(figsize=(12,4))
ax.plot(filtered_data['TANGGAL'], filtered_data['VOL. SELURUH M3'], label='VOL. SELURUH M3', color='blue')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Volume Sampah (m³)")
ax.set_title("Volume Sampah Harian")
ax.legend()
st.pyplot(fig)

# Boxplot Volume Sampah (filtered)
st.subheader("Boxplot Volume Sampah")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.boxplot(data=filtered_data[cols_volume], ax=ax2)
ax2.set_title("Distribusi Volume Sampah")
st.pyplot(fig2)

# Histogram Volume Sampah utama
st.subheader("Histogram Volume Sampah (VOL. SELURUH M3)")
fig3, ax3 = plt.subplots(figsize=(10,4))
sns.histplot(filtered_data['VOL. SELURUH M3'], bins=30, kde=True, ax=ax3)
ax3.set_xlabel("Volume Sampah (m³)")
ax3.set_ylabel("Frekuensi")
st.pyplot(fig3)
