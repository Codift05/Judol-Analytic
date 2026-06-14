# Catatan Hasil Pipeline GSII Google Trends

Judul proyek:

**Sistem Peringatan Dini Peningkatan Minat Pencarian Judi Online di Sulawesi Utara Menggunakan Data Mining**

Dataset utama:

`Dataset/time_series_ID_20200101-0000_20260614-1837.csv`

Pipeline tersedia dalam dua bentuk:

- Script Python: `pipelines/google_trends_gsii_pipeline.py`
- Notebook seperti Google Colab: `notebooks/google_trends_gsii_pipeline.ipynb`

## Status Pengerjaan

Semua komponen utama yang diminta sudah dimasukkan:

- Load dataset CSV dengan `pandas`.
- Menampilkan 5 data awal.
- Menampilkan informasi kolom, tipe data, jumlah baris, dan missing value.
- Menangani kemungkinan metadata Google Trends di bagian atas CSV.
- Membersihkan nama kolom, misalnya `slot gacor` menjadi `slot_gacor`.
- Mengubah kolom tanggal menjadi `datetime`.
- Mengubah seluruh nilai keyword menjadi numerik.
- Menangani nilai seperti `<1` menjadi `0`.
- Membuat statistik deskriptif keyword.
- Menghitung mean, median, standar deviasi, maksimum, dan jumlah nilai bukan nol.
- Menentukan keyword yang layak berdasarkan jumlah nilai bukan nol.
- Membuat grafik tren setiap keyword.
- Membuat heatmap korelasi antar keyword.
- Menyimpan grafik ke `outputs/figures`.
- Membentuk indeks gabungan `GSII`.
- Membuat fitur time series: `lag_1`, `lag_2`, `lag_3`, `rolling_mean_3`, `rolling_std_3`, `month`, `year`.
- Membuat target `target_next_month = GSII.shift(-1)`.
- Menggunakan time-based split 80:20.
- Membandingkan baseline naive forecasting dan Random Forest.
- Menyiapkan XGBoost dan LightGBM sebagai model opsional jika library terinstall.
- Menghitung MAE, RMSE, dan MAPE.
- Menyimpan tabel evaluasi model.
- Membuat grafik aktual vs prediksi.
- Membuat grafik model terbaik.
- Membuat aturan early warning sederhana.
- Menyimpan output data, tabel, dan grafik.

## Ringkasan Dataset

Dataset yang terbaca memiliki:

- Jumlah baris: 73
- Jumlah kolom: 9
- Rentang data bulanan: mulai `2019-12-01` sampai `2025-12-01`
- Kolom tanggal: `date`
- Keyword setelah cleaning:
  - `judi_online`
  - `slot_gacor`
  - `togel_online`
  - `judi_slot`
  - `situs_judi`
  - `slot88`
  - `pragmatic_play`
  - `gacor_hari_ini`

Tidak ada missing value pada dataset setelah proses load dan cleaning.

## Hasil Statistik Keyword

Ringkasan keyword berdasarkan jumlah nilai bukan nol:

| Keyword | Mean | Median | Std | Max | Non-zero Count | Rekomendasi Model |
|---|---:|---:|---:|---:|---:|---|
| `slot_gacor` | 8.48 | 1.00 | 20.55 | 100 | 46 | Ya |
| `judi_slot` | 0.88 | 0.00 | 1.70 | 8 | 26 | Ya |
| `slot88` | 0.25 | 0.00 | 0.43 | 1 | 18 | Ya |
| `judi_online` | 0.32 | 0.00 | 0.66 | 3 | 16 | Ya |
| `situs_judi` | 0.38 | 0.00 | 0.98 | 4 | 11 | Ya |
| `gacor_hari_ini` | 0.22 | 0.00 | 0.98 | 8 | 9 | Ya |
| `togel_online` | 0.11 | 0.00 | 0.49 | 3 | 4 | Tidak |
| `pragmatic_play` | 0.01 | 0.00 | 0.12 | 1 | 1 | Tidak |

Catatan:

- `slot_gacor` adalah keyword dengan sinyal paling kuat karena memiliki nilai bukan nol terbanyak dan nilai maksimum tertinggi.
- `judi_slot` dan `judi_online` tetap digunakan dalam GSII karena sesuai rancangan awal proyek.
- `togel_online` dan `pragmatic_play` tetap dianalisis di EDA, tetapi tidak direkomendasikan untuk model utama karena terlalu banyak nilai nol.

## Pembentukan GSII

GSII dibentuk dari rata-rata keyword utama:

```text
GSII = rata-rata(slot_gacor, judi_slot, judi_online)
```

Kolom yang dipakai pada data ini:

- `slot_gacor`
- `judi_slot`
- `judi_online`

