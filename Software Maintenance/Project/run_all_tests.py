# This file executes three unit tests and two integration tets for the Inventory Management System (IMS).
import subprocess
import sys

def run_tests():

    # First run unit tests, then integration tests. If any test fails, the script will stop and print the failed test.
    print("\n==============================")
    print("Running Unit Tests")
    print("==============================\n")

    unit_tests = [
        "tests/test_category.py",
        "tests/test_supplier.py",
        "tests/test_product.py"
    ]

    for test in unit_tests:
        result = subprocess.run(["pytest", "-s", test])
        if result.returncode != 0:
            print(f"\nUnit Test Failed: {test}")
            sys.exit(1)

    print("\nUnit Tests Successful")
    print("\n==============================")
    print("Running Integration Tests")
    print("==============================\n")

    integration_tests = [
        "tests/test_integration_category_product.py",
        "tests/test_integration_supplier_product.py"
    ]

    for test in integration_tests:
        result = subprocess.run(["pytest", "-s", test])
        if result.returncode != 0:
            print(f"\nIntegration Test Failed: {test}")
            sys.exit(1)

    print("\n==============================")
    print("All Tests Completed Successfully")
    print("==============================\n")


if __name__ == "__main__":
    run_tests()
