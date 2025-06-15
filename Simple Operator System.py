import sqlite3
from datetime import datetime

# Connect to local database
conn = sqlite3.connect("simple_operator_system.db")
cursor = conn.cursor()

# Create operator login table
cursor.execute('''
CREATE TABLE IF NOT EXISTS operators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

# Create goods receiving table with timestamp
cursor.execute('''
CREATE TABLE IF NOT EXISTS goods_receiving (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id INTEGER,
    product_name TEXT,
    supplier_name TEXT,
    quantity REAL,
    unit TEXT,
    rate_per_unit REAL,
    total_rate REAL,
    tax REAL,
    entry_time TEXT
)
''')

# Add two simple operators
def add_operator(username, password):
    try:
        cursor.execute("INSERT INTO operators (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already exists

add_operator("operator1", "1234")
add_operator("operator2", "5678")

# Login function
def login():
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT id FROM operators WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result:
        print("\nLogin successful!\n")
        return result[0]
    else:
        print("Login failed.")
        return None

# Add goods receiving entry
def add_goods(operator_id):
    product = input("Product name: ")
    supplier = input("Supplier name: ")
    quantity = float(input("Quantity: "))
    unit = input("Unit: ")
    rate = float(input("Rate per unit: "))
    total = quantity * rate
    tax = total * 0.18  # 18% tax
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
    INSERT INTO goods_receiving (operator_id, product_name, supplier_name, quantity, unit, rate_per_unit, total_rate, tax, entry_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (operator_id, product, supplier, quantity, unit, rate, total, tax, entry_time))
    conn.commit()
    print("Entry saved.\n")

# View past entries
def view_entries(operator_id):
    cursor.execute('''
    SELECT product_name, supplier_name, quantity, unit, rate_per_unit, total_rate, tax, entry_time
    FROM goods_receiving
    WHERE operator_id=?
    ORDER BY entry_time DESC
    ''', (operator_id,))
    rows = cursor.fetchall()
    if rows:
        print("\n--- Past Goods Received Entries ---")
        for row in rows:
            print(f'''
Product: {row[0]}
Supplier: {row[1]}
Quantity: {row[2]} {row[3]}
Rate per unit: {row[4]}
Total: {row[5]}
Tax: {row[6]}
Date/Time: {row[7]}
''')
    else:
        print("No entries found.\n")

# Main program loop
if __name__ == "__main__":
    op_id = login()
    if op_id:
        while True:
            print("1. Add Goods Entry")
            print("2. View Past Entries")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                add_goods(op_id)
            elif choice == "2":
                view_entries(op_id)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.\n")
