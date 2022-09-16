const form = document.querySelector("form");
const fileInput = form.querySelector(".file-input");
const showNumfile = document.getElementById("showNumfile");
const btn = document.querySelector(".btn.btn-outline-secondary");
const button = document.querySelector(".submit-button");

function showMessage(number) {
  let textHtml = `
        <section class="uploaded-area">
        <li class="row">
          <div class="content">
            <i class="fas fa-file-alt"></i>
            <div class="details">
              <span class="name">Total file for processing</span>
              <span class="size">${number} files</span>
            </div>
          </div>
        </li>
      </section>
      
  `;
  showNumfile.innerHTML = textHtml;
}

form.addEventListener("click", () => {
  fileInput.click();
});

fileInput.onchange = ({ target }) => {
  lengthFile = target.files.length;
  showMessage(lengthFile);
};

btn.addEventListener("click", () => {
  button.click();
});

// return html alert number of files
