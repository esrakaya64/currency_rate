import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
import time
import schedule
from datetime import datetime
from config.config import APP_CONFIG
from database.database import Database
from services.api_service import CurrencyAPIService
from logs.logger import logger

class CurrencyRateApp:
    def __init__(self):
        self.db = Database()
        self.api_service = CurrencyAPIService()

    def update_currency_rates(self):
        logger.info("Döviz kurları güncelleme işi başlatılıyor")
        rates_data = self.api_service.fetch_currency_rates()
        if rates_data:
            self.db.store_currency_rates(rates_data, datetime.now().date())
        logger.info("Döviz kurları güncelleme işi tamamlandı")

    def run(self):
        self.db.create_tables()
        
        # Schedule the daily update
        schedule.every().day.at(APP_CONFIG['schedule_time']).do(self.update_currency_rates)
        
        logger.info("Uygulama başlatıldı. İlk döviz kurları güncellemesi yapılıyor...")
        
        # Run the update immediately when starting
        self.update_currency_rates()
        
        logger.info("Zamanlanmış görevler bekleniyor...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    app = CurrencyRateApp()
    app.run() 
