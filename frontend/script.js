/* Global Constants */
const API_BASE_URL = 'http://localhost:5000/api';
let sampleData = [];

/* Initialize on Page Load */
document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    initializeDashboard();
});

/* Tab Navigation */
function setupTabNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Remove active class from all
            navBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            document.getElementById(tabName).classList.add('active');

            // Load tab-specific content
            if (tabName === 'analytics') loadAnalyticsData();
            if (tabName === 'samples') loadSampleData();
        });
    });
}

/* Check Model Status */
async function checkModelStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        const statusDot = document.getElementById('model-status');
        const statusText = document.getElementById('status-text');

        if (data.model_loaded) {
            statusDot.className = 'status-dot active';
            statusText.textContent = 'Model Ready';
        } else {
            statusDot.className = 'status-dot loading';
            statusText.textContent = 'Model Loading...';
        }
    } catch (error) {
        document.getElementById('model-status').className = 'status-dot error';
        document.getElementById('status-text').textContent = 'Model Unavailable';
        console.error('Error checking model status:', error);
    }
}

/* Initialize Dashboard */
async function initializeDashboard() {
    checkModelStatus();
    await loadDashboardData();
    setInterval(checkModelStatus, 5000); // Check every 5 seconds
}

/* Load Dashboard Data */
async function loadDashboardData() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const stats = await response.json();

        // Update stat cards
        document.getElementById('stat-total').textContent = stats.total_customers || '-';
        document.getElementById('stat-churn').textContent = stats.churn_customers || '-';
        document.getElementById('stat-rate').textContent = 
            (stats.churn_rate * 100).toFixed(1) + '%' || '-';
        
        if (stats.model_metrics && stats.model_metrics.accuracy) {
            document.getElementById('stat-accuracy').textContent = 
                (stats.model_metrics.accuracy * 100).toFixed(1) + '%';
        }

        // Create charts
        createChurnDistributionChart(stats);
        createMetricsChart(stats);
        loadFeatureImportance();

    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

/* Create Churn Distribution Chart */
function createChurnDistributionChart(stats) {
    const churnCount = stats.churn_customers || 0;
    const retainCount = (stats.total_customers || 0) - churnCount;

    const data = [{
        labels: ['Churned', 'Retained'],
        values: [churnCount, retainCount],
        type: 'pie',
        marker: {
            colors: ['#ef4444', '#10b981']
        }
    }];

    const layout = {
        title: '',
        font: { family: 'Segoe UI' }
    };

    Plotly.newPlot('churn-pie', data, layout, { responsive: true, displayModeBar: false });
}

/* Create Model Metrics Chart */
function createMetricsChart(stats) {
    if (!stats.model_metrics) return;

    const metrics = stats.model_metrics;
    const data = [{
        x: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'],
        y: [
            metrics.accuracy || 0,
            metrics.precision || 0,
            metrics.recall || 0,
            metrics.f1 || 0,
            metrics.roc_auc || 0
        ],
        type: 'bar',
        marker: { color: '#2563eb' }
    }];

    const layout = {
        title: '',
        yaxis: { range: [0, 1], title: 'Score' },
        xaxis: { title: '' },
        font: { family: 'Segoe UI' }
    };

    Plotly.newPlot('metrics-bar', data, layout, { responsive: true, displayModeBar: false });
}

/* Load Feature Importance */
async function loadFeatureImportance() {
    try {
        const response = await fetch(`${API_BASE_URL}/feature-importance`);
        const data = await response.json();

        const features = data.features.slice(0, 10);
        const featureData = [{
            x: features.map(f => f.importance),
            y: features.map(f => f.name),
            type: 'bar',
            orientation: 'h',
            marker: { color: '#3b82f6' }
        }];

        const layout = {
            title: '',
            xaxis: { title: 'Importance' },
            yaxis: { automargin: true },
            font: { family: 'Segoe UI' },
            margin: { l: 150 }
        };

        Plotly.newPlot('feature-importance', featureData, layout, 
            { responsive: true, displayModeBar: false });

    } catch (error) {
        console.error('Error loading feature importance:', error);
    }
}

