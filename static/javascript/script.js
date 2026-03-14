



 
 document.addEventListener("DOMContentLoaded", function(){

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');

const savedImage = localStorage.getItem('uploadedImage');

if(savedImage){
  uploadArea.innerHTML = `<img src="${savedImage}">`;
}

uploadArea.addEventListener('click',()=>{
  fileInput.click();
});

fileInput.addEventListener('change',function(){

  const file = this.files[0];
  if(!file) return;

  const reader = new FileReader();

  reader.onload = function(e){
    uploadArea.innerHTML = `<img src="${e.target.result}">`;
    localStorage.setItem("uploadedImage", e.target.result);
  }

  reader.readAsDataURL(file);

});

});


   const editor = document.getElementById("editor");

    // Load saved content from localStorage
    if (localStorage.getItem("savedContent")) {
      editor.innerHTML = localStorage.getItem("savedContent");
    }

    editor.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault(); // stop Enter from adding a new line
        const confirmSave = confirm("Do you want to save the changes?");
        if (confirmSave) {
          const content = editor.innerHTML;
          localStorage.setItem("savedContent", content); // save to browser
          alert("Changes saved!");
        } else {
          editor.innerHTML = localStorage.getItem("savedContent") || "This is editable text. Press Enter to save.";
          alert("Changes discarded.");
        }
      }
    });

    document.addEventListener("DOMContentLoaded", function(){
    const logoBox = document.getElementById("logoBox");
    const logoInput = document.getElementById("logoInput");
    const text = document.getElementById("text");

    // Load saved logo
    const savedLogo = localStorage.getItem("siteLogo");
    if (savedLogo) {
      logoBox.innerHTML = `<img src="${savedLogo}">`;
    }

    // Click box → open file dialog
    logoBox.addEventListener("click", () => {
      logoInput.click();
    });

    // Upload logo
    logoInput.addEventListener("change", function () {
      const file = this.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function (e) {
        logoBox.innerHTML = `<img src="${e.target.result}">`;
        localStorage.setItem("siteLogo", e.target.result);
      };
      reader.readAsDataURL(file);
    });

    });