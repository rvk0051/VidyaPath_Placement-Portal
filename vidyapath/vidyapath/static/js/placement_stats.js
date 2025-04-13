

// Global chart instance
let companyChart;

// Fetch Data and Initialize Chart
document.addEventListener("DOMContentLoaded", function () {
    fetchDataAndRenderChart(); // Load chart with default values
});

// Fetch Placement Stats Data
function fetchDataAndRenderChart(company = null, branch = null) {
    let url = `/get_chart_data/?company=${company || ''}&branch=${branch || ''}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);
            populateCompanyFilter(data);
            populateBranchFilter(data);
            updateChart(data.company_placement_data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Populate Company Filter Dropdown
function populateCompanyFilter(data) {
    let companyFilter = document.getElementById('companyFilter');
    companyFilter.innerHTML = '';

    data.companies.forEach(company => {
        let option = new Option(company, company);
        companyFilter.add(option);
    });
    companyFilter.value = data.selected_company;
}

// Populate Branch Filter Dropdown
function populateBranchFilter(data) {
    let branchFilter = document.getElementById('branchFilter');
    branchFilter.innerHTML = '';  // Clear previous options to avoid duplicates

    // Add "All Branches" as the first option
    let allBranchesOption = new Option("All Branches", "All Branches");
    branchFilter.add(allBranchesOption);

    // Add actual branches from the data
    data.branches.forEach(branch => {
        if (branch !== "All Branches") {  // Avoid duplicate "All Branches"
            let option = new Option(branch, branch);
            branchFilter.add(option);
        }
    });

    // Set the default selected branch to "All Branches"
    branchFilter.value = data.selected_branch || "All Branches";
}

// Apply Filters (Triggered by Button Click)// Apply Filters (Triggered by Button Click)
function applyFilter() {
    let selected_company = document.getElementById('companyFilter').value;
    let selected_branch = document.getElementById('branchFilter').value;

    // If "All Branches" is selected, send an empty string to the backend
    selected_branch = (selected_branch === "All Branches") ? "" : selected_branch;

    console.log(`Applying Filter - Company: ${selected_company}, Branch: ${selected_branch}`);
    fetchDataAndRenderChart(selected_company, selected_branch);
}

// Update Chart
function updateChart(data) {
    console.log("📊 Updating Chart with:", data);

    if (companyChart) companyChart.destroy(); // Destroy old chart if exists

    const ctx = document.getElementById('companyPlacementsChart').getContext('2d');

    if (data.length === 0) {
        console.warn(" No data available for the selected company.");
        return;
    }

    companyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.placement_year),
            datasets: [{
                label: 'Students Placed',
                data: data.map(item => item.students_placed),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: { 
            responsive: true, 
            animation: { duration: 1000 }, 
            scales: { 
                y: { 
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1, // Forces Y-axis to show only whole numbers
                        callback: function(value, index, values) {
                            return Number.isInteger(value) ? value : ''; // Show only whole numbers
                        }
                    }
                } 
            } 
        }
    });
}

// Fetch Salary Data & Populate Chart
// Fetch Salary Data & Populate Chart
function fetchSalaryDistribution(branch = '', year = '') {
    let url = `/get_salary_distribution/?branch=${branch}&year=${year}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (!data.salary_distribution || data.salary_distribution.length === 0) {
                console.warn("No salary data available.");
                return;
            }

            // ✅ Fix: Populate filters and update selected values
            populateSalaryFilters(data.branches, data.years, branch, year);  
            drawSalaryChart(data.salary_distribution, data.total_placed_students);
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Populate Filters & Set Selected Value
function populateSalaryFilters(branches, years, selectedBranch, selectedYear) {
    let branchFilter = document.getElementById("salaryBranchFilter");
    let yearFilter = document.getElementById("salaryYearFilter");

    // Clear existing options
    branchFilter.innerHTML = '<option value="">All</option>';
    yearFilter.innerHTML = '<option value="">All</option>';

    // Add Branch Options
    branches.forEach(branch => {
        let option = new Option(branch, branch);
        branchFilter.add(option);
    });

    // Add Year Options
    years.forEach(year => {
        let option = new Option(year, year);
        yearFilter.add(option);
    });

    // ✅ Fix: Set selected values after populating options
    if (selectedBranch) branchFilter.value = selectedBranch;
    if (selectedYear) yearFilter.value = selectedYear;
}

// Apply Salary Filters
function applySalaryFilter() {
    let selectedBranch = document.getElementById('salaryBranchFilter').value;
    let selectedYear = document.getElementById('salaryYearFilter').value;

    console.log(`Applying Salary Filter - Branch: ${selectedBranch}, Year: ${selectedYear}`);
    fetchSalaryDistribution(selectedBranch, selectedYear);
}

// Draw Salary Pie Chart (Only Non-Empty Ranges)
function drawSalaryChart(data, totalPlacedStudents) {
    // ✅ Filter out empty salary ranges
    let filteredData = data.filter(item => item.students_count > 0);

    let labels = filteredData.map(item => item.salary_range);
    let values = filteredData.map(item => item.students_count);

    let ctx = document.getElementById("salaryChart").getContext("2d");

    // Destroy previous instance if exists
    if (window.salaryChartInstance) {
        window.salaryChartInstance.destroy();
    }

    // ✅ Create Pie Chart only with non-empty salary ranges
    window.salaryChartInstance = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Number of Students",
                data: values,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
                borderColor: "#fff",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                tooltip: { enabled: true },
                title: {
                    display: true,
                    text: `Salary Distribution (Total Placed Students: ${totalPlacedStudents})`,
                    font: { size: 16 }
                }
            }
        }
    });
}

// Initialize on Page Load
document.addEventListener("DOMContentLoaded", function () {
    fetchSalaryDistribution();  // Load default chart
});


function displayTopAchievers(achievers) {
    const carouselInner = document.querySelector('.carousel-inner');
    carouselInner.innerHTML = "";

    achievers.forEach((achiever, index) => {
        const div = document.createElement('div');
        div.classList.add('carousel-item');
        if (index === 0) div.classList.add('active');

        // Decode URL and ensure it's absolute
        const photoUrl = decodeURIComponent(achiever.photo);
        
        div.innerHTML = `
            <img src="${photoUrl}" class="achiever-img" alt="${achiever.student_name}">
            <div class="carousel-caption d-none d-md-block">
                <h5>${achiever.student_name} - ${achiever.year}</h5>
                <p>${achiever.company} | ${achiever.salary_lpa} LPA</p>
            </div>
        `;
        carouselInner.appendChild(div);
    });

    // Initialize the carousel after adding items
    const carousel = new bootstrap.Carousel(document.querySelector('#achieversCarousel'));
}

// Fetch Data from API
fetch('/get_top_achievers')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayTopAchievers(data.top_achievers);
    });
