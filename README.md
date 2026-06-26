# Prediksi Jumlah Sampah Menggunakan Long Short-Term Memory (LSTM)

## Deskripsi Proyek

Proyek ini merupakan penelitian dan pengembangan sistem prediksi jumlah sampah menggunakan metode Deep Learning berbasis Recurrent Neural Network (RNN), khususnya Long Short-Term Memory (LSTM). Fokus utama penelitian adalah melakukan prediksi jumlah sampah harian untuk periode jangka panjang tahun 2025–2030 berdasarkan data historis tahun 2021–2024.

Penelitian ini memanfaatkan kombinasi data time series dan fitur eksternal untuk meningkatkan kemampuan model dalam memahami pola jumlah sampah. Selain menggunakan data historis volume sampah sebagai target utama, penelitian juga mempertimbangkan faktor eksternal seperti:

* Data cuaca
* Data penduduk
* Data ekonomi
* Fitur waktu (temporal features)

Pendekatan yang digunakan meliputi:

* Univariate LSTM
* Multivariate LSTM
* Feature Engineering berbasis waktu
* Sliding Window Sequence
* Prediksi autoregressive jangka panjang
* Evaluasi performa model menggunakan beberapa metrik

Tujuan akhir dari proyek ini adalah menghasilkan model prediksi jumlah sampah yang:

* Stabil untuk prediksi jangka panjang
* Mampu menangkap pola musiman dan tren
* Dapat membantu pengambilan keputusan dalam pengelolaan sampah
* Dapat divisualisasikan secara interaktif menggunakan dashboard

---

# Latar Belakang

Jumlah sampah terus meningkat setiap tahun seiring dengan pertumbuhan penduduk, aktivitas ekonomi, serta perubahan pola konsumsi masyarakat. Pengelolaan sampah yang efektif memerlukan perencanaan yang baik, termasuk kemampuan untuk memprediksi jumlah sampah pada masa mendatang.

Metode statistik tradisional sering mengalami keterbatasan dalam menangkap pola non-linear dan dependensi jangka panjang pada data time series. Oleh karena itu, digunakan pendekatan Deep Learning menggunakan Long Short-Term Memory (LSTM) karena mampu mempelajari pola temporal secara lebih baik.

Selain itu, penelitian ini juga mengevaluasi pengaruh fitur eksternal seperti cuaca, penduduk, dan ekonomi terhadap jumlah sampah untuk mengetahui apakah fitur-fitur tersebut mampu meningkatkan performa model.

---

# Tujuan Penelitian

## Tujuan Utama

Membangun model prediksi jumlah sampah berbasis LSTM untuk memprediksi jumlah sampah harian tahun 2025–2030.

## Tujuan Khusus

1. Menganalisis pola jumlah sampah berdasarkan data historis.
2. Melakukan preprocessing dan feature engineering pada data time series.
3. Membangun model LSTM untuk prediksi jumlah sampah.
4. Membandingkan performa model berdasarkan kombinasi fitur.
5. Menguji pengaruh fitur eksternal terhadap hasil prediksi.
6. Menghasilkan prediksi jangka panjang yang stabil.
7. Membuat visualisasi hasil prediksi menggunakan dashboard interaktif.

---

# Dataset

Penelitian menggunakan beberapa sumber data:

## 1. Data Sampah

Data utama berupa jumlah volume sampah harian.

### Informasi:

* Periode: 2021–2024
* Frekuensi: Harian
* Variabel target: Volume Sampah
* Satuan awal: m³
* Konversi ke ton:

```python
volume_ton = volume_m3 * 0.25
```

### Kolom yang digunakan:

* Tanggal
* Volume Sampah
* Jenis Kendaraan Pengangkut
* Jumlah Kendaraan

---

## 2. Data Cuaca

Data cuaca digunakan sebagai fitur eksternal.

### Variabel:

* Curah hujan
* Temperatur
* Kelembapan
* Kecepatan angin
* Kondisi cuaca lainnya

### Frekuensi:

* Harian

---

## 3. Data Penduduk

Data jumlah penduduk digunakan sebagai fitur eksternal.

