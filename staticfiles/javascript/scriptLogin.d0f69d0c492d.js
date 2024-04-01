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

// Handling form submission using JavaScript
document.getElementById("register-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent default form submission

  // Get form data
  const formData = new FormData(this);

  // Perform client-side validation
  const username = formData.get('username');
  const email = formData.get('email');
  const password1 = formData.get('password1');
  const password2 = formData.get('password2');

  if (!username || !email || !password1 || !password2) {
      document.getElementById('register-error').innerText = 'Please fill all missing blanks.';
      return; // Stop further processing
  }

  if (password1 !== password2) {
      document.getElementById('register-error').innerText = 'Password must match its confirmation.';
      return; // Stop further processing
  }

  // Perform AJAX request to submit the form data
  // You can use fetch or XMLHttpRequest to send the form data to the server
});

document.getElementById("login-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent default form submission

  // Get form data
  const formData = new FormData(this);

  // Perform client-side validation
  const usernameOrEmail = formData.get('username_or_email');
  const password = formData.get('password');

  if (!usernameOrEmail || !password) {
      document.getElementById('login-error').innerText = 'Username or password is missing.';
      return; // Stop further processing
  }

  // Perform AJAX request to submit the form data
  // You can use fetch or XMLHttpRequest to send the form data to the server
});


// // Function to display error message
// function displayError(elementId, errorMessage) {
//   var errorElement = document.getElementById(elementId);
//   errorElement.innerHTML = `<div class="error-message">${errorMessage}</div>`;
// }

// // Function to clear error message
// function clearError(elementId) {
//   var errorElement = document.getElementById(elementId);
//   errorElement.innerHTML = '';
// }

// // Reload the page if an error exists
// window.onload = function() {
//   const registerError = document.getElementById("register-error");
//   const loginError = document.getElementById("login-error");

//   if (registerError.innerText || loginError.innerText) {
//     location.reload();
//   }
// };
