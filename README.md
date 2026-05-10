# MediCare

**MediCare** is a comprehensive healthcare management platform designed to streamline interactions between patients, doctors, pharmacies, and laboratories. It provides a centralized ecosystem for appointment scheduling, medical record management, and pharmaceutical logistics.

## 🚀 Tech Stack

* **Frontend:** HTML5, CSS3
* **Backend:** Python (Flask)
* **Database:** SQLite

---

## ✨ Key Features

### 👨‍⚕️ Doctors
* **Appointment Management:** Accept or reject patient requests and assign specific time slots.
* **Patient History:** Access and view past medical records to provide informed care.
* **Digital Prescriptions:** Write and issue prescriptions directly through the portal.
* **Schedule Overview:** A dedicated dashboard to track upcoming appointments.

### 👤 Patients
* **Smart Booking:** Book appointments by department and date. Patients can request a specific doctor; if rejected, the request is automatically moved to the "Common Pool" of that department.
* **Multi-Account Support:** Manage multiple patient profiles under a single phone number and password (ideal for families).
* **Pharmacy & Lab Integration:** Browse medicine stocks, place orders, and view uploaded lab reports online.

### 💊 Pharmacy
* **Inventory Management:** Update and maintain medicine stock levels in real-time.
* **Order Fulfillment:** Accept or remove incoming medicine orders from patients.

### 🔬 Laboratory
* **Result Digitization:** Securely upload and manage lab reports for patient access.

---

## 🛠️ Setup and Installation

Follow these steps to get the project running locally:

1.  **Create a virtual environment**
    ```powershell
    python -m venv venv
    ```

2.  **Activate the virtual environment**
    ```powershell
    venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies from `requirements.txt`**
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Run the application**
    From the project root, run:
    ```powershell
    python py_files/main.py
    ```

5.  **Access the platform**
    Open `http://127.0.0.1:5000` in your browser.

> If `requirements.txt` is missing or incomplete, install Flask manually:
> ```powershell
> pip install Flask
> ```