### Frekuensi:

* Tahunan

### Proses:

Karena data bersifat tahunan sedangkan model menggunakan data harian, dilakukan:

1. Interpolasi menjadi bulanan
2. Resampling menjadi harian
3. Forward fill pada setiap hari dalam bulan

---

## 4. Data Ekonomi

Data ekonomi digunakan sebagai fitur eksternal.

### Variabel:

* PDRB
* PDRB per kapita
* Indikator ekonomi lainnya

### Frekuensi:

* Tahunan

### Proses:

Sama seperti data penduduk:

1. Interpolasi tahunan → bulanan
2. Resampling bulanan → harian
3. Forward fill

---

# Tahapan Penelitian

# 1. Data Understanding

Tahap awal dilakukan untuk memahami karakteristik data.

## Proses yang dilakukan:

* Analisis statistik deskriptif
* Mengecek tipe data
* Mengecek missing value
* Mengecek distribusi data
* Visualisasi time series
* Analisis pola musiman
* Analisis tren
* Deteksi outlier

## Insight yang diperoleh:

* Data memiliki pola musiman tertentu
* Terdapat fluktuasi harian
* Terdapat beberapa outlier pada volume sampah
* Volume sampah cenderung meningkat pada periode tertentu

---

# 2. Data Preprocessing

Tahap preprocessing dilakukan agar data siap digunakan pada model LSTM.

## Langkah-langkah:

### a. Konversi Tanggal

Mengubah kolom tanggal menjadi format datetime.

```python
pd.to_datetime()
```

---

### b. Menangani Missing Value

Metode yang digunakan:

* Forward fill
* Interpolasi
* Penghapusan data tertentu jika diperlukan

---

### c. Penanganan Outlier

Outlier hanya ditangani pada kolom volume sampah.

Tidak dilakukan pada:

* Jumlah kendaraan
* Truk
* Pick Up
* Roda 3

Karena jumlah kendaraan harus tetap berupa bilangan bulat.

---

### d. Scaling Data

Digunakan MinMaxScaler untuk normalisasi.

```python
from sklearn.preprocessing import MinMaxScaler
```

Rentang scaling:

```python
0 - 1
```

---

# 3. Feature Engineering

Feature engineering dilakukan untuk membantu model memahami pola temporal.

## Fitur Waktu yang Digunakan

### a. Day of Week

Menunjukkan hari dalam minggu.

```python
df['dayofweek']
```

---

### b. Month

Menunjukkan bulan.

```python
df['month']
```

---

### c. Trend

Representasi tren waktu.

```python
df['trend'] = np.arange(len(df))
```

---

### d. Is Weekend

Menandai akhir pekan.

```python
1 = weekend
0 = weekday
```

---

### e. Is Holiday

Menandai hari libur.

---

### f. Is Tomorrow Holiday

Menandai apakah hari berikutnya adalah hari libur.

---

### g. Is Big Event

Menandai hari-hari tertentu dengan potensi peningkatan volume sampah.

---

# Fitur yang Tidak Digunakan

Beberapa fitur sempat diuji namun tidak digunakan karena menyebabkan oversmoothing dan ketidakstabilan:

* Lag feature
* Moving Average
* Differencing

---

# 4. Pemilihan Fitur Eksternal

Penelitian melakukan analisis pengaruh fitur eksternal menggunakan:

## Mutual Information (MI)

Tujuan:

* Mengukur relevansi fitur terhadap target
* Menentukan fitur eksternal paling berpengaruh

Fitur diuji satu per satu untuk melihat pengaruhnya terhadap performa model.

---

# 5. Pembentukan Sequence Data

Karena LSTM memerlukan data sequence, digunakan teknik sliding window.

## Contoh:

Jika menggunakan:

```python
window_size = 30
```

Maka model menggunakan 30 hari sebelumnya untuk memprediksi hari berikutnya.

---

# 6. Pembagian Data

Data dibagi menjadi:

* Training set
* Validation set
* Testing set

Pembagian dilakukan secara time series split.

Tidak menggunakan shuffle agar urutan temporal tetap terjaga.

---

