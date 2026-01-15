🩸 LifeFlow – Blood Bank Management System

LifeFlow is a full-stack Blood Bank Management System designed to streamline the process of blood donation, hospital coordination, and patient blood requests. The system offers a secure and user-friendly platform for donors, patients, hospitals, and administrators.

This project is developed using **Flask (Python)** for the backend, **SQLite** for the database, and **HTML, CSS, and JavaScript** for the frontend.

---

🚀 Features

👤 User Module

* User registration and login
* Donor registration form
* Blood request submission
* Patient and hospital request handling
* User dashboard
* Simple and intuitive UI

🛠️ Admin Module

* Secure admin login
* Admin dashboard
* Manage all users
* View and manage donors
* View patient and hospital requests
* Publish and manage notices
* System monitoring

💾 Database Integration

* SQLite database
* Stores:

  * User data
  * Donor details
  * Blood requests
  * Hospital requests
  * Admin notices

🎨 UI/UX

* Clean and modern design
* Responsive layout
* Easy navigation
* Mobile-friendly interface

---

🧑‍💻 Tech Stack

| Technology | Purpose       |
| ---------- | ------------- |
| Python     | Backend       |
| Flask      | Web framework |
| SQLite     | Database      |
| HTML       | Structure     |
| CSS        | Styling       |
| JavaScript | Interactivity |

---

📂 Project Structure

```
Blood_Bank_Management/
│
├── app.py                     
├── bloodbank.db               
├── README.md                  
│
├── static/
│   ├── style.css              
│   ├── script.js              
│   ├── hosp_1.jpg
│   ├── hosp_2.jpg
│   ├── hosp_3.jpg
│   ├── hosp_4.jpg
│   ├── hosp_5.jpg
│   └── hosp_6.jpg
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── user_dashboard.html
│   ├── admin_dashboard.html
│   ├── admin_notices.html
│   ├── donor_form.html
│   ├── donors.html
│   ├── patient_request_form.html
│   ├── hospital_request_form.html
│   ├── hospital_requests.html
│   ├── requests.html
│   ├── users.html
│   └── request_type.html
```

---

⚙️ How to Run the Project Locally

Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/Blood_Bank_Management.git
```

Step 2: Navigate to Project Folder

```bash
cd Blood_Bank_Management
```

Step 3: Install Dependencies

```bash
pip install flask
```

Step 4: Run the Application

```bash
python app.py
```

Step 5: Open in Browser

```
http://127.0.0.1:5000/
```

---

🔐 Admin Access

Admins can log in using the credentials stored in the database or configured in the backend. The admin panel provides full access to system data and management tools.

---

🎯 Project Objective

The aim of this project is to:

* Demonstrate full-stack development
* Implement role-based dashboards
* Integrate a relational database
* Simulate real-world blood bank operations
* Improve healthcare service accessibility

---

📸 Screenshots

(Add screenshots here)

---

🧾 Future Enhancements

* Email & SMS notifications
* OTP-based authentication
* Blood stock tracking
* API integration
* Analytics dashboard
* Mobile app version

---

🤝 Contribution

Contributions are welcome! Fork the repository, raise issues, or submit pull requests.

---

📜 License

This project is developed for educational purposes.
