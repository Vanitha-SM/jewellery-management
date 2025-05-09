import mysql.connector

con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='randompassword',
    port='3306',
    database='jewel'
)

if con.is_connected():
    print("Successfully connected to the database.")

cursor = con.cursor()

while True:
    print("\n===== DAZZLE JEWELLERY MANAGEMENT =====")
    print("1. Employee Entry")
    print("2. Purchase Entry")
    print("3. Sales Entry")
    print("4. Print Bill")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        ecode = input("Employee Code: ")
        ename = input("Name: ")
        edes = input("Designation: ")
        esal = int(input("Salary: "))
        eadd = input("Address: ")
        ephone = input("Phone: ")
        sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (ecode, ename, edes, esal, eadd, ephone))
        con.commit()
        print("Employee saved.")

    elif choice == '2':
        pdt = input("Purchase Date (YYYY-MM-DD): ")
        itemcode = input("Item Code: ")
        itemname = input("Item Name: ")
        qty = int(input("Quantity: "))
        sql = "INSERT INTO purchase VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (pdt, itemcode, itemname, qty))
        con.commit()
        print("Purchase saved.")

    elif choice == '3':
        sdt = input("Sale Date (YYYY-MM-DD): ")
        cname = input("Customer Name: ")
        cadd = input("Customer Address: ")
        cmob = input("Customer Phone: ")
        spcode = input("Salesperson Code: ")

        cursor.execute("SELECT COALESCE(MAX(bno), 0) FROM sales")
        bno = cursor.fetchone()[0] + 1

        n = int(input("Number of items: "))
        for i in range(n):
            print(f"\nItem {i+1}")
            icode = input("Item Code: ")
            wt = float(input("Weight: "))
            ws = int(input("Wastage (%): "))
            mc = int(input("Making Charge: "))
            rate = int(input("Rate/gm: "))
            amt = rate * wt + (rate * wt * ws / 100)
            tax = amt * 0.03
            total = amt + tax + mc
            sql = "INSERT INTO sales VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (bno, sdt, icode, rate, wt, ws, mc, amt, tax, total, cmob, spcode))
            con.commit()

        cursor.execute("INSERT INTO customer VALUES (%s, %s, %s)", (cname, cadd, cmob))
        con.commit()
        print("Sale and customer saved.")

    elif choice == '4':
        bill = input("Enter bill number to print: ")
        sql = """SELECT bno, bdate, cname, cadd, s.cmob FROM sales s 
                 JOIN customer c ON s.cmob = c.cmob WHERE bno = %s"""
        cursor.execute(sql, (bill,))
        result = cursor.fetchone()
        if not result:
            print("Invalid bill number.")
            continue
        print("\n=== BILL ===")
        print(f"Bill No: {result[0]}, Date: {result[1]}")
        print(f"Customer: {result[2]}, Address: {result[3]}, Phone: {result[4]}")
        print("-" * 50)
        sql2 = """SELECT itemname, weight, wastage, rate, amt, tax, mc, total FROM sales s 
                  JOIN purchase p ON s.itemcode = p.itemcode WHERE s.bno = %s"""
        cursor.execute(sql2, (bill,))
        total = 0
        for row in cursor.fetchall():
            print(row)
            total += row[7]
        print(f"Grand Total: ₹{total:.2f}")

    elif choice == '5':
        print("Exiting...")
        break

    else:
        print("Invalid choice.")

cursor.close()
con.close()