# Arsitektur Model

Penelitian mengeksplorasi beberapa arsitektur:

## 1. Single LSTM

```python
LSTM(50)
Dense(1)
```

---

## 2. Double LSTM

```python
LSTM(128, return_sequences=True)
LSTM(64)
Dense(1)
```

---

## 3. Bidirectional LSTM

```python
Bidirectional(LSTM(64))
Dense(1)
```

---

# Hyperparameter

Beberapa hyperparameter yang diuji:

| Parameter     | Nilai            |
| ------------- | ---------------- |
| Neuron        | 50, 64, 100, 128 |
| Epoch         | 32, 64           |
| Batch Size    | 32, 64           |
| Learning Rate | 0.001, 0.0005    |
| Optimizer     | Adam             |
| Loss Function | MSE              |
| Dropout       | 0.1 - 0.3        |

---

# Strategi Eksperimen

Penelitian menggunakan beberapa skenario:

## 1. Univariate

Hanya menggunakan:

* Volume sampah

---

## 2. Univariate + Feature Engineering

Menggunakan:

* Volume sampah
* Fitur waktu

---

## 3. Multivariate

Menggunakan:

* Volume sampah
* Cuaca
* Penduduk
* Ekonomi
* Fitur waktu

---

# Pendekatan Prediksi Jangka Panjang

Untuk melakukan prediksi tahun 2025–2030 digunakan pendekatan:

## Autoregressive Forecasting

Output prediksi sebelumnya digunakan kembali sebagai input berikutnya.

### Alur:

1. Model memprediksi hari ke-1
2. Hasil prediksi dimasukkan ke sequence
3. Sequence baru digunakan memprediksi hari berikutnya
4. Proses diulang hingga 2030

---

# Synthetic Forecasting untuk Fitur Eksternal

Karena prediksi dilakukan hingga 2030, fitur eksternal masa depan juga perlu disiapkan.

## Strategi:

### Penduduk

Menggunakan:

* Interpolasi
* Growth trend

---

### Ekonomi

Menggunakan:

* Pertumbuhan tahunan
* Proyeksi linear/trend

---

### Cuaca

Menggunakan:

* Pola historis
* Seasonal pattern

---

# Evaluasi Model

Model dievaluasi menggunakan beberapa metrik.

## 1. Mean Squared Error (MSE)

Mengukur rata-rata error kuadrat.

---

## 2. Mean Absolute Error (MAE)

Mengukur rata-rata error absolut.

---

## 3. Root Mean Squared Error (RMSE)

Mengukur error dalam skala asli.

---

## 4. Mean Absolute Percentage Error (MAPE)

Mengukur error dalam bentuk persentase.

---

# Fokus Evaluasi

Penelitian lebih berfokus pada:

* Stabilitas prediksi
* Generalisasi model
* Konsistensi pola
* Kemampuan prediksi jangka panjang

Daripada hanya mengejar akurasi ekstrem pada data testing.

---

# Hasil Penelitian

## Temuan Utama

1. Feature engineering berbasis waktu sangat membantu model memahami pola temporal.
2. Penggunaan lag dan moving average menyebabkan oversmoothing.
3. Model yang terlalu kompleks cenderung overfitting.
4. Learning rate kecil memberikan hasil lebih stabil.
5. Double LSTM dengan neuron sedang memberikan keseimbangan terbaik.
6. Penambahan fitur eksternal tertentu meningkatkan performa model.
7. Prediksi autoregressive dapat digunakan untuk forecasting jangka panjang.

---

# Konfigurasi Model Terbaik

Contoh konfigurasi model stabil:

```python
model = Sequential([
    LSTM(128, return_sequences=True),
    LSTM(64),
    Dense(1)
])
```

### Konfigurasi:

| Parameter     | Nilai  |
| ------------- | ------ |
| Learning Rate | 0.0005 |
| Epoch         | 64     |
| Batch Size    | 32     |
| Optimizer     | Adam   |

Fokus utama model:

* Stabil
* Tidak overfitting
* Mampu generalisasi
* Cocok untuk forecasting jangka panjang

---

# Visualisasi

