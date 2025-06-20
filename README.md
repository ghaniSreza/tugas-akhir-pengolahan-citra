## Proyek Dekripsi
Projek ini membuat web yang bisa klasifikasikan gambar rontgen dada secara otomatis. Sistem ini dirancang untuk mendeteksi penyakit pneumonia. Cara kerjanya adalah dengan menggunakan metode GLCM atau Gray Level Co-Occurrence Matrix untuk mengambil ciri-ciri tekstur dari gambar. Setelah itu, hasil ekstraksi fitur ini akan diolah oleh SVM atau Support Vector Machine untuk melakukan klasifikasi. Untuk UI sendiri dibuat dengan framework Flask. 

## install Virtual Environment
python -m venv .venv

## install library
pip install -r requirements.txt

## Dataset
dataset yang digunakan pada projek ini berasal dari kaggle dengan citra pneumonia sebanyak 1397 dan citra normal sebanyak 1341
berikut ini link kaggle nya https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia/data

# Menjalankan Aplikasi
 - jika belum ada model_svm.pkl (file ini merupakan model dari svm setelah dilakukan training) ketik "py training.py" di terminal
 - setelah di run dan dapet file model_svm.pkl, ketik "py app.py" untuk menjalankan server flask copy http://127.0.0.1:5000 di browser atau (ctrl+clik)


## 📋 Tahapan pada sistem sampai ke hasil

# Preprocess
1. Load Gambar
Bergunna untuk mengambil gambar dari folder dataset atau input user, tujuan nya supaya gambar bisa preprocess.
2. Konversi Grayscale 
Jika citra pada dataset berupa RGB maka akan dikonversi ke grayscale, tujuan nya karena GLCM hanya bekerja pada citra grayscale dan ber fokus pada intensitas, bukan warna. 
3. Resize
Gambar diubah ukurannya menjadi 300x300 menyamakan dimensi gambar agar proses ekstraksi fitur konsisten.
4. Ekstraksi Fitur dengan GLCM
GLCM menghitung nilai statistik tekstur pada fitur contrast, dissimilarity, homogeneity, energy, correlation, dan ASM, tujuan nya untuk mengubah citra menjadi representasi numerik yang bisa dibaca oleh SVM.
5. Scaling
Nilai fitur GLCM diubah agar memiliki distribusi standar (mean=0, std=1), tujuan nya supaya model SVM bekerja optimal (karena SVM sensitif terhadap skala data).

## Klasifikasi
Setelah preprocessing selesai, data dilatih menggunakan model SVM. Kami pilih SVM karena tingkat akurasi nya lebih tinggi dibandingkan KNN.

1. Split Data 
Dataset dibagi menjadi data training (80%) dan testing (20%).
2. Scaling  
Fitur training dan testing di-scale menggunakan StandardScaler.
3. Model Training 
Model SVM dengan kernel RBF dilatih menggunakan data training.
4. Evaluasi 
Model diuji dengan data testing untuk mengecek performa akurasi nya.
5. Simpan Model 
Model dan scaler disimpan (model_svm.pkl) agar bisa digunakan saat pengujian/prediksi.

## Proses Pengujian
Tahapan ini dilakukan saat user upload citra melalui web dan ingin tahu apakah itu pneumonia atau tidak.

# Alur Pengujian:
1. Upload Gambar.
2. Saat gambar di upload ke sistem, gambar bakal konversi ke grayscale, lalu resize ke 300x300, ekstraksi fitur GLCM, dan scaling fitur.
3. Fitur GLCM yang udah discaling dimasukkan ke model SVM untuk diklasifikasi dan menampilkan hasil bahwa gambar tersebut pneumonia atau normal.

