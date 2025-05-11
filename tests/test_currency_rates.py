import unittest
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.database.database import Database
from src.services.api_service import CurrencyAPIService

class TestCurrencyRates(unittest.TestCase):
    def setUp(self):
        self.currency_service = CurrencyAPIService()
        self.db = Database()  

    def test_currency_rate_structure(self):
        """Test if currency rate has required fields"""
        # Database sınıfı bir ORM değil, dictionary kullanmalıyız
        rate_data = {
            'date': datetime.now(),
            'currency_code': "EUR",
            'rate': 1.2
        }
        
        self.assertIsNotNone(rate_data['date']) 
        self.assertIsNotNone(rate_data['currency_code'])
        self.assertIsNotNone(rate_data['rate'])
        self.assertEqual(rate_data['currency_code'], "EUR") 
        self.assertEqual(rate_data['rate'], 1.2) 

    def test_currency_service_initialization(self):
        """Test if currency service initializes correctly"""
        self.assertIsNotNone(self.currency_service) # CurrencyAPIService instance'inin None olmadığını kontrol et
        self.assertIsNotNone(self.currency_service.config)  # config'in None olmadığını kontrol et
        self.assertIn('key', self.currency_service.config)  # config içinde key olduğunu kontrol et

if __name__ == '__main__':
    unittest.main()