# Sistem Peringatan Dini Peningkatan Minat Pencarian Judi Online di Sulawesi Utara Menggunakan Data Mining

**Gloria Elisabeth Tandi Rondonguwu**<sup>1</sup>, **Miftahuddin S. Arsyad**<sup>2</sup>, **Brilliani Jeshia Potangil**<sup>3</sup>

<sup>1</sup>Fakultas Teknik, Universitas Sam Ratulangi, Manado, Kodepos, Indonesia, email: isi_email_ketua@domain.ac.id  
<sup>2</sup>Fakultas Teknik, Universitas Sam Ratulangi, Manado, Kodepos, Indonesia, email: isi_email_anggota1@domain.ac.id  
<sup>3</sup>Fakultas Teknik, Universitas Sam Ratulangi, Manado, Kodepos, Indonesia, email: isi_email_anggota2@domain.ac.id  

**Corresponding Author:** Gloria Elisabeth Tandi Rondonguwu

**Catatan footer template:** isi footer kiri dengan `Gloria Elisabeth Tandi Rondonguwu: Sistem Peringatan Dini...`

## INTISARI

Judi online merupakan salah satu isu sosial digital yang membutuhkan mekanisme pemantauan dan mitigasi dini berbasis data. Penelitian ini bertujuan mengembangkan sistem peringatan dini untuk memprediksi peningkatan minat pencarian terkait judi online di Sulawesi Utara menggunakan pendekatan data mining. Data yang digunakan berasal dari Google Trends dalam bentuk deret waktu bulanan dengan kata kunci terkait, yaitu `judi online`, `slot gacor`, `togel online`, `judi slot`, `situs judi`, `slot88`, `pragmatic play`, dan `gacor hari ini`. Tahapan penelitian meliputi pembersihan data, eksplorasi data, pembentukan Google Search Interest Index (GSII), rekayasa fitur time series, pemodelan forecasting, evaluasi model, dan penentuan status peringatan dini. GSII dibentuk dari rata-rata kata kunci utama `slot_gacor`, `judi_slot`, dan `judi_online`. Model yang dibandingkan meliputi baseline naive forecasting dan Random Forest Regressor, dengan dukungan opsional untuk XGBoost dan LightGBM. Berdasarkan eksperimen awal, model baseline naive memperoleh performa terbaik dengan MAE 4,79, RMSE 5,97, dan MAPE 64,02. Hasil prediksi terakhir menunjukkan status `Normal` karena prediksi GSII bulan berikutnya tidak mengalami peningkatan dibandingkan bulan saat ini. Sistem ini diharapkan dapat menjadi dasar pendukung pengambilan keputusan untuk pemantauan tren pencarian judi online dan penyusunan strategi literasi digital.

**KATA KUNCI** — Data Mining, Google Trends, Judi Online, Forecasting, Early Warning System, GSII, Random Forest.

## I. PENDAHULUAN

Perkembangan teknologi informasi memberikan kemudahan akses terhadap berbagai layanan digital, tetapi di sisi lain juga membuka ruang bagi meningkatnya aktivitas digital yang berisiko, salah satunya judi online. Fenomena ini tidak hanya berkaitan dengan aspek hukum, tetapi juga berdampak pada kondisi sosial, ekonomi, dan literasi digital masyarakat. Upaya pencegahan tidak cukup dilakukan secara reaktif setelah aktivitas bermasalah terjadi, melainkan perlu dilengkapi dengan sistem pemantauan yang mampu mendeteksi potensi peningkatan minat masyarakat secara lebih awal.

Salah satu sumber data yang dapat digunakan untuk membaca sinyal awal perilaku masyarakat adalah Google Trends. Data Google Trends merepresentasikan intensitas relatif pencarian suatu kata kunci dalam rentang waktu dan wilayah tertentu. Dalam konteks judi online, peningkatan pencarian terhadap kata kunci tertentu dapat menjadi indikasi meningkatnya perhatian, rasa ingin tahu, atau eksposur masyarakat terhadap konten terkait judi online.

Penelitian ini berfokus pada pengembangan sistem peringatan dini peningkatan minat pencarian terkait judi online di Sulawesi Utara. Sistem dibangun menggunakan data deret waktu Google Trends dan pendekatan forecasting jangka pendek untuk memprediksi nilai indeks pencarian satu bulan ke depan. Hasil prediksi kemudian diterjemahkan menjadi status peringatan dini berdasarkan ambang kenaikan tertentu.

Rumusan masalah dalam penelitian ini adalah:

