let currentTicker = 'BTC';

// Function to toggle sidebar visibility and shift content
function toggleSidebar() {
    document.body.classList.toggle('sidebar-open');
}

// Load the saved theme from localStorage on page load
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.classList.add(savedTheme);
        document.getElementById('mode-toggle').textContent = savedTheme === 'dark-mode' ? '🌞' : '🌙';
    }
}

// Toggle between light and dark mode and save it to localStorage
document.getElementById('mode-toggle').addEventListener('click', function () {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    const theme = isDarkMode ? 'dark-mode' : 'light-mode';
    
    // Ensure only one theme is applied
    document.body.classList.remove(isDarkMode ? 'light-mode' : 'dark-mode');
    
    // Save the theme in localStorage
    localStorage.setItem('theme', theme);

    // Update the button icon
    this.textContent = isDarkMode ? '🌞' : '🌙';
});

// Load the chart when the page loads
function loadChart(ticker) {
    currentTicker = ticker;
    updateChart();
}

// Fetch chart data and update the chart and price display
function updateChart() {
    const period = document.getElementById('period').value;
    const interval = document.getElementById('interval').value;

    fetch(`/chart?ticker=${currentTicker}&period=${period}&interval=${interval}`)
        .then(response => response.json())
        .then(data => {
            const chartElement = document.getElementById('chart');
            Plotly.react(chartElement, JSON.parse(data.chart).data, JSON.parse(data.chart).layout);

            // Update the price below the chart
            document.getElementById('price-display').textContent = `Current Price: $${data.price}`;
        });
}

// Initial page load: load the saved theme and chart
window.onload = function() {
    loadTheme();  // Load saved theme on page load
    loadChart(currentTicker);  // Load initial chart
}
