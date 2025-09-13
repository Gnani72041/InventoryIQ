# 📊 InventoryIQ – Sales Forecasting Web Application

**InventoryIQ** is a Django-based web application that leverages **Machine Learning** to forecast product sales and optimize inventory management. It provides an intuitive dashboard for users to make **data-driven business decisions**.

---

## 🚀 Features
- 🔐 User Authentication (Sign up, Login, Dashboard)  
- 📦 Inventory & Sales Data Management  
- 🤖 Sales Forecasting using ML models (scikit-learn)  
- 🎨 Responsive UI with Bootstrap 5 & Crispy Forms  
- ☁️ Deployed on **Azure App Service**  

---

## 🛠️ Tech Stack
- **Backend:** Django 5, Python 3.12  
- **Frontend:** Bootstrap 5, Django Templates, Crispy Forms  
- **Database:** SQLite (dev), PostgreSQL/MySQL (production ready)  
- **ML Libraries:** scikit-learn, pandas, numpy  
- **Deployment:** Azure App Service (Linux, Gunicorn, Whitenoise)  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Gnani72041/InventoryIQ.git
cd InventoryIQ/inventory-forecaster

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt


### 3️⃣ Setup Environment Variables
SECRET_KEY=your_secret_key_here
DEBUG=True


### 4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate


### 5️⃣ Run the Development Server
python manage.py runserver