1. Bagaimana membentuk indeks gabungan minat pencarian judi online dari beberapa kata kunci Google Trends?
2. Bagaimana membangun fitur time series untuk memprediksi peningkatan indeks pencarian satu bulan ke depan?
3. Model forecasting apa yang memberikan performa terbaik pada data Google Trends yang digunakan?
4. Bagaimana menerjemahkan hasil prediksi menjadi status peringatan dini yang mudah dipahami?

Tujuan penelitian ini adalah menghasilkan pipeline data mining yang mampu membersihkan data Google Trends, membentuk Google Search Interest Index (GSII), melakukan forecasting jangka pendek, mengevaluasi model, serta menghasilkan status peringatan dini peningkatan minat pencarian judi online.

## II. METODE/INOVASI

### A. Data

Dataset yang digunakan adalah data Google Trends dalam format CSV dengan rentang waktu bulanan dari Desember 2019 sampai Desember 2025. Dataset terdiri dari 73 baris dan 9 kolom, yaitu satu kolom tanggal dan delapan kolom kata kunci. Kata kunci yang dianalisis meliputi:

- `judi_online`
- `slot_gacor`
- `togel_online`
- `judi_slot`
- `situs_judi`
- `slot88`
- `pragmatic_play`
- `gacor_hari_ini`

### B. Pra-pemrosesan Data

Pra-pemrosesan dilakukan untuk memastikan data dapat digunakan dalam analisis time series. Tahapan pra-pemrosesan meliputi:

1. Membaca file CSV menggunakan `pandas`.
2. Mendeteksi kemungkinan metadata pada file Google Trends.
3. Membersihkan nama kolom agar sesuai format Python.
4. Mengubah kolom tanggal menjadi tipe `datetime`.
5. Mengubah seluruh nilai kata kunci menjadi numerik.
6. Mengubah nilai khusus seperti `<1` menjadi `0`.
7. Mengurutkan data berdasarkan tanggal.

### C. Exploratory Data Analysis

Exploratory Data Analysis (EDA) dilakukan untuk memahami karakteristik sinyal setiap kata kunci. Statistik yang dihitung meliputi rata-rata, median, standar deviasi, nilai maksimum, dan jumlah nilai bukan nol. Jumlah nilai bukan nol digunakan untuk melihat kekuatan sinyal awal dari setiap kata kunci.

### D. Pembentukan Google Search Interest Index

Penelitian ini membentuk indeks gabungan bernama Google Search Interest Index (GSII). GSII digunakan sebagai representasi agregat minat pencarian judi online. Rumus awal yang digunakan adalah:

```text
GSII = rata-rata(slot_gacor, judi_slot, judi_online)
```

Pemilihan ketiga kata kunci tersebut didasarkan pada relevansi topik dan eksplorasi awal terhadap kekuatan sinyal. Jika salah satu kolom tidak tersedia, pipeline secara otomatis menyesuaikan dengan kolom yang tersedia.

### E. Rekayasa Fitur Time Series

Target forecasting adalah memprediksi GSII satu bulan ke depan. Fitur yang digunakan adalah:

- `lag_1`
- `lag_2`
- `lag_3`
- `rolling_mean_3`
- `rolling_std_3`
- `month`
- `year`

Target prediksi didefinisikan sebagai:

```text
target_next_month = GSII.shift(-1)
```

Data kemudian dibagi menggunakan time-based split, yaitu 80% data awal sebagai data latih dan 20% data terakhir sebagai data uji.

### F. Model Forecasting

Model yang digunakan dalam eksperimen awal adalah:

1. Baseline naive forecasting, yaitu prediksi bulan depan sama dengan nilai GSII bulan saat ini.
2. Random Forest Regressor.

Pipeline juga disiapkan untuk mendukung XGBoost Regressor dan LightGBM Regressor apabila library telah terpasang. Evaluasi model dilakukan menggunakan metrik Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), dan Mean Absolute Percentage Error (MAPE).

### G. Aturan Peringatan Dini

Hasil prediksi diterjemahkan ke dalam status peringatan dini menggunakan aturan berikut:

- Jika prediksi GSII bulan depan naik minimal 40% dari bulan saat ini, status `Tinggi`.
- Jika prediksi GSII bulan depan naik minimal 20% dari bulan saat ini, status `Waspada`.
- Jika prediksi naik tetapi kurang dari 20%, status `Perhatian`.
- Jika prediksi tidak naik, status `Normal`.

## III. HASIL DAN DISKUSI

### A. Hasil Statistik Kata Kunci

