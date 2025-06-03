document.addEventListener('DOMContentLoaded', function () {
    const runRateChart = document.getElementById('runRateChart');
    if (runRateChart) {
        const ctx = runRateChart.getContext('2d');
        const data = JSON.parse(runRateChart.dataset.graphData || '[]');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => `Over ${item.over}`),
                datasets: [{
                    label: 'Runs per Over',
                    data: data.map(item => item.runs),
                    borderColor: '#1a3c34',
                    backgroundColor: 'rgba(26, 60, 52, 0.2)',
                    fill: true,
                    tension: 0.4,
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Overs', font: { size: 14 } }
                    },
                    y: {
                        title: { display: true, text: 'Runs', font: { size: 14 } },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: { display: true, position: 'top' }
                }
            }
        });
    }
});