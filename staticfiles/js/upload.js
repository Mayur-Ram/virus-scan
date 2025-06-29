document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const progressBar = document.getElementById("progressBar");
  const progressContainer = document.getElementById("progressBarContainer");
  const loader = document.getElementById("loader");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const file = document.getElementById("fileInput").files[0];
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/scan/", true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    // Show loader and progress bar
    progressContainer.style.display = "block";
    loader.classList.remove("hidden");

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percent = (event.loaded / event.total) * 100;
        progressBar.style.width = percent + "%";
      }
    };

    xhr.onload = () => {
      // Delay the display of result between 5s to 8s
      const delay = Math.floor(Math.random() * 3000) + 5000;

      setTimeout(() => {
        loader.classList.add("hidden");
        if (xhr.status === 200) {
          document.body.innerHTML = xhr.responseText;
        } else {
          alert("Scan failed.");
        }
      }, delay);
    };

    xhr.onerror = () => {
      loader.classList.add("hidden");
      alert("An error occurred during file upload.");
    };

    xhr.send(formData);
  });
});
