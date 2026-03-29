import sqlite3
import time

# Test to verify integration between category and product modules
def test_category_product_integration():

    # This test will create a category and then create a product using that category. 
    # Finally, it will verify that the product was created successfully.

    start = time.time()

    connection = sqlite3.connect("ims.db")
    cursor = connection.cursor()

    try:
        category_name = "ICategory"
        product_name = "IProduct"

        # Clean duplicate test data
        cursor.execute("DELETE FROM product WHERE name=?", (product_name,))
        cursor.execute("DELETE FROM category WHERE name=?", (category_name,))
        connection.commit()

        # Create the category first
        cursor.execute(
            "INSERT INTO category(name) VALUES(?)",
            (category_name,)
        )

        # Then create a product using that category
        cursor.execute(
            """
            INSERT INTO product
            (Category,Supplier,name,price,qty,status)
            VALUES (?,?,?,?,?,?)
            """,
            (
                category_name,
                "UnitTest Supplier Ltd", # Supplier from unit test, can be modified
                product_name,
                "100",
                "5",
                "Inactive"
            )
        )

        connection.commit()

        # Verify product exists
        cursor.execute(
            "SELECT * FROM product WHERE name=?",
            (product_name,)
        )

        result = cursor.fetchone()

        end = time.time()

        print("\nCategory-Product Integration Test")
        print(f"Execution Time: {round(end - start, 4)}s")

        assert result is not None

        print("Test Status: SUCCESS")

    finally:
        connection.close()
