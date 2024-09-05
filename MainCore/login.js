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


document.addEventListener('DOMContentLoaded', () => {
    const signInForm = document.querySelector('.sign-in-form');
    const signUpForm = document.querySelector('.sign-up-form');

   // Function to handle form submission for sign-in
signInForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(signInForm);
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });

    console.log('Sign In Form Data:', formDataObject); // Log form data

    try {
        const response = await fetch('http://127.0.0.1:5007/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataObject)
        });

        if (response.ok) {
            const data = await response.json();

            if (data.success) {

                window.location.href = 'draktrader.html';
            } else {

                alert(data.message);
            }
        } else {

            alert('Failed to log in. Please try again later.');
        }
    } catch (error) {
        console.error('Error signing in:', error);

        alert('An error occurred while signing in. Please try again later.');
    }
});



    signUpForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(signUpForm);
        const formDataObject = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        console.log('Sign Up Form Data:', formDataObject); // Log form data

        try {
            const response = await fetch('http://127.0.0.1:5007/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formDataObject) // Send form data as JSON
            });

            if (response.ok) {
                const data = await response.json();
                // Redirect to the login page
                window.location.href = 'login.html'; // Replace 'login.html' with your actual login page
            } else {
                // Handle error response (e.g., display error message)
            }
        } catch (error) {
            console.error('Error signing up:', error);
            // Handle network or server error (e.g., display error message)
        }
    });
});


