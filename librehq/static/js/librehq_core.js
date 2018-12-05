document.addEventListener(
  "DOMContentLoaded",
  () => {
    // For toggling nav menu on phones, from Bulma docs:
    // https://bulma.io/documentation/components/navbar/
    const $navbarBurgers = Array.prototype.slice.call(
      document.querySelectorAll(".navbar-burger"),
      0
    );
    if ($navbarBurgers.length > 0) {
      $navbarBurgers.forEach(el => {
        el.addEventListener("click", () => {
          const target = el.dataset.target;
          const $target = document.getElementById(target);
          el.classList.toggle("is-active");
          $target.classList.toggle("is-active");
        });
      });
    }

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
