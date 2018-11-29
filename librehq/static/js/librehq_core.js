document.addEventListener(
  "DOMContentLoaded",
  () => {
    // Display the name of files that are being uploaded.
    const fileInputs = document.querySelectorAll(".file-input");
    fileInputs.forEach(input => {
      input.onchange = event => {
        const input = event.target;
        if (input.files.length > 0) {
          const label = input.parentElement;
          const fileDiv = label.parentElement;
          const fileName =
            label.querySelector(".file-name") || document.createElement("span");

          fileDiv.classList.add("has-name");
          fileName.innerText = input.files[0].name;

          if (!fileName.classList.contains("file-name")) {
            fileName.className = "file-name";
            label.appendChild(fileName);
          }
        }
      };
    });
  },
  false
);
