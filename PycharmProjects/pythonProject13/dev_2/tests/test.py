import unittest
from dev_2.dev_2 import search_records, calculate_statistics


class TestFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_file = 'test_data.csv'
        with open(cls.test_file, 'w') as file:
            file.write("date,type,category,description,amount\n")
            file.write("2024-01-01,income,salary,January salary,3000.00\n")
            file.write("2024-01-02,expense,food,Groceries,-150.50\n")
            file.write("2024-01-03,expense,food,Dinner,-200.00\n")
            file.write("2024-01-04,income,freelance,Project payment,500.00\n")
            file.write("2024-02-01,expense,entertainment,Cinema,-50.00\n")

    # Тесты search_records
    def test_search_records_normal_case(self):
        result = search_records(self.test_file, 'food')
        self.assertEqual(len(result), 2)

    def test_search_records_no_results(self):
        result = search_records(self.test_file, 'travel')
        self.assertEqual(len(result), 0)

    def test_search_records_empty_category(self):
        result = search_records(self.test_file, '')
        self.assertGreater(len(result), 0)

    # Тесты calculate_statistics

    def test_calculate_statistics_normal_case(self):
        result = calculate_statistics(self.test_file, "2024-01-01", "2024-01-21")
        self.assertEqual(result['income'], 3500.00)
        self.assertEqual(result['expense'], -350.50)

    def test_calculate_statistics_no_records(self):
        result = calculate_statistics(self.test_file, "2025-01-01", "2025-01-31")
        self.assertEqual(result['income'], 0)
        self.assertEqual(result['expense'], 0)

    def test_calculate_statistics_income(self):
        result = calculate_statistics(self.test_file, "2024-01-01", "2024-01-04")
        self.assertEqual(result['income'], 3500.00)
        self.assertEqual(result['expense'], 0)

    def test_calculate_statistics_expense(self):
        result = calculate_statistics(self.test_file, "2024-01-02", "2024-01-03")
        self.assertEqual(result['income'], 0)
        self.assertEqual(result['expense'], -350.50)

    def test_calculate_statistics_large_date_range(self):
        result = calculate_statistics(self.test_file, "1900-01-01", "2100-01-01")
        self.assertEqual(result['income'], 3500.00)
        self.assertEqual(result['expense'], -400.50)


if __name__ == '__main__':
    unittest.main()