Visualisasi yang digunakan:

* Grafik aktual vs prediksi
* Grafik loss training dan validation
* Visualisasi tren prediksi 2025–2030
* Dashboard interaktif

---

# Dashboard Streamlit

Hasil prediksi divisualisasikan menggunakan Streamlit.

## Fitur Dashboard

* Statistik total volume sampah
* Grafik prediksi
* Perbandingan aktual vs prediksi
* Filter tahun
* Visualisasi kendaraan
* Insight data

---

# Teknologi yang Digunakan

## Bahasa Pemrograman

* Python

---

## Library Data Processing

```python
pandas
numpy
```

---

## Library Visualisasi

```python
matplotlib
seaborn
plotly
```

---

## Library Machine Learning dan Deep Learning

```python
scikit-learn
tensorflow
keras
```

---

## Dashboard

```python
streamlit
```

---

# Alur Pipeline Penelitian

```text
Data Collection
        ↓
Data Understanding
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Feature Selection
        ↓
Scaling
        ↓
Sliding Window
        ↓
Train Test Split
        ↓
Modeling LSTM
        ↓
Evaluation
        ↓
Forecasting 2025–2030
        ↓
Visualization Dashboard
```

---

# Cara Menjalankan Proyek

## 1. Clone Repository

```bash
git clone https://github.com/username/nama-repository.git
```

---

## 2. Masuk ke Folder

```bash
cd nama-repository
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Jalankan Notebook

Gunakan:

```bash
jupyter notebook
```

---

## 5. Jalankan Streamlit

```bash
streamlit run app.py
```

---

# Contoh Output

## Prediksi Harian

| Tanggal    | Prediksi Sampah |
| ---------- | --------------- |
| 2025-01-01 | xx ton          |
| 2025-01-02 | xx ton          |
| 2025-01-03 | xx ton          |

---

# Kelebihan Penelitian

* Menggunakan pendekatan deep learning modern
* Memanfaatkan fitur eksternal
* Mendukung prediksi jangka panjang
* Menggunakan feature engineering temporal
* Memiliki dashboard visualisasi interaktif
* Menggunakan pendekatan autoregressive forecasting

---

# Keterbatasan Penelitian

* Data historis masih terbatas
* Prediksi jangka panjang memiliki potensi error akumulatif
* Data ekonomi dan penduduk berasal dari interpolasi
* Cuaca masa depan masih menggunakan pendekatan proyeksi

---

# Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dilakukan:

* Menggunakan Transformer Time Series
* Menggunakan Temporal Fusion Transformer (TFT)
* Menambahkan data hari besar nasional otomatis
* Menggunakan data real-time IoT
* Hybrid LSTM + Attention
* Hyperparameter tuning otomatis
* Deploy ke cloud server

---

# Dokumentasi Notebook

## Notebook Utama

| Notebook                    | Fungsi                  |
| --------------------------- | ----------------------- |
| data_understanding.ipynb    | Analisis awal data      |
| preprocessing.ipynb         | Preprocessing data      |
| feature_engineering.ipynb   | Pembuatan fitur         |
| modeling.ipynb              | Training model          |
| forecasting_2025_2030.ipynb | Prediksi jangka panjang |

---

# Referensi

## Framework

* TensorFlow
* Keras
* Scikit-learn
* Streamlit

---

## Metode

* Long Short-Term Memory (LSTM)
* Recurrent Neural Network (RNN)
* Time Series Forecasting
* Feature Engineering
* Autoregressive Forecasting

---

# Author

## Nama

Pinka Ananda

## Bidang

* Artificial Intelligence
* Data Science
* Machine Learning
* Time Series Forecasting
* Deep Learning

---

# Penutup

Proyek ini dikembangkan sebagai implementasi penerapan Deep Learning untuk membantu proses pengelolaan sampah melalui prediksi jumlah sampah jangka panjang. Dengan memanfaatkan data historis, fitur eksternal, serta pendekatan LSTM, diharapkan hasil penelitian dapat membantu proses perencanaan dan pengambilan keputusan yang lebih baik dalam pengelolaan sampah.
