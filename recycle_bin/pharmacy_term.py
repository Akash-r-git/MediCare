import sqlite3
import os

PHARMACY_PASSWORD = "pharmacy123"
ORDERS_FILE = "..\\..\\txt_files\\orders.txt"


def get_db_connection():
    conn = sqlite3.connect("..\\hospital.db")
    conn.row_factory = sqlite3.Row
    return conn


# ──────────────────────────────────────────
#  STOCK
# ──────────────────────────────────────────

def insert_stock():
    print("\n" + "=" * 40)
    print("           INSERT STOCK")
    print("=" * 40)

    drug_id    = input("Drug ID       : ").strip()
    batch_id   = input("Batch ID      : ").strip()
    drug_name  = input("Drug Name     : ").strip()
    quantity   = input("Quantity      : ").strip()
    price      = input("Price         : ").strip()
    drugType      = input("Drug Type     : ").strip()
    expiry     = input("Expiry Date (YYYY-MM-DD): ").strip()

    if not quantity.isdigit():
        print("\n[ERROR] Quantity must be a number.")
        return
    try:
        price = float(price)
    except ValueError:
        print("\n[ERROR] Price must be a number.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO pharmacyInventory (drugId, batchId, drugName, quantity, price, expiryDate, drugType)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (drug_id, batch_id, drug_name, int(quantity), price, expiry, drugType)
        )
        conn.commit()
        print(f"\n[SUCCESS] {drug_name} added to inventory.")
    except sqlite3.Error as e:
        print(f"\n[ERROR] {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────
#  ORDERS
# ──────────────────────────────────────────

def see_orders():
    if not os.path.exists(ORDERS_FILE):
        print("\n[INFO] No pending orders.")
        return

    with open(ORDERS_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("\n[INFO] No pending orders.")
        return

    print("\n" + "=" * 50)
    print("            PENDING ORDERS")
    print("=" * 50)
    for i, line in enumerate(lines, start=1):
        patient_id, drug_id, drug_name, quantity = line.split("|")
        print(f"  {i}. Patient: {patient_id} | Drug: {drug_name} ({drug_id}) | Qty: {quantity}")
    print("=" * 50)


def remove_order():
    if not os.path.exists(ORDERS_FILE):
        print("\n[INFO] No pending orders.")
        return

    with open(ORDERS_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("\n[INFO] No pending orders.")
        return

    print("\n" + "=" * 50)
    print("            PENDING ORDERS")
    print("=" * 50)
    for i, line in enumerate(lines, start=1):
        patient_id, drug_id, drug_name, quantity = line.split("|")
        print(f"  {i}. Patient: {patient_id} | Drug: {drug_name} ({drug_id}) | Qty: {quantity}")
    print("=" * 50)

    choice = input("\nEnter order number to remove (or 0 to go back): ").strip()

    if choice == "0":
        return

    if not choice.isdigit() or not (1 <= int(choice) <= len(lines)):
        print("\n[ERROR] Invalid choice.")
        return

    removed = lines.pop(int(choice) - 1)
    with open(ORDERS_FILE, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))

    _, _, drug_name, quantity = removed.split("|")
    print(f"\n[SUCCESS] Order for {drug_name} x{quantity} removed.")


def orders_menu():
    while True:
        print("\n" + "=" * 40)
        print("           ORDERS")
        print("=" * 40)
        print("  1. See Orders")
        print("  2. Remove Order")
        print("  3. Back")
        print("=" * 40)

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            see_orders()
        elif choice == "2":
            remove_order()
        elif choice == "3":
            break
        else:
            print("\n[ERROR] Invalid choice.")

def view_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pharmacyInventory")
        results = cursor.fetchall()

        if not results:
            print("\n[INFO] Inventory is empty.")
            return

        print("\n" + "=" * 80)
        print(f"  {'Drug ID':<10} {'Batch ID':<10} {'Drug Name':<20} {'Quantity':<10} {'Price':<10} {'Expiry Date':<15} {'Type'}")
        print("=" * 80)
        for row in results:
            print(f"  {row['drugId']:<10} {row['batchId']:<10} {row['drugName']:<20} {row['quantity']:<10} Rs.{row['price']:<10.2f} {row['expiryDate']:<15} {row['drugType']}")
        print("=" * 80)
    except sqlite3.Error as e:
        print(f"\n[ERROR] {e}")
    finally:
        conn.close()

# ──────────────────────────────────────────
#  LOGIN + MAIN MENU
# ──────────────────────────────────────────

def login():
    print("\n" + "=" * 40)
    print("         PHARMACY LOGIN")
    print("=" * 40)

    password = input("Enter Password: ").strip()

    if password != PHARMACY_PASSWORD:
        print("\n[ERROR] Invalid password.")
        return False

    print("\n[SUCCESS] Welcome, Pharmacist!")
    return True


# MAIN PROGRAM
if not login():
    exit()

while True:
    print("\n" + "=" * 40)
    print("       PHARMACY MANAGEMENT")
    print("=" * 40)
    print("  1. Insert Stock")
    print("  2. Orders")
    print("  3. View Inventory")
    print("  4. Exit")
    print("=" * 40)

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        insert_stock()
    elif choice == "2":
        orders_menu()
    elif choice == "3":
        view_inventory()
    elif choice == "4":
        print("\nGoodbye!")
        break
    else:
        print("\n[ERROR] Invalid choice. Please enter 1, 2, or 3.")