Hasil EDA menunjukkan bahwa `slot_gacor` merupakan kata kunci dengan sinyal paling kuat. Keyword ini memiliki rata-rata 8,48, nilai maksimum 100, dan 46 nilai bukan nol dari 73 observasi. Kata kunci `judi_slot` memiliki 26 nilai bukan nol, sedangkan `judi_online` memiliki 16 nilai bukan nol. Kedua kata kunci tersebut tetap digunakan dalam pembentukan GSII karena relevan dengan topik utama penelitian.

**[TEMPATKAN GAMBAR 1 DI SINI]**  
File gambar: `outputs/figures/keyword_trends_all.png`  
Caption yang dipakai: **Gambar 1. Tren interest over time seluruh kata kunci.**  
Alasan penempatan: gambar ini memperlihatkan pola umum pencarian sebelum tabel statistik keyword dibahas lebih detail.

Tabel I menunjukkan ringkasan statistik kata kunci.

**TABEL I**  
**Ringkasan Statistik Kata Kunci Google Trends**

| Keyword | Mean | Median | Std | Max | Non-zero Count | Rekomendasi Model |
|---|---:|---:|---:|---:|---:|---|
| `slot_gacor` | 8,48 | 1,00 | 20,55 | 100 | 46 | Ya |
| `judi_slot` | 0,88 | 0,00 | 1,70 | 8 | 26 | Ya |
| `slot88` | 0,25 | 0,00 | 0,43 | 1 | 18 | Ya |
| `judi_online` | 0,32 | 0,00 | 0,66 | 3 | 16 | Ya |
| `situs_judi` | 0,38 | 0,00 | 0,98 | 4 | 11 | Ya |
| `gacor_hari_ini` | 0,22 | 0,00 | 0,98 | 8 | 9 | Ya |
| `togel_online` | 0,11 | 0,00 | 0,49 | 3 | 4 | Tidak |
| `pragmatic_play` | 0,01 | 0,00 | 0,12 | 1 | 1 | Tidak |

Kata kunci `togel_online` dan `pragmatic_play` memiliki jumlah nilai bukan nol yang rendah, sehingga tetap dianalisis dalam EDA tetapi tidak diprioritaskan dalam model utama.

### B. Hasil Pembentukan GSII

GSII berhasil dibentuk dari rata-rata `slot_gacor`, `judi_slot`, dan `judi_online`. Indeks ini digunakan sebagai target utama sistem forecasting. Penggunaan indeks gabungan bertujuan mengurangi ketergantungan pada satu kata kunci dan menangkap sinyal pencarian secara lebih representatif.

**[TEMPATKAN GAMBAR 2 DI SINI]**  
File gambar: `outputs/figures/keyword_correlation_heatmap.png`  
Caption yang dipakai: **Gambar 2. Heatmap korelasi antar kata kunci.**  
Alasan penempatan: gambar ini mendukung penjelasan bahwa beberapa keyword memiliki hubungan sinyal sehingga layak dipertimbangkan dalam indeks gabungan.

### C. Hasil Evaluasi Model

Tabel II menunjukkan hasil evaluasi model pada data uji.

**TABEL II**  
**Perbandingan Evaluasi Model Forecasting**

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Baseline Naive | 4,79 | 5,97 | 64,02 |
| Random Forest | 13,15 | 16,76 | 78,22 |

Berdasarkan RMSE, model terbaik pada eksperimen awal adalah baseline naive forecasting. Hasil ini menunjukkan bahwa pada dataset yang relatif kecil dan memiliki banyak nilai rendah atau nol, model sederhana dapat menghasilkan performa lebih stabil dibandingkan model yang lebih kompleks seperti Random Forest.

### D. Visualisasi Prediksi

Grafik aktual versus prediksi telah disimpan untuk setiap model. Grafik model terbaik disimpan pada:

`outputs/figures/best_model_actual_vs_prediction.png`

**[TEMPATKAN GAMBAR 3 DI SINI]**  
File gambar: `outputs/figures/best_model_actual_vs_prediction.png`  
Caption yang dipakai: **Gambar 3. Perbandingan nilai aktual dan prediksi GSII pada model terbaik.**  
Alasan penempatan: gambar ini memperlihatkan performa prediksi model terbaik secara visual setelah tabel evaluasi model dibahas.

Visualisasi ini digunakan untuk melihat kedekatan pola prediksi terhadap nilai aktual GSII bulan berikutnya.

### E. Hasil Peringatan Dini

Berdasarkan data terakhir, sistem menghasilkan status sebagai berikut:

**TABEL III**  
**Status Peringatan Dini**

| Tanggal Saat Ini | Tanggal Prediksi | Model | GSII Saat Ini | Prediksi GSII Bulan Depan | Perubahan | Status |
|---|---|---|---:|---:|---:|---|
| 2025-12-01 | 2026-01-01 | Baseline Naive | 1,00 | 1,00 | 0,00% | Normal |

