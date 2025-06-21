// Show image preview
function showPreview(input, previewId) {
  const file = input.files[0];
  const preview = document.getElementById(previewId);
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

// Image preview listeners
document.getElementById('encrypt-image').addEventListener('change', function () {
  showPreview(this, 'encrypt-preview');
});

document.getElementById('decrypt-image').addEventListener('change', function () {
  showPreview(this, 'decrypt-preview');
});

// Encrypt and Download
async function encrypt() {
  const image = document.getElementById('encrypt-image').files[0];
  const secret = document.getElementById('secret-text').value;
  const password = document.getElementById('encrypt-password').value;

  if (!image || !secret || !password) {
    alert("Please fill all fields.");
    return;
  }

  const formData = new FormData();
  formData.append("image", image);
  formData.append("secret", secret);
  formData.append("password", password);

  try {
    const response = await fetch('http://127.0.0.1:5000/encrypt', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      alert("Encryption failed: " + (err.error || "Unknown error"));
      return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    // Create a link to download the image
    const a = document.createElement('a');
    a.href = url;
    a.download = "encrypted_image.png";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  } catch (err) {
    alert("Error encrypting: " + err.message);
  }
}

// Decrypt
async function decrypt() {
  
  const image = document.getElementById('decrypt-image').files[0];
  const password = document.getElementById('decrypt-password').value;

  if (!image || !password) {
    alert("Please provide image and password.");
    return;
  }

  const formData = new FormData();
  formData.append("image", image);
  formData.append("password", password);

  try {
    const response = await fetch('http://127.0.0.1:5000/decrypt', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (response.ok) {
      document.getElementById('decrypted-message').innerText = result.message;
      console.log(result.message);
      
    } else {
      alert("Decryption failed: " + (result.error || "Unknown error"));
    }
  } catch (err) {
    alert("Error decrypting: " + err.message);
  }
}