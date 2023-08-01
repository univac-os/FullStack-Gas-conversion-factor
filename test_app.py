import unittest
from app import app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_app = app.test_client()

    def test_get_conversion_factors(self):
        # Test valid input
        response = self.test_app.get('http://127.0.0.1:5000/get_conversion_factors?fuel=Butane&gas=CO2&liter=10')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['fuel'], 'Butane')
        self.assertEqual(data['gas'], 'CO2')
        self.assertEqual(data['liter'], 10)
        self.assertIn('conversion_factors', data)

    def test_get_conversion_factors_fuel_only(self):
        # Test valid input for fuel only
        response = self.test_app.get('http://127.0.0.1:5000/get_conversion_factors_fuel_only?fuel=Butane')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['fuel'], 'Butane')
        self.assertIn('conversion_factors', data)
    

if __name__ == '__main__':
    unittest.main()
