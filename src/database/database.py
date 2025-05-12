import logging
import psycopg2
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.config.config import DB_CONFIG

load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.config = DB_CONFIG

    def get_connection(self):
        return psycopg2.connect(**self.config)

    def create_tables(self):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS currency_rates (
                            id SERIAL PRIMARY KEY,
                            date DATE NOT NULL,
                            currency_code VARCHAR(100) NOT NULL,
                            rate DECIMAL(20, 10) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(date, currency_code)
                        )
                    """)
                    conn.commit()
                    logger.info("Veritabanı tabloları başarıyla oluşturuldu")
        except Exception as e:
            logger.error(f"Tablolar oluşturulurken hata: {e}")
            raise

    def store_currency_rates(self, rates_data, date):
        if not rates_data or 'rates' not in rates_data:
            logger.error("Invalid rates data received")
            return

        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                values_to_insert = []
                for currency_code, rate in rates_data['rates'].items():
                    if currency_code == os.getenv('API_BASE_CURRENCY'):
                        continue
                    try:
                        rate_float = float(rate)
                        values_to_insert.append((date, currency_code, rate_float))
                    except (ValueError, TypeError) as e:
                        logger.error(f"Invalid rate value for {currency_code}: {rate} - {str(e)}")
                        continue

                if not values_to_insert:
                    logger.warning("No valid rates to insert")
                    return

                cur.executemany("""
                    INSERT INTO currency_rates (date, currency_code, rate)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (date, currency_code) DO UPDATE
                    SET rate = EXCLUDED.rate
                """, values_to_insert)
                
                conn.commit()
                logger.info(f"Successfully stored {len(values_to_insert)} currency rates for {date}")

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error while storing rates: {e}")
            raise
        finally:
            if conn:
                conn.close() 
