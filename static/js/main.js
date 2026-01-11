// Fonction pour créer un graphique en anneau (doughnut)
function createDoughnutChart(elementId) {
    const chartElement = document.getElementById(elementId);
    if (chartElement) {
        const labels = JSON.parse(chartElement.dataset.labels);
        const data = {
            labels: labels,
            datasets: [{
                data: JSON.parse(chartElement.dataset.data),
                backgroundColor: JSON.parse(chartElement.dataset.colors)
            }]
        };
        new Chart(chartElement.getContext('2d'), {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }
}

// Fonction pour créer un graphique à barres
function createBarChart(elementId) {
    const chartElement = document.getElementById(elementId);
    if (chartElement) {
        const data = {
            labels: JSON.parse(chartElement.dataset.labels),
            datasets: [{
                label: 'Nombre de ventes',
                data: JSON.parse(chartElement.dataset.data),
                backgroundColor: '#007bff'
            }]
        };
        new Chart(chartElement.getContext('2d'), {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    createDoughnutChart('opportunitiesChart');
    createBarChart('servicesChart');
    createBarChart('categoriesChart');
});