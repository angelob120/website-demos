'use strict';

/**
 * navbar toggle
 */

const header = document.querySelector("[data-header]");
const navToggleBtn = document.querySelector("[data-nav-toggle-btn]");
const navLinks = document.querySelectorAll("[data-navbar-link]");

navToggleBtn.addEventListener("click", function () {
  this.classList.toggle("active");
  header.classList.toggle("nav-active");
});

for (let i = 0; i < navLinks.length; i++) {
  navLinks[i].addEventListener("click", function () {
    header.classList.toggle("nav-active");
    navToggleBtn.classList.toggle("active");
  });
}



/**
 * header scroll active state & go to top
 */

const goTopBtn = document.querySelector("[data-go-top]");

window.addEventListener("scroll", function () {

  if (window.scrollY >= 100) {
    header.classList.add("active");
    goTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    goTopBtn.classList.remove("active");
  }

});



const getStartedBtn = document.querySelector('.btn.btn-primary[data-scroll-to]');

getStartedBtn.addEventListener('click', (e) => {
  e.preventDefault();

  const target = document.querySelector(getStartedBtn.getAttribute('data-scroll-to'));
  if (target) {
    target.scrollIntoView({
      behavior: 'smooth',
    });
  }
});




// Get the target section element
const targetSection = document.querySelector('#features');

// Wait for the DOM content to load
document.addEventListener("DOMContentLoaded", () => {
  // Get the "Get Started Now" button by its class name
  const getStartedButton = document.querySelector(".btn.btn-primary[data-scroll-to='#booking-section']");

  // Get the target section by its ID
  const targetSection = document.querySelector("#features");

  // Function to scroll to the target section smoothly
  const scrollToSection = () => {
    targetSection.scrollIntoView({ behavior: "smooth" });
  };

  // Add a click event listener to the button
  getStartedButton.addEventListener("click", scrollToSection);
});




// JavaScript function to scroll to the target section
function scrollToSection(target) {
  const section = document.querySelector(target);
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' });
  }
}