#  Store Smart Manager

**Store Smart Manager** is a Python-based inventory and billing management system built on top of **MySQL**.  
It helps shopkeepers and small businesses to manage products, track expiry dates, generate bills, and calculate daily profits efficiently.

---

##  Features

- **Database Setup**
  - Automatically creates a database (`mydb`) and table (`item`) if they don’t exist.
  - Stores product details: `ID`, `Product Name`, `Stock`, `Cost Price`, `Selling Price`, `Vendor`, `Expiry Date`, and `Position`.

- **Add Products**
  - Add new items with unique IDs.
  - Supports products with/without expiry dates.
  - Ensures valid dates and unique item IDs.

- **Billing System**
  - Generate bills with customer name, product details, discounts, and net payable amount.  
  - Auto-updates stock after each sale.  
  - Deletes items when stock reaches zero.  
  - Tracks **profit per day** (Selling Price – Cost Price).

- **Expiry Tracking**
  - View items expiring in the next 7 days.

- **Profit Tracking**
  - View daily profit at any time.

- **Interactive Menu**
  - `u` → Update/Add products  
  - `b` → Generate bill  
  - `p` → View today’s profit  
  - `s` → Check items expiring soon  
  - `st` → Stop program 
