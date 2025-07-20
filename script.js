document.addEventListener('DOMContentLoaded', () => {

    const donorForm = document.getElementById('donor-form');
    const requestForm = document.getElementById('request-form');
    const adminLoginForm = document.getElementById('admin-login-form');
    const adminDashboard = document.getElementById('admin-dashboard');
    const loginSection = document.getElementById('login-section');

    const ADMIN_PASSWORD = 'admin123';

    // --- Utility Functions ---
    const getFromStorage = (key) => JSON.parse(localStorage.getItem(key)) || [];
    const saveToStorage = (key, data) => localStorage.setItem(key, JSON.stringify(data));

    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast-notification');
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        setTimeout(() => { toast.className = 'toast'; }, 3000);
    }

    // --- Donor Registration Form ---
    if (donorForm) {
        donorForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const newDonor = {
                name: document.getElementById('name').value,
                bloodGroup: document.getElementById('blood-group').value,
                contact: document.getElementById('contact').value,
            };
            const donors = getFromStorage('donors');
            donors.push(newDonor);
            saveToStorage('donors', donors);
            showToast('Donor registered successfully!');
            donorForm.reset();
        });
    }

    // --- Blood Request Form ---
    if (requestForm) {
        requestForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const newRequest = {
                patientName: document.getElementById('patient-name').value,
                bloodGroup: document.getElementById('request-blood-group').value,
                contactInfo: document.getElementById('contact-info').value,
            };
            const requests = getFromStorage('requests');
            requests.push(newRequest);
            saveToStorage('requests', requests);
            showToast('Blood request submitted successfully.');
            requestForm.reset();
        });
    }

    // --- Admin Page Logic ---
    function populateTable(tableId, data, fields) {
        const tableBody = document.querySelector(`#${tableId} tbody`);
        tableBody.innerHTML = '';
        if (data.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="${fields.length}" style="text-align:center;">No entries found.</td></tr>`;
            return;
        }
        data.forEach(item => {
            const row = document.createElement('tr');
            fields.forEach(field => {
                const cell = document.createElement('td');
                cell.textContent = item[field];
                row.appendChild(cell);
            });
            tableBody.appendChild(row);
        });
    }

    function showDashboard() {
        loginSection.style.display = 'none';
        adminDashboard.classList.remove('hidden');

        // Populate both tables
        populateTable('donors-table', getFromStorage('donors'), ['name', 'bloodGroup', 'contact']);
        populateTable('requests-table', getFromStorage('requests'), ['patientName', 'bloodGroup', 'contactInfo']);
        
        // Tab functionality
        const tabs = document.querySelector('.tabs');
        const tabContents = document.querySelectorAll('.tab-content');
        tabs.addEventListener('click', (e) => {
            if (e.target.classList.contains('tab-button')) {
                // Deactivate all
                document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Activate clicked
                e.target.classList.add('active');
                document.getElementById(`${e.target.dataset.tab}-content`).classList.add('active');
            }
        });
    }

    if (adminDashboard) {
        // Check login status on page load
        if (sessionStorage.getItem('isAdminLoggedIn') === 'true') {
            showDashboard();
        }

        // Handle Admin Login
        adminLoginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (document.getElementById('password').value === ADMIN_PASSWORD) {
                sessionStorage.setItem('isAdminLoggedIn', 'true');
                showDashboard();
            } else {
                showToast('Incorrect password.', 'error');
            }
        });

        // Handle Logout
        document.getElementById('logout-button').addEventListener('click', () => {
            sessionStorage.removeItem('isAdminLoggedIn');
            window.location.reload(); // Easiest way to reset the view
        });
    }
});