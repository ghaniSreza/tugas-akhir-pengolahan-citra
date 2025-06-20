import os
import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_glcm_features(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Tidak bisa baca gambar")

        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        gray = cv2.resize(gray, (300, 300))

        # Konversi ke uint8 (0-255)
        gray = (gray / gray.max()) * 255
        gray = gray.astype(np.uint8)

        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        glcm = graycomatrix(gray, [1], angles, levels=256, symmetric=True, normed=True)

        features = []
        for i in range(len(angles)):
            features.extend([
                graycoprops(glcm, 'contrast')[0, i],
                graycoprops(glcm, 'dissimilarity')[0, i],
                graycoprops(glcm, 'homogeneity')[0, i],
                graycoprops(glcm, 'energy')[0, i],
                graycoprops(glcm, 'correlation')[0, i],
                graycoprops(glcm, 'ASM')[0, i]
            ])
        return np.array(features)

    except Exception as e:
        print(f"GLCM error: {e}")
        return None


def load_dataset():
    dataset_path = 'dataset'
    features, labels = [], []
    for class_name in ['Pneumonia', 'normal']:
        class_path = os.path.join(dataset_path, class_name)
        if not os.path.exists(class_path):
            continue
        for fname in os.listdir(class_path):
            if allowed_file(fname):
                path = os.path.join(class_path, fname)
                feat = extract_glcm_features(path)
                if feat is not None:
                    features.append(feat)
                    labels.append(class_name)
    return np.array(features), np.array(labels)