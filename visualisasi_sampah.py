import pandas as pd

# ========== 1. Load Data ==========
# Pastikan file berada dalam direktori yang sama dengan file .py ini
file_sampah = 'data_sampah.xlsx'
file_cuaca = 'data_cuaca.xlsx'
file_ekonomi = 'data_ekonomi.xlsx'

# Baca data sampah
try:
    data_sampah = pd.read_excel(file_sampah)
    data_sampah['TANGGAL'] = pd.to_datetime(data_sampah['TANGGAL'])
    print("===== DATA SAMPAH =====")
    print(data_sampah.info())
    print(data_sampah.head())
    print("\n")
except Exception as e:
    print("Gagal membaca data sampah:", e)

# Baca data cuaca
try:
    data_cuaca = pd.read_excel(file_cuaca)
    if 'tanggal' in data_cuaca.columns:
        data_cuaca['tanggal'] = pd.to_datetime(data_cuaca['tanggal'])
    print("===== DATA CUACA =====")
    print(data_cuaca.info())
    print(data_cuaca.head())
    print("\n")
except Exception as e:
    print("Gagal membaca data cuaca:", e)

# Baca data sosial ekonomi
try:
    data_ekonomi = pd.read_excel(file_ekonomi)
    data_ekonomi.columns = data_ekonomi.columns.str.lower()  # normalisasi nama kolom
    print("===== DATA SOSIAL EKONOMI =====")
    print(data_ekonomi.info())
    print(data_ekonomi.head())
    print("\n")
except Exception as e:
    print("Gagal membaca data sosial ekonomi:", e)
