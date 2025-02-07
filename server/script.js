const outputWindow = document.querySelector(".window-console");
const button = document.querySelector(".my-button");

button.addEventListener("click", () => {
  const textInput = document.querySelector("input").value;
  const styleInput = document.querySelector("select").value;

  if (textInput !== "") {
    const span = document.createElement("span");
    span.classList.add("typerio", styleInput);
    outputWindow.appendChild(span);

    let i = 0;
    function typeWriter() {
      if (i < textInput.length) {
        span.innerHTML += textInput.charAt(i);
        i++;
        setTimeout(typeWriter, 100);
      }
    }
    typeWriter();
  }
});
