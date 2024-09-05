const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");
inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});
toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
    main.classList.toggle("sign-in-mode");
    images.forEach((img) => img.classList.toggle("show"));
  });
});
function moveSlider() {
  let index = this.dataset.value;

  images.forEach((img) => img.classList.remove("show"));
  document.querySelector(`.img-${index}`).classList.add("show");

  const textSlider = document.querySelector(".text-group");
  textSlider.style.transform = `translateY(${-(index - 1) * 100}%)`;

  bullets.forEach((bull) => bull.classList.remove("active"));
  this.classList.add("active");
}
bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});

// this will be here login logical code


