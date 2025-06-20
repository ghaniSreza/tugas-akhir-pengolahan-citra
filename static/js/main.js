document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.getElementById('fileInput');
  const uploadSection = document.getElementById('uploadSection');
  const fileInfo = document.getElementById('fileInfo');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const previewImage = document.getElementById('previewImage');
  const predictBtn = document.getElementById('predictBtn');
  const loading = document.getElementById('loading');

  fileInput.addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (file) {
      handleFile(file);
    }
  });

  uploadSection.addEventListener('dragover', function (e) {
    e.preventDefault();
    uploadSection.classList.add('drag-over');
  });

  uploadSection.addEventListener('dragleave', function (e) {
    e.preventDefault();
    uploadSection.classList.remove('drag-over');
  });

  uploadSection.addEventListener('drop', function (e) {
    e.preventDefault();
    uploadSection.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        fileInput.files = files;
        handleFile(file);
      } else {
        alert('Harap pilih file gambar yang valid!');
      }
    }
  });

  function handleFile(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';

    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
      previewImage.style.display = 'block';
    };
    reader.readAsDataURL(file);

    predictBtn.disabled = false;
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  const form = document.querySelector('form');
  form.addEventListener('submit', function () {
    loading.style.display = 'block';
    predictBtn.disabled = true;
    predictBtn.textContent = 'Menganalisis...';
  });
});
