"""
Döviz kuru API servisi.
CurrencyAPI.net servisinden döviz kurlarını çeker.
"""
import logging
import requests
import sys
import os
# Projenin kök dizinini (CURRENCY RATES-2 klasörünü) import yoluna ekler
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.config.config import API_CONFIG

logger = logging.getLogger(__name__)

class CurrencyAPIService:
    def __init__(self):
        self.config = API_CONFIG

    def fetch_currency_rates(self):
        """
        CurrencyAPI.net'ten güncel döviz kurlarını çeker.
        Başarılı olursa JSON verisi, hata durumunda None döner.
        """
        try:
            response = requests.get(
                self.config['url'],
                params={
                    'key': self.config['key'],
                    'base': self.config['base_currency']
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Döviz kurları çekilirken hata oluştu: {e}")
            return None 
        
        
        