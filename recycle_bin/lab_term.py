import sqlite3
import random
import tkinter as tk
from tkinter import filedialog
from datetime import date


def get_db_connection():
    conn = sqlite3.connect("..\\hospital.db")
    conn.row_factory = sqlite3.Row
    return conn


def generate_lab_id(cursor):
    while True:
        lab_id = "L" + str(random.randint(100, 999))
        cursor.execute("SELECT labId FROM lab WHERE labId = ?", (lab_id,))
        if not cursor.fetchone():
            return lab_id


def login():
    print("\n" + "=" * 40)
    print("              LOGIN")
    print("=" * 40)

    lab_id = input("Enter Lab ID: ").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM lab WHERE labId = ?", (lab_id,))
    lab = cursor.fetchone()
    conn.close()

    if not lab:
        print("\n[ERROR] Invalid Lab ID. Please try again.")
        return None

    print(f"\n[SUCCESS] Welcome, Lab {lab_id}!")
    return dict(lab)


def signup():
    print("\n" + "=" * 40)
    print("              SIGNUP")
    print("=" * 40)

    conn = get_db_connection()
    cursor = conn.cursor()

    lab_id = generate_lab_id(cursor)

    try:
        cursor.execute(
            "INSERT INTO lab (labId) VALUES (?)",
            (lab_id,)
        )
        conn.commit()
        print(f"\n[SUCCESS] Lab registered! Your Lab ID is: {lab_id}")
        print("Please save your Lab ID — you'll need it to log in.")

    except sqlite3.IntegrityError as e:
        print(f"\n[ERROR] Could not register lab: {e}")
    finally:
        conn.close()


def browse_file():
    root = tk.Tk()
    root.withdraw()        # hide the tkinter window
    root.attributes("-topmost", True)  # bring dialog to front
    file_path = filedialog.askopenfilename(
        title="Select Report File",
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.doc *.docx"), ("All files", "*.*")]
    )
    root.destroy()

    if not file_path:
        return None, None

    with open(file_path, "rb") as f:
        file_data = f.read()

    return file_path, file_data


def add_report(lab_id):
    print("\n" + "=" * 40)
    print("           ADD LAB REPORT")
    print("=" * 40)

    patient_id = input("Patient ID   : ").strip()
    test_name  = input("Test Name    : ").strip()

    print("Browsing for report file...")
    file_path, file_data = browse_file()

    if not file_data:
        print("\n[ERROR] No file selected. Aborting.")
        return

    print(f"File selected: {file_path}")

    result     = input("Result       : ").strip()
    today      = date.today().strftime("%Y-%m-%d")
    entry_date = input(f"Date (YYYY-MM-DD) [press Enter for today: {today}]: ").strip()
    if not entry_date:
        entry_date = today

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO lab (labId, patientId, testName, reportBlob, result, date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (lab_id, patient_id, test_name, file_data, result, entry_date)
        )
        conn.commit()
        print(f"\n[SUCCESS] Report for Patient {patient_id} added successfully!")
    except sqlite3.Error as e:
        print(f"\n[ERROR] Could not add report: {e}")
    finally:
        conn.close()


# MAIN PROGRAM
while True:
    print("\n" + "=" * 40)
    print("       HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 40)
    print("  1. Login")
    print("  2. Signup")
    print("  3. Exit")
    print("=" * 40)

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        selected_lab = login()
        if selected_lab:
            print(f"\nLogged in as: Lab (ID: {selected_lab['labId']})")

            while True:
                print("\n" + "=" * 40)
                print("           LAB MENU")
                print("=" * 40)
                print("  1. Add Report")
                print("  2. Logout")
                print("=" * 40)

                lab_choice = input("Enter your choice (1/2): ").strip()

                if lab_choice == "1":
                    add_report(selected_lab['labId'])
                elif lab_choice == "2":
                    print("\n[INFO] Logged out.")
                    break
                else:
                    print("\n[ERROR] Invalid choice.")

    elif choice == "2":
        signup()

    elif choice == "3":
        print("\nGoodbye!")
        break

    else:
        print("\n[ERROR] Invalid choice. Please enter 1, 2, or 3.")