/* Predict Single Customer */
async function predictSingleCustomer() {
    try {
        const customerData = {
            Age: parseInt(document.getElementById('input-age').value),
            Tenure: parseInt(document.getElementById('input-tenure').value),
            Monthly_Charges: parseFloat(document.getElementById('input-monthly-charges').value),
            Total_Charges: parseFloat(document.getElementById('input-total-charges').value),
            Monthly_Usage_Hours: parseInt(document.getElementById('input-usage-hours').value),
            Customer_Support_Contacts: parseInt(document.getElementById('input-support-contacts').value),
            Contract_Type: document.getElementById('input-contract').value,
            Internet_Service: document.getElementById('input-internet').value,
            Payment_Method: document.getElementById('input-payment').value,
            Has_Tech_Support: document.getElementById('input-tech-support').value,
            Has_Online_Backup: document.getElementById('input-online-backup').value
        };

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(customerData)
        });

        const result = await response.json();

        // Show results
        const resultSection = document.getElementById('prediction-result');
        const riskValue = document.getElementById('result-risk-value');
        const recommendation = document.getElementById('result-recommendation');

        resultSection.classList.remove('hidden');

        if (result.churn_risk === 1) {
            riskValue.textContent = '⚠️ HIGH CHURN RISK';
            riskValue.className = 'result-risk-value high';
            recommendation.className = 'result-recommendation high';
            recommendation.innerHTML = `
                <strong>⚠️ Recommendation:</strong> This customer has a high risk of churning. 
                Consider implementing retention strategies such as:
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li>Personalized engagement campaigns</li>
                    <li>Special discounts or loyalty programs</li>
                    <li>Enhanced customer support</li>
                    <li>Service quality improvements</li>
                </ul>
            `;
        } else {
            riskValue.textContent = '✅ LOW CHURN RISK';
            riskValue.className = 'result-risk-value low';
            recommendation.className = 'result-recommendation low';
            recommendation.innerHTML = `
                <strong>✅ Recommendation:</strong> This customer appears satisfied and unlikely to churn. 
                Continue maintaining good service quality and consider cross-selling opportunities.
            `;
        }

        const churnProb = (result.churn_probability * 100).toFixed(1);
        const noChurnProb = (result.no_churn_probability * 100).toFixed(1);

        document.getElementById('result-churn-prob').textContent = churnProb + '%';
        document.getElementById('result-no-churn-prob').textContent = noChurnProb + '%';

        // Create probability visualization
        createProbabilityGauge(result.churn_probability);

    } catch (error) {
        alert('Error making prediction: ' + error.message);
        console.error(error);
    }
}

/* Create Probability Gauge */
function createProbabilityGauge(probability) {
    const canvas = document.getElementById('probability-gauge');
    const ctx = canvas.getContext('2d');

    // Set canvas size
    canvas.width = 300;
    canvas.height = 150;

    // Draw gauge
    const x = canvas.width / 2;
    const y = canvas.height - 20;
    const radius = 80;

    // Background arc
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 20;
    ctx.beginPath();
    ctx.arc(x, y, radius, Math.PI, 2 * Math.PI);
    ctx.stroke();

    // Colored arc based on probability
    const angle = Math.PI + (probability * Math.PI);
    const color = probability > 0.5 ? '#ef4444' : probability > 0.3 ? '#f59e0b' : '#10b981';

    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, Math.PI, angle);
    ctx.stroke();

    // Text
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 24px Segoe UI';
    ctx.textAlign = 'center';
    ctx.fillText(Math.round(probability * 100) + '%', x, y - 30);

    ctx.fillStyle = '#64748b';
    ctx.font = '14px Segoe UI';
    ctx.fillText('Churn Probability', x, y + 40);
}

