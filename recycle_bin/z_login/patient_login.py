import sqlite3
import uuid


def get_db_connection():
    conn = sqlite3.connect("..\\hospital.db")
    conn.row_factory = sqlite3.Row
    return conn


def login():
    print("\n" + "=" * 40)
    print("              LOGIN")
    print("=" * 40)

    phone_no = input("Enter Phone Number: ").strip()
    password = input("Enter Password: ").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patient WHERE phoneNo = ? AND password = ?",
        (phone_no, password)
    )
    patients = cursor.fetchall()
    conn.close()

    if not patients:
        print("\n[ERROR] Invalid phone number or password. Please try again.")
        return None

    # Display matching patients
    print("\n" + "=" * 40)
    print("Select a Patient Profile:")
    print("=" * 40)
    for patient in patients:
        print(f"  Name: {patient['name']}  |  ID: {patient['patientId']}")
    print("=" * 40)

    while True:
        choice = input("\nEnter Patient ID from the list above: ").strip()
        matched = next((p for p in patients if p['patientId'] == choice), None)
        if matched:
            print(f"\n[SUCCESS] Welcome, {matched['name']}!")
            return dict(matched)
        else:
            print("[ERROR] Invalid Patient ID. Please enter a valid ID from the list.")


def signup():
    print("\n" + "=" * 40)
    print("              SIGNUP")
    print("=" * 40)

    name      = input("Full Name              : ").strip()
    age       = input("Age                    : ").strip()
    dob       = input("Date of Birth (YYYY-MM-DD): ").strip()
    gender    = input("Gender (M/F/Other)     : ").strip()
    phone_no  = input("Phone Number           : ").strip()
    address   = input("Address                : ").strip()
    allergies = input("Allergies (or 'None')  : ").strip()
    password  = input("Set Password           : ").strip()

    if not age.isdigit():
        print("\n[ERROR] Age must be a number.")
        return

    # Auto-generate a unique patient ID 
    patient_id = "P" + str(uuid.uuid4())[:8].upper()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO patient (patientId, age, name, phoneNo, password, address, gender, allergies, DOB)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (patient_id, int(age), name, phone_no, password, address, gender, allergies, dob)
        )
        conn.commit()
        print(f"\n[SUCCESS] Account created! Your Patient ID is: {patient_id}")
        print("Please save your Patient ID — you'll need it to log in.")
    except sqlite3.IntegrityError as e:
        print(f"\n[ERROR] Could not create account: {e}")
    finally:
        conn.close()

def patient_login_menu():
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
            selected_patient = login()
            if selected_patient:
                print(f"\nLogged in as: {selected_patient['name']} (ID: {selected_patient['patientId']})")
                # Continue with rest of the application...
                break

        elif choice == "2":
            signup()

        elif choice == "3":
            print("\nGoodbye!")
            break

        else:
            print("\n[ERROR] Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    patient_login_menu()
    