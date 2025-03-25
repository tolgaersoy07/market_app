
# 🛒 MarketApp – The New Way of Shopping Without Checkout

**MarketApp** is a modern e-market solution that allows users shopping in a physical market to create a cart and complete their payments through their mobile devices **without going to the checkout**.  
With its mobile-friendly interface and powerful backend architecture, it offers a seamless and fast shopping experience for both users and market managers.

"With MarketApp, customers add products to their cart while walking around the store, pay through the app, and leave the market without a receipt."

---

## 🎯 Project Purpose

To make traditional market shopping faster and contactless. While inside the store, users can:
- Scan barcodes to add products to their cart,
- Pay through the app without going to a physical checkout,
- Receive digital receipts,
- View their order history.

This provides time savings for users and reduces checkout congestion in markets.

---

## 🚀 Features

### 👥 User Panel
- JWT-based login/logout system (Access + Refresh Token)
- Product search, viewing, and barcode-based cart addition
- Mobile-friendly and fast user interface
- Cart management and payment processing
- Order history and transaction details

### 🛠️ Admin Panel
- Product CRUD operations (add, edit, delete)
- Monitoring and managing orders
- Viewing customer and sales data
- Managing withdrawal requests

---

## 🧪 Technologies Used

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Database:** MySQL
- **Authentication:** JWT (access + refresh token), device ID control
- **Mobile Support:** Responsive (mobile & tablet support)

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure database connection  
Create a database in MySQL and configure the connection in `db_info/db.sql`.

### 3. Run the application
```bash
python app.py
```
Open `http://localhost:5000` in your browser to start the project.

---

## 🔒 Security Features
- User and admin separation through token validation
- Encrypted refresh tokens
- Identity check before each request (`before_request`)
- Users can only access their own data

---

## 🔄 API Request Flow
- This diagram shows how the API processes incoming requests and handles authentication:

- User sends a request to the API (e.g., to get a resource or perform an action).

- The request reaches the Server, where the `@app.before_request` function is triggered before any route is processed.

The request path is checked:

- If the request is in the `OUTLIST` (e.g., `/login`, `/register`), it's considered public and allowed immediately → `HTTP 200 OK`.

- If the request is not in the `OUTLIST`, it goes through token validation.

- In Token Control:

  - If the token is valid, the request proceeds and `HTTP 200` is sent.

  - If the token is invalid or missing, access is denied → `HTTP 401` Unauthorized.

Diagram:
<img src="https://i.imgur.com/LWEp3mS.png">


## 📱 User Interface  
<img src="https://i.imgur.com/CZbT52E.png">

## 🌟 Why MarketApp?

Unlike traditional online shopping systems, MarketApp aims to bring **digital convenience to physical market shopping**. It allows shopping through a mobile device, saving time for users and increasing operational efficiency on the market side.

With its modern, secure, and extensible structure, it offers a professional solution in terms of both technology and user experience.

---

## 👨‍💻 Developer: TOLGA ERSOY

🎓 Pamukkale University – Computer Engineering | Full Stack Developer

🐙 [My Github Account](https://github.com/tolgaersoy07)

---