/* Load Analytics Data */
async function loadAnalyticsData() {
    try {
        const response = await fetch(`${API_BASE_URL}/sample-data`);
        const data = await response.json();
        sampleData = data.samples;

        // Create distribution charts
        createAgeDistributionChart(data.samples);
        createTenureDistributionChart(data.samples);
        createChargesDistributionChart(data.samples);
        createContractImpactChart(data.samples);
        generateInsights(data.samples);

    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

/* Create Age Distribution Chart */
function createAgeDistributionChart(samples) {
    const churned = samples.filter(s => s.Churn === 1);
    const retained = samples.filter(s => s.Churn === 0);

    const data = [
        {
            x: retained.map(s => s.Age),
            name: 'Retained',
            type: 'histogram',
            marker: { color: '#10b981' },
            opacity: 0.7
        },
        {
            x: churned.map(s => s.Age),
            name: 'Churned',
            type: 'histogram',
            marker: { color: '#ef4444' },
            opacity: 0.7
        }
    ];

    const layout = {
        title: '',
        xaxis: { title: 'Age' },
        yaxis: { title: 'Count' },
        font: { family: 'Segoe UI' },
        barmode: 'overlay'
    };

    Plotly.newPlot('age-distribution', data, layout, { responsive: true, displayModeBar: false });
}

/* Create Tenure Distribution Chart */
function createTenureDistributionChart(samples) {
    const churned = samples.filter(s => s.Churn === 1);
    const retained = samples.filter(s => s.Churn === 0);

    const data = [
        {
            x: retained.map(s => s.Tenure),
            name: 'Retained',
            type: 'histogram',
            marker: { color: '#10b981' },
            opacity: 0.7
        },
        {
            x: churned.map(s => s.Tenure),
            name: 'Churned',
            type: 'histogram',
            marker: { color: '#ef4444' },
            opacity: 0.7
        }
    ];

    const layout = {
        title: '',
        xaxis: { title: 'Tenure (months)' },
        yaxis: { title: 'Count' },
        font: { family: 'Segoe UI' },
        barmode: 'overlay'
    };

    Plotly.newPlot('tenure-distribution', data, layout, { responsive: true, displayModeBar: false });
}

/* Create Charges Distribution Chart */
function createChargesDistributionChart(samples) {
    const churned = samples.filter(s => s.Churn === 1);
    const retained = samples.filter(s => s.Churn === 0);

    const data = [
        {
            x: retained.map(s => s.Monthly_Charges),
            name: 'Retained',
            type: 'histogram',
            marker: { color: '#10b981' },
            opacity: 0.7
        },
        {
            x: churned.map(s => s.Monthly_Charges),
            name: 'Churned',
            type: 'histogram',
            marker: { color: '#ef4444' },
            opacity: 0.7
        }
    ];

    const layout = {
        title: '',
        xaxis: { title: 'Monthly Charges ($)' },
        yaxis: { title: 'Count' },
        font: { family: 'Segoe UI' },
        barmode: 'overlay'
    };

    Plotly.newPlot('charges-distribution', data, layout, { responsive: true, displayModeBar: false });
}

/* Create Contract Impact Chart */
function createContractImpactChart(samples) {
    const contracts = ['Month-to-month', 'One year', 'Two year'];
    const churnRates = contracts.map(contract => {
        const filtered = samples.filter(s => s.Contract_Type === contract);
        return filtered.length > 0 ? filtered.filter(s => s.Churn === 1).length / filtered.length : 0;
    });

    const data = [{
        x: contracts,
        y: churnRates.map(r => r * 100),
        type: 'bar',
        marker: { color: '#3b82f6' }
    }];

    const layout = {
        title: '',
        xaxis: { title: 'Contract Type' },
        yaxis: { title: 'Churn Rate (%)' },
        font: { family: 'Segoe UI' }
    };

    Plotly.newPlot('contract-impact', data, layout, { responsive: true, displayModeBar: false });
}

/* Generate Insights */
function generateInsights(samples) {
    const insights = [];

    // Calculate various metrics
    const avgAgeCchurned = samples.filter(s => s.Churn === 1).reduce((sum, s) => sum + s.Age, 0) / 
                           (samples.filter(s => s.Churn === 1).length || 1);
    const avgAgeRetained = samples.filter(s => s.Churn === 0).reduce((sum, s) => sum + s.Age, 0) / 
                           (samples.filter(s => s.Churn === 0).length || 1);

    insights.push(`Churned customers average age (${avgAgeCchurned.toFixed(1)}) is ${
        avgAgeCchurned > avgAgeRetained ? 'higher' : 'lower'} than retained customers (${avgAgeRetained.toFixed(1)})`);

    // Tenure insights
    const avgTenureCchurned = samples.filter(s => s.Churn === 1).reduce((sum, s) => sum + s.Tenure, 0) / 
                              (samples.filter(s => s.Churn === 1).length || 1);
    insights.push(`Customers with lower tenure are more likely to churn (avg: ${avgTenureCchurned.toFixed(1)} months)`);

    // Contract type insights
    const monthToMonth = samples.filter(s => s.Contract_Type === 'Month-to-month');
    const monthToMonthChurnRate = monthToMonth.filter(s => s.Churn === 1).length / (monthToMonth.length || 1);
    insights.push(`Month-to-month contracts have a ${(monthToMonthChurnRate * 100).toFixed(1)}% churn rate`);

    // Tech support insights
    const withSupport = samples.filter(s => s.Has_Tech_Support === 'Yes');
    const supportChurnRate = withSupport.filter(s => s.Churn === 1).length / (withSupport.length || 1);
    insights.push(`Customers with tech support have a ${(supportChurnRate * 100).toFixed(1)}% churn rate`);

    // Display insights
    const insightsList = document.getElementById('insights-list');
    insightsList.innerHTML = insights.map(insight => `<li>${insight}</li>`).join('');
}

/* Load Sample Data */
async function loadSampleData() {
    try {
        const response = await fetch(`${API_BASE_URL}/sample-data`);
        const data = await response.json();

        const header = document.getElementById('table-header');
        const body = document.getElementById('table-body');

        // Clear existing content
        header.innerHTML = '';
        body.innerHTML = '';

        if (data.samples.length === 0) return;

        // Create header
        const headerRow = Object.keys(data.samples[0]);
        headerRow.forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            header.appendChild(th);
        });

        // Create rows
        data.samples.forEach(sample => {
            const tr = document.createElement('tr');
            headerRow.forEach(key => {
                const td = document.createElement('td');
                const value = sample[key];
                if (key === 'Churn') {
                    td.textContent = value === 1 ? '⚠️ Churned' : '✅ Retained';
                    td.style.fontWeight = 'bold';
                } else {
                    td.textContent = typeof value === 'number' ? value.toFixed(2) : value;
                }
                tr.appendChild(td);
            });
            body.appendChild(tr);
        });

    } catch (error) {
        console.error('Error loading sample data:', error);
    }
}
