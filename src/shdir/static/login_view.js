const passwordInput = document.getElementById("access-code");
const toggleButton = document.querySelector(".toggle-password");

toggleButton?.addEventListener("click", () => {
  const isPassword = passwordInput.type === "password";

  passwordInput.type = isPassword ? "text" : "password";
  toggleButton.setAttribute("aria-pressed", String(isPassword));
  toggleButton.setAttribute("aria-label", isPassword ? "Hide access code" : "Show access code");
});

