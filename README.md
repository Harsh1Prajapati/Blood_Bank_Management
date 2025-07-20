# Blood_Bank_Management

LifeFlow: A Simple Blood Bank Management System
A lightweight, frontend-only web application for managing a local blood bank. Built entirely with HTML, CSS, and JavaScript, it provides a clean and modern interface for registering donors and handling blood requests. This project serves as an excellent example of building a functional application without a backend by using browser localStorage to simulate a database.

✨ Features
Modern UI/UX: A beautiful "glassmorphism" design with smooth animations and transitions for an attractive user experience.

Donor Registration: A simple and intuitive form for users to register as blood donors.

Blood Request System: A dedicated form for patients or hospitals to submit urgent blood requests.

Password-Protected Admin Panel: A secure dashboard for administrators to view and manage data.

Tabbed Interface: The admin panel features organized tabs to easily switch between viewing registered donors and submitted blood requests.

Local Data Persistence: Uses browser localStorage to save all data, so information persists even after closing the browser.

Fully Responsive: The interface works seamlessly on both desktop and mobile devices.

🖥️ How to Run Locally
Since this is a frontend-only project, running it is very simple.

Download all the project files (index.html, request.html, admin.html, style.css, script.js) and place them in a single folder.

Open the index.html file in any modern web browser (like Google Chrome, Mozilla Firefox, or Microsoft Edge).

That's it! The application is now running locally on your machine.

🔑 Admin Access
To access the admin panel and view the lists of donors and requests:

Navigate to the Admin Panel link.

Enter the password: admin123

📁 Folder Structure
The project uses a simple and flat file structure for ease of use.

blood-bank-project/

├── index.html         (Donor Registration Page)

├── request.html       (Blood Request Page)

├── admin.html         (Admin Panel)

├── style.css          (All Styles and Animations)

└── script.js          (All Application Logic)

⚠️ Important Limitation
This project uses localStorage, which means all data (donors and requests) is stored locally within your specific web browser. It is a simulation of a full-stack application and the data cannot be accessed from another computer or a different browser. The "user" and the "admin" must be using the same browser on the same machine to see the data.
