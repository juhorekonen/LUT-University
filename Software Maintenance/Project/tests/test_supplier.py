import sqlite3
import time
import pytest

SUPPLIER = {
    "invoice": 000, # This needs to be an integer
    "name": "UnitTest Supplier Ltd",
    "contact": "Hidden",
    "desc": "Unit test support"
}

# Function to test adding a new supplier to database
def test_add_supplier():
    """
    Unit Test:
    Test adding a new supplier
    """

    start = time.time()

    connection = sqlite3.connect("ims.db")
    cursor = connection.cursor()

    try:
        # Remove test supplier if exists
        cursor.execute(
            "DELETE FROM supplier WHERE invoice=?",
            (SUPPLIER["invoice"],)
        )
        connection.commit()

        # Insert supplier
        cursor.execute(
            """
            INSERT INTO supplier(invoice,name,contact,desc)
            VALUES (?,?,?,?)
            """,
            (
                SUPPLIER["invoice"],
                SUPPLIER["name"],
                SUPPLIER["contact"],
                SUPPLIER["desc"]
            )
        )

        connection.commit()

        # Fetch inserted supplier
        cursor.execute(
            "SELECT * FROM supplier WHERE invoice=?",
            (SUPPLIER["invoice"],)
        )

        result = cursor.fetchone()

        end = time.time()
        execution_time = round(end - start, 4)

        print("\n------ Supplier Unit Test Result ------")
        print(f"Supplier Invoice: {SUPPLIER['invoice']}")
        print(f"Supplier Name: {SUPPLIER['name']}")
        print(f"Execution Time: {execution_time} seconds")

        assert result is not None

        print("Test Status: SUCCESS")
        print("--------------------------------------\n")

    finally:
        connection.close()
