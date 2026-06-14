# Panduan Penempatan Gambar Makalah GEMASTIK

Dokumen ini menandai gambar mana yang perlu dimasukkan ke makalah dan diletakkan di bagian mana.

## Gambar Wajib Dimasukkan

### Gambar 1 - Tren Semua Keyword

File:

`outputs/figures/keyword_trends_all.png`

Letakkan di:

`III. HASIL DAN DISKUSI` -> `A. Hasil Statistik Kata Kunci`

Posisi paling pas:

Setelah paragraf yang menjelaskan bahwa `slot_gacor` adalah keyword dengan sinyal paling kuat, sebelum `Tabel I`.

Caption:

**Gambar 1. Tren interest over time seluruh kata kunci.**

Alasan:

Gambar ini menunjukkan pola umum semua keyword dari waktu ke waktu. Ini cocok muncul sebelum tabel statistik karena pembaca bisa melihat dulu tren visualnya.

## Gambar 2 - Heatmap Korelasi Keyword

File:

`outputs/figures/keyword_correlation_heatmap.png`

Letakkan di:

`III. HASIL DAN DISKUSI` -> `B. Hasil Pembentukan GSII`

Posisi paling pas:

Setelah paragraf yang menjelaskan GSII dibentuk dari rata-rata `slot_gacor`, `judi_slot`, dan `judi_online`.

Caption:

**Gambar 2. Heatmap korelasi antar kata kunci.**

Alasan:

Gambar ini mendukung pembahasan hubungan antar keyword. Cocok dipakai untuk memperkuat alasan bahwa keyword-keyword tersebut bisa dianalisis bersama.

## Gambar 3 - Aktual vs Prediksi Model Terbaik

File:

`outputs/figures/best_model_actual_vs_prediction.png`

Letakkan di:

`III. HASIL DAN DISKUSI` -> `D. Visualisasi Prediksi`

Posisi paling pas:

Setelah `Tabel II` evaluasi model dan setelah paragraf yang menyatakan model terbaik adalah `Baseline Naive`.

Caption:

**Gambar 3. Perbandingan nilai aktual dan prediksi GSII pada model terbaik.**

Alasan:

Gambar ini memperlihatkan hasil forecasting secara visual, jadi cocok diletakkan setelah metrik evaluasi model.

## Gambar Opsional Jika Halaman Masih Cukup

### Gambar 4 - Tren Keyword Slot Gacor

File:

`outputs/figures/trend_slot_gacor.png`

Letakkan di:

`III. HASIL DAN DISKUSI` -> `A. Hasil Statistik Kata Kunci`

Caption:

**Gambar 4. Tren pencarian keyword slot_gacor sebagai sinyal dominan.**

Alasan:

Dipakai hanya jika ingin menonjolkan keyword paling kuat. Kalau halaman sudah penuh, gambar ini tidak wajib karena `keyword_trends_all.png` sudah mencakupnya.

## Gambar yang Tidak Perlu Dimasukkan ke Makalah Utama

Gambar berikut cukup disimpan sebagai output pendukung, tidak wajib masuk makalah 4-5 halaman:

- `outputs/figures/actual_vs_prediction_Baseline_Naive.png`
- `outputs/figures/actual_vs_prediction_Random_Forest.png`
- `outputs/figures/trend_judi_online.png`
- `outputs/figures/trend_judi_slot.png`
- `outputs/figures/trend_togel_online.png`
- `outputs/figures/trend_situs_judi.png`
- `outputs/figures/trend_slot88.png`
- `outputs/figures/trend_pragmatic_play.png`
- `outputs/figures/trend_gacor_hari_ini.png`

Alasannya: gambar-gambar tersebut terlalu detail untuk makalah utama dan bisa membuat halaman penuh. Jika diminta lampiran atau presentasi, gambar-gambar ini baru dimasukkan.

## Di Notebook Letaknya Di Mana?

Pada file:

`notebooks/google_trends_gsii_pipeline.ipynb`

Gambar-gambar muncul dari cell berikut:

- `Gambar 1`: Section **6. Visualisasi Tren Keyword**
- `Gambar 2`: Section **7. Heatmap Korelasi Antar Keyword**
- `Gambar 3`: Section **11. Visualisasi Aktual vs Prediksi**

Jika menjalankan notebook, gambar akan tampil langsung di bawah cell tersebut. Untuk makalah, pakai file PNG yang sudah tersimpan di `outputs/figures`, bukan screenshot dari notebook.

## Tips Memasukkan ke Template GEMASTIK

- Letakkan gambar di tengah halaman.
- Gunakan gambar dengan ukuran cukup besar agar label terbaca.
- Untuk gambar yang lebar seperti tren dan prediksi, boleh dibuat melintasi dua kolom jika template memungkinkan.
- Caption gambar diletakkan di bawah gambar.
- Jangan hanya menulis path file gambar di makalah final; path file hanya catatan untuk proses penyusunan.
