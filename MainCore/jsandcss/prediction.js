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

document.getElementById('stockForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var stockName = document.getElementById('stockName').value;
    fetchStockDescription(stockName);
    fetchPlots(stockName);
});

function fetchStockDescription(stockName) {
    fetch('http://127.0.0.1:5004/get_stock_description', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({stock_name: stockName})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var descriptionHtml = '<h2>Dataset Summary</h2><table>';
            for (var key in data.description) {
                var value = data.description[key];
                descriptionHtml += '<tr><th>' + key + '</th>';
                for (var subKey in value) {
                    descriptionHtml += '<td>' + value[subKey] + '</td>';
                }
                descriptionHtml += '</tr>';
            }
            descriptionHtml += '</table>';
            document.getElementById('stockDescription').innerHTML = descriptionHtml;
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function fetchPlots(stockName) {
    fetch('http://127.0.0.1:5004/get_plots', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({stock_name: stockName})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Plotly.newPlot('candlestickPlot', JSON.parse(data.candlestick_plot));
            Plotly.newPlot('maPlot', JSON.parse(data.ma_plot));
            Plotly.newPlot('predictionVsRealPlot', JSON.parse(data.prediction_vs_real_plot));
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}