Output tersimpan di:

`outputs/processed/google_trends_gsii.csv`

## Fitur Forecasting

Fitur yang dibuat:

- `lag_1`
- `lag_2`
- `lag_3`
- `rolling_mean_3`
- `rolling_std_3`
- `month`
- `year`

Target:

```text
target_next_month = GSII.shift(-1)
```

Output fitur tersimpan di:

`outputs/processed/google_trends_gsii_features.csv`

## Evaluasi Model

Hasil evaluasi saat pipeline dijalankan:

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Baseline_Naive | 4.79 | 5.97 | 64.02 |
| Random_Forest | 13.15 | 16.76 | 78.22 |

Model terbaik berdasarkan RMSE:

`Baseline_Naive`

Interpretasi singkat:

- Baseline naive lebih baik daripada Random Forest pada data uji saat ini.
- Ini bisa terjadi karena jumlah data relatif kecil dan deret GSII cukup banyak bernilai rendah atau nol.
- Random Forest belum tentu buruk, tetapi pada data kecil model yang lebih kompleks bisa sulit menangkap pola secara stabil.
- XGBoost dan LightGBM belum dijalankan karena belum terinstall. Untuk mengaktifkan:

```bash
pip install -r requirements-optional.txt
```

Tabel evaluasi tersimpan di:

`outputs/tables/model_evaluation.csv`

## Hasil Early Warning

Status peringatan dini terakhir:

| Tanggal Saat Ini | Tanggal Prediksi | Model | GSII Saat Ini | Prediksi GSII Bulan Depan | Perubahan | Status |
|---|---|---|---:|---:|---:|---|
| 2025-12-01 | 2026-01-01 | Baseline_Naive | 1.00 | 1.00 | 0.00% | Normal |

Interpretasi:

- Prediksi GSII bulan berikutnya tidak naik dibandingkan GSII saat ini.
- Karena kenaikan prediksi 0%, status sistem adalah `Normal`.
- Aturan yang digunakan:
  - Naik minimal 40%: `Tinggi`
  - Naik minimal 20%: `Waspada`
  - Naik positif tetapi kurang dari 20%: `Perhatian`
  - Tidak naik: `Normal`

Output tersimpan di:

`outputs/tables/early_warning_status.csv`

## File Output Penting

Data hasil proses:

- `outputs/processed/google_trends_gsii.csv`
- `outputs/processed/google_trends_gsii_features.csv`

Tabel:

- `outputs/tables/keyword_summary.csv`
- `outputs/tables/model_evaluation.csv`
- `outputs/tables/model_predictions.csv`
- `outputs/tables/early_warning_status.csv`

Grafik:

- `outputs/figures/keyword_trends_all.png`
- `outputs/figures/keyword_correlation_heatmap.png`
- `outputs/figures/actual_vs_prediction_Baseline_Naive.png`
- `outputs/figures/actual_vs_prediction_Random_Forest.png`
- `outputs/figures/best_model_actual_vs_prediction.png`
- `outputs/figures/trend_slot_gacor.png`
- `outputs/figures/trend_judi_slot.png`
- `outputs/figures/trend_judi_online.png`
- `outputs/figures/trend_togel_online.png`
- `outputs/figures/trend_situs_judi.png`
- `outputs/figures/trend_slot88.png`
- `outputs/figures/trend_pragmatic_play.png`
- `outputs/figures/trend_gacor_hari_ini.png`

## Cara Menjalankan

Versi script:

```bash
python pipelines/google_trends_gsii_pipeline.py
```

Versi notebook:

```text
Buka notebooks/google_trends_gsii_pipeline.ipynb di VS Code,
pilih kernel Python,
lalu jalankan cell satu per satu atau klik Run All.
```

## Catatan untuk Laporan GEMASTIK

Pipeline ini sudah dapat dijadikan dasar sistem peringatan dini karena memiliki alur lengkap:

1. Mengambil data Google Trends.
2. Membersihkan dan menstandarkan data.
3. Melakukan EDA untuk memahami kekuatan sinyal keyword.
4. Membentuk indeks gabungan GSII.
5. Membuat fitur time series.
6. Melatih dan mengevaluasi model forecasting.
7. Mengubah hasil prediksi menjadi status peringatan dini.

Namun, untuk pengembangan berikutnya, hasil dapat diperkuat dengan:

- Menambahkan data wilayah spesifik Sulawesi Utara jika tersedia dari Google Trends regional.
- Menguji model setelah XGBoost dan LightGBM terinstall.
- Menambahkan metode validasi time series seperti walk-forward validation.
- Menggabungkan data pendukung, misalnya berita GDELT atau data penanganan konten negatif.
- Meninjau ulang ambang batas 20% dan 40% bersama domain expert.
