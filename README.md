# Currency Rates Application

This application fetches currency exchange rates from the CurrencyAPI.net API and stores them in a PostgreSQL database. The rates are updated daily at 06:00 UTC.

## Features

- Daily automatic currency rate updates
- Historical rate storage
- PostgreSQL database for data persistence
- Docker containerization
- Error handling and logging

## Prerequisites

- Docker and Docker Compose
- CurrencyAPI.net API key (free tier)

## Setup

1. Clone the repository
2. Create a `.env` file in the project root with the following content:

   ```properties
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=currency_db
   DB_USER=postgres
   DB_PASSWORD=admin
   API_KEY=your_api_key_here
   API_URL=https://currencyapi.net/api/v1/rates
   API_BASE_CURRENCY=USD
   ```
**Note:** Make sure to replace `API_KEY` with your actual API key from currencyapi.net

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

## Database Schema

The application uses a single table `currency_rates` with the following structure:

- `id`: Auto-incrementing primary key
- `date`: Date of the exchange rate
- `currency_code`: Three-letter currency code (e.g., EUR, GBP)
- `rate`: Exchange rate value with high precision (20 digits, 10 decimal places)
- `created_at`: Automatic timestamp of record creation
- Unique constraint on `(date, currency_code)` to prevent duplicate entries

## Data Persistence

The PostgreSQL data is persisted using a Docker volume named `postgres_data`. This ensures that data remains available even if the container is deleted and recreated.

## Error Handling

The application includes comprehensive error handling for:
- API connection issues
- Database connection problems
- Invalid data responses
- Duplicate entries

## Logging

All operations are logged with timestamps and appropriate log levels (INFO, ERROR) for monitoring and debugging purposes. 