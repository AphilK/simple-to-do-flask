// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const htmlElement = document.documentElement;
  
  // Check for saved theme preference or default to system preference
  const currentTheme = localStorage.getItem('theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  // Apply saved theme
  if (currentTheme === 'dark') {
    htmlElement.setAttribute('data-theme', 'dark');
    if (themeToggleBtn) themeToggleBtn.textContent = '☀️ Light';
  } else {
    htmlElement.removeAttribute('data-theme');
    if (themeToggleBtn) themeToggleBtn.textContent = '🌙 Dark';
  }
  
  // Toggle theme on button click
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function() {
      const isDark = htmlElement.getAttribute('data-theme') === 'dark';
      
      if (isDark) {
        htmlElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        themeToggleBtn.textContent = '🌙 Dark';
      } else {
        htmlElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeToggleBtn.textContent = '☀️ Light';
      }
    });
  }
  
  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    // Only apply if user hasn't set a preference
    if (!localStorage.getItem('theme')) {
      const isDark = e.matches;
      const htmlElement = document.documentElement;
      const themeToggleBtn = document.getElementById('theme-toggle');
      
      if (isDark) {
        htmlElement.setAttribute('data-theme', 'dark');
        if (themeToggleBtn) themeToggleBtn.textContent = '☀️ Light';
      } else {
        htmlElement.removeAttribute('data-theme');
        if (themeToggleBtn) themeToggleBtn.textContent = '🌙 Dark';
      }
    }
  });
});
