import sqlite3
import time

# Test to verify integration between supplier and product modules
def test_supplier_product_integration():

    start = time.time()

    # This test will create a supplier and then create a product using that supplier. 
    # Finally, it will verify that the product was created successfully.

    connection = sqlite3.connect("ims.db")
    cursor = connection.cursor()

    try:
        supplier_name = "Integration Supplier Ltd"
        product_name = "ISProduct"

        # Clean old data
        cursor.execute("DELETE FROM product WHERE name=?", (product_name,))
        cursor.execute("DELETE FROM supplier WHERE name=?", (supplier_name,))
        connection.commit()

        # Create supplier
        cursor.execute(
            """
            INSERT INTO supplier
            (invoice,name,contact,desc)
            VALUES (?,?,?,?)
            """,
            (
                1800,
                supplier_name,
                "123456789",
                "Integration test support"
            )
        )

        # Create product
        cursor.execute(
            """
            INSERT INTO product
            (Category,Supplier,name,price,qty,status)
            VALUES (?,?,?,?,?,?)
            """,
            (
                "Electronics",
                supplier_name,
                product_name,
                "200",
                "10",
                "Active"
            )
        )

        connection.commit()

        # Verify
        cursor.execute(
            "SELECT * FROM product WHERE name=?",
            (product_name,)
        )

        result = cursor.fetchone()

        end = time.time()

        print("\nSupplier-Product Integration Test")
        print(f"Execution Time: {round(end - start,4)}s")

        assert result is not None

        print("Test Status: SUCCESS")

    finally:
        connection.close()
