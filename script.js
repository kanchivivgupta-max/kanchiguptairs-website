// ============================================
// script.js — Interactive features
// ============================================

// 1. Theme management (Dark Mode by Default)
const themeToggle = document.getElementById("theme-toggle");

// Initialize theme from storage, fallback to dark
const savedTheme = localStorage.getItem("theme") || "dark";
if (savedTheme === "light") {
  document.documentElement.classList.remove("dark");
  document.documentElement.classList.add("light");
  themeToggle.textContent = "🌙";
} else {
  document.documentElement.classList.add("dark");
  document.documentElement.classList.remove("light");
  themeToggle.textContent = "☀️";
}

themeToggle.addEventListener("click", () => {
  const isLight = document.documentElement.classList.toggle("light");
  if (isLight) {
    document.documentElement.classList.remove("dark");
    themeToggle.textContent = "🌙";
    localStorage.setItem("theme", "light");
  } else {
    document.documentElement.classList.add("dark");
    themeToggle.textContent = "☀️";
    localStorage.setItem("theme", "dark");
  }
});

// 2. Time-based greeting
const hour = new Date().getHours();
const greeting = document.getElementById("greeting");

if (greeting) {
  if (hour < 12) {
    greeting.textContent = "Good morning, I'm";
  } else if (hour < 18) {
    greeting.textContent = "Good afternoon, I'm";
  } else {
    greeting.textContent = "Good evening, I'm";
  }
}

// 3. Auto-updating copyright year in footer
const yearSpan = document.getElementById("year");
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear();
}