Hasil tersebut menunjukkan bahwa prediksi GSII bulan berikutnya tidak mengalami peningkatan dibandingkan GSII bulan saat ini. Oleh karena itu, status peringatan dini yang dihasilkan adalah `Normal`.

## IV. KESIMPULAN

Penelitian ini berhasil membangun pipeline data mining untuk sistem peringatan dini peningkatan minat pencarian judi online menggunakan data Google Trends. Pipeline mencakup proses pembersihan data, EDA, pembentukan GSII, rekayasa fitur time series, pemodelan forecasting, evaluasi model, visualisasi hasil, dan penentuan status peringatan dini.

Hasil eksperimen awal menunjukkan bahwa `slot_gacor` merupakan kata kunci dengan sinyal paling kuat. GSII dibentuk menggunakan `slot_gacor`, `judi_slot`, dan `judi_online`. Model baseline naive forecasting memperoleh hasil terbaik dengan MAE 4,79, RMSE 5,97, dan MAPE 64,02. Berdasarkan prediksi terakhir, sistem memberikan status `Normal` karena tidak terdapat peningkatan GSII bulan berikutnya.

Pengembangan berikutnya dapat dilakukan dengan menambahkan data Google Trends regional yang lebih spesifik, menguji XGBoost dan LightGBM, menerapkan walk-forward validation, serta menggabungkan data pendukung seperti berita daring atau data penanganan konten negatif.

## REFERENSI

[1] Google, "Google Trends," [Online]. Tersedia: https://trends.google.com/. Tanggal akses: 15-Jun-2026.

[2] H. Choi dan H. Varian, "Predicting the Present with Google Trends," Economic Record, Vol. 88, No. s1, hal. 2-9, 2012, doi: 10.1111/j.1475-4932.2012.00809.x.

[3] R. West, "Calibration of Google Trends Time Series," Proc. ACM International Conference on Information and Knowledge Management, 2020, doi: 10.1145/3340531.3412094.

[4] J. Ginsberg, M. H. Mohebbi, R. S. Patel, L. Brammer, M. S. Smolinski, dan L. Brilliant, "Detecting Influenza Epidemics Using Search Engine Query Data," Nature, Vol. 457, hal. 1012-1014, 2009, doi: 10.1038/nature07634.

[5] A. Mavragani dan G. Ochoa, "Google Trends in Infodemiology and Infoveillance: Methodology Framework," JMIR Public Health and Surveillance, Vol. 5, No. 2, 2019, doi: 10.2196/13439.

[6] R. J. Hyndman dan G. Athanasopoulos, Forecasting: Principles and Practice, 3rd ed. Melbourne, Australia: OTexts, 2021. [Online]. Tersedia: https://otexts.com/fpp3/. Tanggal akses: 15-Jun-2026.

[7] L. Breiman, "Random Forests," Machine Learning, Vol. 45, No. 1, hal. 5-32, 2001, doi: 10.1023/A:1010933404324.

[8] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," Journal of Machine Learning Research, Vol. 12, hal. 2825-2830, 2011.

[9] T. Chen dan C. Guestrin, "XGBoost: A Scalable Tree Boosting System," Proc. 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, hal. 785-794, 2016, doi: 10.1145/2939672.2939785.

[10] G. Ke et al., "LightGBM: A Highly Efficient Gradient Boosting Decision Tree," Advances in Neural Information Processing Systems, Vol. 30, 2017.

[11] W. McKinney, "Data Structures for Statistical Computing in Python," Proc. 9th Python in Science Conference, hal. 56-61, 2010, doi: 10.25080/Majora-92bf1922-00a.

[12] C. R. Harris et al., "Array Programming with NumPy," Nature, Vol. 585, hal. 357-362, 2020, doi: 10.1038/s41586-020-2649-2.

[13] J. D. Hunter, "Matplotlib: A 2D Graphics Environment," Computing in Science & Engineering, Vol. 9, No. 3, hal. 90-95, 2007, doi: 10.1109/MCSE.2007.55.

[14] M. L. Waskom, "Seaborn: Statistical Data Visualization," Journal of Open Source Software, Vol. 6, No. 60, 3021, 2021, doi: 10.21105/joss.03021.

[15] Republik Indonesia, Undang-Undang Nomor 1 Tahun 2024 tentang Perubahan Kedua atas Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik, 2024. [Online]. Tersedia: https://peraturan.bpk.go.id/. Tanggal akses: 15-Jun-2026.
