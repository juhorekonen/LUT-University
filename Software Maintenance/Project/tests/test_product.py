import sqlite3
import time
import pytest

PRODUCT = {
    "category": "Mobile Games",
    "supplier": "JR Electronics",
    "name": "GTA X",
    "price": "1999",
    "qty": "1",
    "status": "Active"
}

# Function to test adding a new product to database
def test_add_product():
    """
    Unit Test:
    Test adding a new product
    """

    start = time.time()

    connection = sqlite3.connect("ims.db")
    cursor = connection.cursor()

    try:
        # Remove duplicate product if exists
        cursor.execute(
            "DELETE FROM product WHERE name=?",
            (PRODUCT["name"],)
        )
        connection.commit()

        # Insert test product
        cursor.execute(
            """
            INSERT INTO product
            (Category,Supplier,name,price,qty,status)
            VALUES (?,?,?,?,?,?)
            """,
            (
                PRODUCT["category"],
                PRODUCT["supplier"],
                PRODUCT["name"],
                PRODUCT["price"],
                PRODUCT["qty"],
                PRODUCT["status"]
            )
        )

        connection.commit()

        # Check that the inserted product exists
        cursor.execute(
            "SELECT * FROM product WHERE name=?",
            (PRODUCT["name"],)
        )

        result = cursor.fetchone()

        end = time.time()
        execution_time = round(end - start, 4)

        print("\n------ Product Unit Test Result ------")
        print(f"Product Name: {PRODUCT['name']}")
        print(f"Category: {PRODUCT['category']}")
        print(f"Execution Time: {execution_time} seconds")

        assert result is not None

        print("Test Status: SUCCESS")
        print("--------------------------------------\n")

    finally:
        connection.close()
