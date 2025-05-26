import unittest
import os
import sys

# ==============================================================================
## @file Test.py
#  @brief Unit test suite for the ML Electricity Demand Forecasting system.
#  @details Validates system functionality including module imports, data downloading,
#  and structural placeholders for future feature testing.
# ==============================================================================

# Dynamically resolve and add root directory to path
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

# ------------------------------------------------------------------------------
## @brief Try importing the required modules.
#  @warning Exits if modules are not found. Ensure directory names and cases match.
# ------------------------------------------------------------------------------
try:
    from CodeDataPreparation.DataDownload import download_energy_data
    from CodeDataPreparation import DataCombine, DataFilterHour
    from CodeDataVisualisation import demand_dec
    from CodeTimeForecast import Sarimamodel5
except ModuleNotFoundError as e:
    print(f"[IMPORT ERROR] {e}")
    print(" Make sure your folder names are correct and capitalized: e.g., 'CodeDataPreparation', not 'codedatapreparation'.")
    print(" Check that you're running the script from within the 'Test' directory.")
    sys.exit(1)

# ---------------------------- TEST CLASSES ----------------------------

## @class TestSystemFunctions
#  @brief Tests high-level system functions like data downloading.
class TestSystemFunctions(unittest.TestCase):
    ## @brief Tests the energy data download process.
    def test_data_download(self):
        """System Function: Data Download"""
        try:
            download_energy_data()
            print("[PASSED]  download_energy_data ran successfully.")
            self.assertTrue(True)
        except Exception as e:
            print(f"[FAILED]  download_energy_data failed: {e}")
            print(" Check your .env file for missing variables like BASE_URL, REGION, START_MONTH.")
            self.fail(f"Exception: {e}")

## @class TestParts
#  @brief Placeholder tests for intermediate script functionality.
class TestParts(unittest.TestCase):
    ## @brief Dummy test for DataCombine script functionality.
    def test_combination(self):
        """Part: Data Combination"""
        try:
            print("[PASSED]  DataCombine dummy test executed.")
            self.assertTrue(True)
        except Exception as e:
            print(f"[FAILED]  DataCombine failed: {e}")
            print(" Ensure DataCombine.py has no syntax errors and has functions.")
            self.fail()

    ## @brief Dummy test for DataFilterHour script functionality.
    def test_filter_hour(self):
        """Part: Data Filtering"""
        try:
            print("[PASSED]  DataFilterHour dummy test executed.")
            self.assertTrue(True)
        except Exception as e:
            print(f"[FAILED]  DataFilterHour failed: {e}")
            print(" Verify the DataFilterHour.py script for importable functions.")
            self.fail()

## @class TestModules
#  @brief Ensures all core modules are importable and not None.
class TestModules(unittest.TestCase):
    ## @brief Validates that key modules are correctly imported.
    def test_module_imports(self):
        """SW Module: Imports"""
        try:
            self.assertIsNotNone(DataCombine)
            self.assertIsNotNone(DataFilterHour)
            self.assertIsNotNone(demand_dec)
            self.assertIsNotNone(Sarimamodel5)
            print("[PASSED]  All modules imported successfully.")
        except Exception as e:
            print(f"[FAILED]  Module import failed: {e}")
            print("[INFO] Confirm the file names and '__init__.py' existence if needed.")
            self.fail()

## @class TestClasses
#  @brief Placeholder for future class structure validations.
class TestClasses(unittest.TestCase):
    ## @brief Dummy class structure check.
    def test_class_structure(self):
        """SW Classes (Placeholder)"""
        try:
            print("[PASSED]  Class structure test simulated.")
            self.assertTrue(True)
        except Exception as e:
            print(f"[FAILED]  Class structure test failed: {e}")
            self.fail()

## @class TestFunctions
#  @brief Placeholder for function-level SARIMA model testing.
class TestFunctions(unittest.TestCase):
    ## @brief Dummy test to simulate SARIMA logic testing.
    def test_sarima_placeholder(self):
        """SW Function: SARIMA Forecast"""
        try:
            print("[PASSED]  SARIMA forecast logic placeholder test.")
            self.assertTrue(True)
        except Exception as e:
            print(f"[FAILED]  SARIMA forecast test failed: {e}")
            print(" Review Sarimamodel5.py for broken function calls.")
            self.fail()

# ---------------------------- MAIN ----------------------------

## @brief Main entry point for executing the test suite.
if __name__ == '__main__':
    print("=" * 70)
    print("  RUNNING TEST SUITE FOR: ML ELECTRICITY DEMAND FORECASTING SYSTEM ")
    print("=" * 70)
    print(" Root directory resolved to:", ROOT_DIR)
    print(" Executing tests for functions, parts, modules, classes, and logic...\n")
    unittest.main(verbosity=2)