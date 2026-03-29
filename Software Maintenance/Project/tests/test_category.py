import sqlite3
import time
import pytest

CATEGORY_NAME = "UT Software Products"

# Function to test adding a new category to database
def test_category():
    """
    Unit Test:
    Test adding a new category to database
    """

    start = time.time()

    connection = sqlite3.connect("ims.db")
    cursor = connection.cursor()

    try:
        # Remove duplicate data if exists
        cursor.execute("DELETE FROM category WHERE name=?", (CATEGORY_NAME,))
        connection.commit()

        # Insert new category
        cursor.execute(
            "INSERT INTO category(name) VALUES(?)",
            (CATEGORY_NAME,)
        )

        connection.commit()

        # Check that the inserted category exists
        cursor.execute(
            "SELECT * FROM category WHERE name=?",
            (CATEGORY_NAME,)
        )

        result = cursor.fetchone()

        end = time.time()
        execution_time = round(end - start, 4)

        print("\n------ Category Unit Test Result ------")
        print(f"Category Name: {CATEGORY_NAME}")
        print(f"Execution Time: {execution_time} seconds")

        assert result is not None

        print("Test Status: SUCCESS")
        print("--------------------------------------\n")

    finally:
        connection.close()
