




'use strict';



/**
 * add event on element
 */



const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
}



/**
 * navbar toggle
 */

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");

const toggleNavbar = function () {
  navbar.classList.toggle("active");
  navToggler.classList.toggle("active");
  document.body.classList.toggle("active");
}

addEventOnElem(navToggler, "click", toggleNavbar);

const closeNavbar = function () {
  navbar.classList.remove("active");
  navToggler.classList.remove("active");
  document.body.classList.remove("active");
}

addEventOnElem(navbarLinks, "click", closeNavbar);



/**
 * header active
 */

const header = document.querySelector("[data-header]");

const activeHeader = function () {
  if (window.scrollY > 300) {
    header.classList.add("active");
  } else {
    header.classList.remove("active");
  }
}

addEventOnElem(window, "scroll", activeHeader);



/**
 * toggle active on add to fav
 */

const addToFavBtns = document.querySelectorAll("[data-add-to-fav]");

const toggleActive = function () {
  this.classList.toggle("active");
}

addEventOnElem(addToFavBtns, "click", toggleActive);



/**
 * scroll revreal effect
 */

const sections = document.querySelectorAll("[data-section]");

const scrollReveal = function () {
  for (let i = 0; i < sections.length; i++) {
    if (sections[i].getBoundingClientRect().top < window.innerHeight / 1.5) {
      sections[i].classList.add("active");
    } else {
      sections[i].classList.remove("active");
    }
  }
}

scrollReveal();



addEventOnElem(window, "scroll", scrollReveal);

// Function to upload strategy code
async function uploadStrategy() {
  try {
      const strategyCode = editor.getValue();
      const stockName = document.getElementById('stockName').value;

      console.log('Strategy code:', strategyCode);
      console.log('Stock name:', stockName);

      // Send strategy code and stock name to server
      const response = await fetch('http://127.0.0.1:5002/upload', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ strategyCode, stockName })
      });

      const data = await response.json();
      console.log('Server response:', data); // Log server response
  } catch (error) {
      console.error('Error uploading strategy:', error);
  }
}

// Function to generate plot
async function generatePlot() {
  try {
      const stockName = document.getElementById('stockName').value;

      console.log('Generating plot for stock:', stockName);

      // Send stock name to server to generate plot
      const response = await fetch('http://127.0.0.1:5002/upload?stockName=' + stockName, {
          method: 'GET'
      });

      const data = await response.json();
      console.log('Chart data:', data.chart);

      // Display the plot received from the server
      const plotDiv = document.getElementById('plotContainer');
      Plotly.newPlot(plotDiv, JSON.parse(data.chart), {}, {responsive: true});
  } catch (error) {
      console.error('Error generating plot:', error);
  }
}



