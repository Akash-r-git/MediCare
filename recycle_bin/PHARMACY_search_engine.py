import sqlite3
import os

ORDERS_FILE = "..\\..\\txt_files\\orders.txt"


def get_db_connection():
    conn = sqlite3.connect("D:\\PROGRAMS\\first-yr-sem-2\\python\\package\\py_files\\hospital.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_unit(drug_type):
    if not drug_type:
        return "pieces"
    dt = drug_type.strip().lower()
    if dt == "tablet":
        return "tablets"
    elif dt == "tonic":
        return "bottles"
    elif dt == "ointment":
        return "tubes"
    else:
        return "pieces"


def display_results(results):
    print("\n" + "=" * 72)
    print(f"  {'#':<4} {'Drug ID':<10} {'Drug Name':<20} {'Expiry':<12} {'Stock':<15} {'Total Price'}")
    print("=" * 72)
    for i, row in enumerate(results, start=1):
        unit      = get_unit(row['drugType'])
        stock_str = f"{row['quantity']} {unit}"
        total     =  row['price']
        print(f"  {i:<4} {row['drugId']:<10} {row['drugName']:<20} {row['expiryDate']:<12} {stock_str:<15} Rs.{total:.2f}")
    print("=" * 65)


def place_order(patient_id, drug_id, drug_name, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE pharmacyInventory SET quantity = quantity - ? WHERE drugId = ?",
            (quantity, drug_id)
        )
        conn.commit()
    finally:
        conn.close()

    with open(ORDERS_FILE, "a") as f:
        f.write(f"{patient_id}|{drug_id}|{drug_name}|{quantity}\n")
    print(f"\n[SUCCESS] Order placed for {drug_name} x{quantity}!")


def search_drugs(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    while True:
        print("\n" + "=" * 65)
        print("              DRUG SEARCH ENGINE")
        print("=" * 65)
        keyword = input("Enter Drug Name or Drug ID to search (or 'exit' to quit): ").strip()

        if keyword.lower() == "exit":
            break

        if not keyword:
            print("\n[ERROR] Please enter a search term.")
            continue


        cursor.execute(
            """SELECT * FROM pharmacyInventory
               WHERE LOWER(drugName) LIKE LOWER(?) OR LOWER(drugId) LIKE LOWER(?)""",
            (f"%{keyword}%", f"%{keyword}%")
        )
        results = cursor.fetchall()

        if not results:
            print(f"\n[INFO] No drugs found matching '{keyword}'.")
            continue

        display_results(results)

        # Order flow
        choice = input("\nEnter row number to order a drug (or 0 to search again): ").strip()

        if choice == "0" or not choice.isdigit():
            continue

        idx = int(choice) - 1
        if not (0 <= idx < len(results)):
            print("\n[ERROR] Invalid selection.")
            continue

        selected = results[idx]
        unit = get_unit(selected['drugType'])

        print(f"\nSelected: {selected['drugName']} ({selected['drugId']}) — Rs.{selected['price']:.2f} per {unit[:-1]}")

        qty_input = input(f"Enter quantity (in {unit}): ").strip()

        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("\n[ERROR] Quantity must be a positive number.")
            continue

        qty = int(qty_input)

        if qty > selected['quantity']:
            print(f"\n[ERROR] Only {selected['quantity']} {unit} available in stock.")
            continue

        total = qty * selected['price']
        print(f"\n  Drug   : {selected['drugName']}")
        print(f"  Qty    : {qty} {unit}")
        print(f"  Total  : Rs.{total:.2f}")

        confirm = input("\nConfirm order? (y/n): ").strip().lower()
        if confirm == "y":
            place_order(patient_id, selected['drugId'], selected['drugName'], qty)
        else:
            print("\n[INFO] Order cancelled.")

    conn.close()


# ── For standalone testing ──
if __name__ == "__main__":
    test_patient_id = input("Enter your Patient ID: ").strip()
    search_drugs(test_patient_id)