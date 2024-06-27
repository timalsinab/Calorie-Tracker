import unittest
from unittest.mock import patch
from project import setup_database, fetch_nutrition_data, save_food_entry, display_summary, clear_database

class TestCalorieTracker(unittest.TestCase):

    def setUp(self):
        self.conn = setup_database({
            'name': ':memory:'
        })  # Using an in-memory database for testing
    
    def tearDown(self):
        clear_database(self.conn)
        self.conn.close()

    def test_setup_database(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='food_entries';")
        self.assertIsNotNone(cursor.fetchone())

    def test_fetch_nutrition_data(self):
        result = fetch_nutrition_data("1 apple")
        self.assertIsNotNone(result)
        self.assertIn('items', result)

    def test_save_food_entry(self):
        nutrition_data = fetch_nutrition_data("1 apple")
        save_food_entry(self.conn, "1 apple", nutrition_data)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM food_entries WHERE food_name='1 apple';")
        entry = cursor.fetchone()
        self.assertIsNotNone(entry)
        self.assertEqual(entry[1], "1 apple")

    @patch('builtins.print')
    def test_display_summary(self, mock_print):
        nutrition_data = fetch_nutrition_data("1 apple")
        save_food_entry(self.conn, "1 apple", nutrition_data)
        display_summary(self.conn)
        
        mock_print.assert_any_call("Today's Food Entries:")
        mock_print.assert_any_call("1 apple - Calories: 96.4, Fat: 0.3g, Protein: 0.50g, Carbohydrates: 25.6g")
        mock_print.assert_any_call("\nToday's Summary:")
        mock_print.assert_any_call("Total Calories: 96.4")
        mock_print.assert_any_call("Total Fat: 0.3g")
        mock_print.assert_any_call("Total Protein: 0.50g")
        mock_print.assert_any_call("Total Carbohydrates: 25.6g")

    def test_clear_database(self):
        nutrition_data = fetch_nutrition_data("1 apple")
        save_food_entry(self.conn, "1 apple", nutrition_data)
        clear_database(self.conn)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM food_entries;")
        self.assertEqual(cursor.fetchall(), [])

if __name__ == '__main__':
    unittest.main()
