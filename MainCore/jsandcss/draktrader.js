'use strict';







const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
}





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


document.addEventListener('DOMContentLoaded', function() {
  let cachedStockPrices = {};
  const cacheExpirationTime = 60 * 1000; // 1 minute in milliseconds

  // Function to fetch and display stock prices
  function fetchStockPrices() {
    fetch('http://127.0.0.1:5000/api/stock-prices') // Modify the URL to match your server's API endpoint
      .then(response => response.json())
      .then(data => {
        if (data.prices) {
          updateStockPrices(data.prices);
          cachedStockPrices = data.prices; // Update cached prices
        } else {
          console.error('Stock price data not available yet');
        }
      })
      .catch(error => {
        console.error('Error fetching stock prices:', error);
      });
  }

  // Function to check if cached stock prices are still valid
  function isCacheValid() {
    return Object.keys(cachedStockPrices).length > 0 && (Date.now() - cachedStockPrices.timestamp) < cacheExpirationTime;
  }

  // Function to update stock prices on the webpage
  function updateStockPrices(prices) {
    for (const [stockName, price] of Object.entries(prices)) {
      const stockPriceContainer = document.getElementById(`stock-price-${stockName.replace(':', '-').toLowerCase()}`);
      if (stockPriceContainer) {
        stockPriceContainer.innerText = `${stockName}: ${price}`;
      }
    }
  }

  // Function to periodically update stock prices
  function updateStockPricesPeriodically() {
    if (!isCacheValid()) {
      // If cached stock prices are not valid or not available, fetch new stock prices
      fetchStockPrices();
    } else {
      // If cached stock prices are still valid, update the stock prices on the webpage
      updateStockPrices(cachedStockPrices);
    }
  }

  // Call updateStockPricesPeriodically function initially
  updateStockPricesPeriodically();

  // Set an interval to update stock prices periodically
  setInterval(updateStockPricesPeriodically, 20000); // 20 seconds interval
});








