// Handling panel slide
const registerButton = document.getElementById("register");
const loginButton = document.getElementById("login");
const container = document.getElementById("container");

registerButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

loginButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

// Function to display error message
function displayError(elementId, errorMessage) {
  var errorElement = document.getElementById(elementId);
  errorElement.innerHTML = `<div class="error-message">${errorMessage}</div>`;
}

// Function to clear error message
function clearError(elementId) {
  var errorElement = document.getElementById(elementId);
  errorElement.innerHTML = '';
}

// Reload the page if an error exists
window.onload = function() {
  const registerError = document.getElementById("register-error");
  const loginError = document.getElementById("login-error");

  if (registerError.innerText || loginError.innerText) {
    location.reload();
  }
};
