# 🐾 Pet Shop – Full-Stack Web Application for Online Pet Sales  

Welcome to **Pet Shop**, a complete full-stack web application for selling pets online.  
This project is designed to give customers a smooth shopping experience with **user authentication, pet browsing, order placement, and admin management**.  
Built using **FastAPI + SQLite** with a clean frontend powered by **HTML, CSS, and Jinja2**, this project is perfect for demonstrating practical e-commerce workflows.  

---

## 🔍 Project Overview  

**Pet Shop enables customers to:**  
- Browse available pets by category  
- Register/login as a user to place orders  
- Enter delivery details and confirm purchase  
- Track order history in their dashboard  

**Admin users can:**  
- Login to a secure admin dashboard  
- Add new pets with image upload and price  
- View and manage customer orders  
- Manage registered users  

---

## 🚀 Key Features  

### 🔐 User Authentication  
- Sign up, log in, and log out  
- Secure session handling  
- Separate dashboards for **Users** & **Admins**  

### 🐕 Dynamic Pet Listing  
- Upload pets with category, price & image  
- Pets displayed dynamically on homepage  
- Browse pets easily with clean card layout  

### 📦 Order Placement  
- Place order with delivery details (Name, Address, City, Pincode, State, Country)  
- Order stored in database and shown in dashboard  
- Confirmation page after placing order  

### 👤 User Dashboard  
- View order history  
- See personal purchase records  

### 🛠️ Admin Dashboard  
- Add or remove pets  
- Manage all orders  
- Manage registered users  

### 🖼️ Image Uploads  
- Upload pet images and serve from `/static/images/`  
- Display dynamically in templates  

---

## 🛠️ Tech Stack  

| Layer         | Technology |
|---------------|------------|
| **Backend**   | FastAPI (Python) |
| **Database**  | SQLite (SQLAlchemy ORM) |
| **Frontend**  | HTML5, CSS3, Jinja2 Templates |
| **Server**    | Uvicorn |
| **Version Control** | Git, GitHub |

---

## ⚙️ How to Run Locally  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/petshop.git
cd petshop
2️⃣ Create and activate virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run migrations (creates SQLite DB & tables)
bash
Copy code
# The app auto-creates DB tables on first run
5️⃣ Start development server
bash
Copy code
uvicorn main:app --reload
6️⃣ Access the app
👉 Open browser: http://127.0.0.1:8000/

📁 Folder Structure
csharp
Copy code
petshop/
│── main.py              # Main FastAPI app with routes
│── templates/           # Jinja2 HTML templates
│   │── petshop.html
│   │── login.html
│   │── signup.html
│   │── admin_dashboard.html
│   │── user_dashboard.html
│   │── order.html
│   │── order_success.html
│── static/              # Static files (CSS, JS, Images)
│   │── style.css
│   │── images/
│── petshop.db           # SQLite database
│── requirements.txt     # Python dependencies
│── README.md            # Documentation
