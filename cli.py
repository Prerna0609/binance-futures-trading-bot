import argparse
import os
import sys
import requests
from bot.client import BinanceFuturesClient, BinanceClientError
from bot.logging_config import setup_logging, get_logger
from bot.orders import build_order_request, place_order


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot",
    )
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], type=str.upper)
    parser.add_argument("--type", dest="order_type", required=True,
                        choices=["MARKET", "LIMIT", "STOP_MARKET"], type=str.upper)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float, default=None)
    parser.add_argument("--stop-price", dest="stop_price", type=float, default=None)
    parser.add_argument("--log-dir", default="logs")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(log_dir=args.log_dir)
    logger = get_logger("cli")
    logger.info("Trading bot started | args: %s", vars(args))

    print(f"\n  Symbol   : {args.symbol}")
    print(f"  Side     : {args.side}")
    print(f"  Type     : {args.order_type}")
    print(f"  Quantity : {args.quantity}")
    if args.price:
        print(f"  Price    : {args.price}")
    if args.stop_price:
        print(f"  Stop     : {args.stop_price}")
    print()

    try:
        order_request = build_order_request(
            symbol=args.symbol, side=args.side,
            order_type=args.order_type, quantity=args.quantity,
            price=args.price, stop_price=args.stop_price,
        )
    except ValueError as exc:
        logger.error("Validation failed: %s", exc)
        print(f"  ERROR: {exc}")
        sys.exit(1)

    if args.dry_run:
        print("  Dry-run mode — no order sent.")
        sys.exit(0)

    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        print("  ERROR: Set BINANCE_API_KEY and BINANCE_API_SECRET")
        sys.exit(1)

    client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)

    try:
        client.get_server_time()
    except Exception as exc:
        print(f"  ERROR: Cannot reach Binance Testnet: {exc}")
        sys.exit(1)

    try:
        result = place_order(client, order_request)
    except BinanceClientError as exc:
        print(f"  ERROR: Binance error {exc.code}: {exc.message}")
        sys.exit(1)
    except requests.exceptions.RequestException as exc:
        print(f"  ERROR: Network error: {exc}")
        sys.exit(1)

    print(f"  Order ID     : {result.order_id}")
    print(f"  Status       : {result.status}")
    print(f"  Executed Qty : {result.executed_qty}")
    print(f"  Avg Price    : {result.avg_price}")
    print("\n  Order submitted successfully!")


if __name__ == "__main__":
    main()
