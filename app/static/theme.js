// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const htmlElement = document.documentElement;
  
  console.log('Theme script loaded');
  console.log('Button found:', themeToggleBtn);
  
  // Check for saved theme preference or default to system preference
  const currentTheme = localStorage.getItem('theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  console.log('Current theme:', currentTheme);
  
  // Apply saved theme
  if (currentTheme === 'dark') {
    htmlElement.setAttribute('data-theme', 'dark');
    if (themeToggleBtn) themeToggleBtn.textContent = 'Light';
  } else {
    htmlElement.removeAttribute('data-theme');
    if (themeToggleBtn) themeToggleBtn.textContent = 'Dark';
  }
  
  // Toggle theme on button click
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function(e) {
      console.log('Button clicked!');
      e.preventDefault();
      
      const isDark = htmlElement.getAttribute('data-theme') === 'dark';
      console.log('Is dark now:', isDark);
      
      if (isDark) {
        htmlElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        themeToggleBtn.textContent = 'Dark';
        console.log('Switched to light mode');
      } else {
        htmlElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeToggleBtn.textContent = 'Light';
        console.log('Switched to dark mode');
      }
    });
  } else {
    console.error('Theme toggle button not found!');
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
        if (themeToggleBtn) themeToggleBtn.textContent = 'Light';
      } else {
        htmlElement.removeAttribute('data-theme');
        if (themeToggleBtn) themeToggleBtn.textContent = 'Dark';
      }
    }
  });
});
