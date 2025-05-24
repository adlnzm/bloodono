# Blood-Connect

**Bridging Lives Through Blood Donation**

Blood-Connect is a web-based application built with **Streamlit** and **MySQL** that simplifies the process of managing and connecting **blood donors, receivers**, and **hospitals**. The app provides a centralized platform for users to register, search, and manage life-saving blood donation operations efficiently.

## Features

* **Donor Management** – Register new donors, view donor lists, and delete entries.
* **Receiver Management** – Add patients in need of blood, view and delete records.
* **Hospital Registry** – Register hospitals, view existing ones, or remove them.
* **Smart Search** – Search for blood donors by blood group and city.
* **Blood Compatibility Matching** – Built-in logic to identify compatible donors.
* **User-Friendly UI** – Clean, responsive UI built with Streamlit and enhanced with emojis and imagery.
* **Rain Animation** – Celebrate generosity with a raining blood drop animation using `streamlit_extras`.
  
## Preview

![Blood Connect UI](path_to_your_screenshot.png) *(Replace with actual image path)*

---

## 🛠️ Technologies Used

* [Streamlit](https://streamlit.io/) – For building the web app.
* [MySQL](https://www.mysql.com/) – Database for storing donor, receiver, and hospital data.
* [Pymysql](https://pymysql.readthedocs.io/) – Python MySQL client.
* [Pandas](https://pandas.pydata.org/) – For tabular data handling.
* [Geopy](https://pypi.org/project/geopy/) – Distance calculation (future use).
* [Scikit-learn](https://scikit-learn.org/) – KNN model integration (planned matching system).
* [Pillow](https://python-pillow.org/) – Image processing.
* [streamlit-extras](https://github.com/tylerjrichards/streamlit-extras) – For visual effects.

## Setup Instructions

### Prerequisites

* Python 3.7+
* MySQL server installed and running
* `pip` installed

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/blood-connect.git
   cd blood-connect
   ```

2. **Create and activate a virtual environment (optional but recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure MySQL is configured and running**. Update the following in the script if needed:

   ```python
   user='root'
   password=''  # Update with your MySQL password
   ```

5. **Run the app**:

   ```bash
   streamlit run app.py
   ```

## Project Structure

```
blood-connect/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── blood_donate.jpeg     # UI image for display
└── README.md             # Project documentation
```

## To-Do / Future Improvements

* [ ] Add location-based smart matching using latitude and longitude.
* [ ] Include scheduling and notification systems for blood donation.
* [ ] Integrate maps for visual location of donors/hospitals.
* [ ] Secure authentication for hospitals and verified users.
* [ ] Admin dashboard for full control over data.
