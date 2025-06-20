import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from joblib import dump
from utils import load_dataset

print("="*60)
print("Memuat dataset dan training model SVM...")
print("="*60)

# Load fitur dan juga label
X, y = load_dataset()

# menampilkan distribusi kelas
print("\n Distribusi Kelas:")
unique, counts = np.unique(y, return_counts=True)
for cls, count in zip(unique, counts):
    print(f"  - {cls}: {count} gambar")

# Cek jumlah data
if len(X) == 0:
    print("\n Dataset kosong atau tidak ditemukan.")
    exit()

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n Data berhasil displit:")
print(f"Jumlah training: {len(X_train)}")
print(f"Jumlah testing : {len(X_test)}")

# StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training SVM
print("\n Training model SVM...")
model = SVC(kernel='rbf', random_state=42, probability=True)
model.fit(X_train_scaled, y_train)

# Evaluasi
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)

print("\n Evaluasi Model:")
print(f"Akurasi  : {acc:.4f}")
print("\n Classification Report:")
print(classification_report(y_test, y_pred))

# Simpan model dan scaler
dump((model, scaler), "model_svm.pkl")
print("\n Model disimpan sebagai 'model_svm.pkl'")
print("="*60)