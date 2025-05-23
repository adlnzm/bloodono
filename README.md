# Blood-Connect

**Blood-Connect** is a simple, user-friendly web application built using **Streamlit** and **MySQL** that helps manage donors, receivers, and hospitals for blood donations. It also allows users to search for available donors based on blood group and location.

---

## Features

* Add, list, and delete **donors** and **receivers**
* Register and remove **hospitals**
* Search for **donors by blood group and city**
* Schedule and confirm blood donation appointments
* Backend powered by **MySQL**
* Interactive UI built with **Streamlit**

---

## Technologies Used

* [Streamlit](https://streamlit.io/)
* [PyMySQL](https://pymysql.readthedocs.io/)
* [MySQL](https://www.mysql.com/)

---

## Project Structure

```
├── app.py              # Main application code
├── README.md           # Project documentation
```

## Setup Instructions

### Prerequisites

* Python 3.7+
* MySQL server running locally
* Required Python packages:

  ```bash
  pip install streamlit pymysql
  ```

### Database Setup

Create a database named `blood_donation_db` in your MySQL server:

```sql
CREATE DATABASE blood_donation_db;
```

Ensure your MySQL user credentials (host, user, password) in the code match your MySQL configuration.

### Running the App

```bash
streamlit run app.py
```

Access the app in your browser at: [http://localhost:8501](http://localhost:8501)

## Functionality Overview

### Donor Management

* Add new donors with personal and location details.
* View a list of all donors.
* Delete donors by ID.

### Receiver Management

* Register new blood receivers.
* View receiver list.
* Delete receivers by ID.

### Hospital Management

* Add hospital contact and address information.
* Delete hospitals by ID.

### Donor Search & Scheduling

* Search for donors by blood group and city.
* View matching donor details.
* Schedule donation with date and time.

## Notes

* This is a basic version intended for educational/demo purposes.
* Replace the empty password (`''`) with your actual MySQL root password in `get_connection()`.
* For production use, implement authentication, input validation, and better error handling.

## Screenshots

*Add screenshots of the app's UI here (optional)*
