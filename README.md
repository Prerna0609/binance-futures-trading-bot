# Binance Futures Testnet Trading Bot

A Python CLI application to place orders on Binance USDT-M Futures Testnet.

## Features
- MARKET, LIMIT, STOP_MARKET orders (bonus)
- BUY / SELL sides
- Input validation
- Structured logging (file + console)
- Clean layered architecture
- No SDK — pure REST with HMAC-SHA256

## Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Set environment variables
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_secret_key"

## Usage

Market BUY:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

Limit SELL:
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500

Stop-Market BUY (Bonus):
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 95000

Dry run (validate only, no order sent):
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 90000 --dry-run

## Project Structure

trading_bot/
  bot/
    client.py          - Binance API wrapper (auth, signing, HTTP)
    orders.py          - Order logic and response parsing
    validators.py      - Input validation
    logging_config.py  - File + console logging setup
  cli.py               - CLI entry point (argparse)
  logs/                - Log files
  requirements.txt

## Assumptions
- Testnet only: https://testnet.binancefuture.com
- USDT-M Futures endpoints only
- One-way mode (positionSide: BOTH)
- Credentials via environment variables only
