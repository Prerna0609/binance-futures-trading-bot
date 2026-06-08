import logging

logger = logging.getLogger("trading_bot.validators")

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol):
    symbol = symbol.strip().upper()
    if len(symbol) < 4:
        raise ValueError(f"Symbol '{symbol}' looks too short. Example: BTCUSDT")
    return symbol


def validate_side(side):
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL. Got: '{side}'")
    return side


def validate_order_type(order_type):
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be MARKET, LIMIT or STOP_MARKET. Got: '{order_type}'")
    return order_type


def validate_quantity(quantity):
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Quantity must be a number. Got: '{quantity}'")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {qty}")
    return qty


def validate_price(price, order_type):
    if order_type in ("MARKET", "STOP_MARKET"):
        return None
    if price is None:
        raise ValueError(f"Price is required for {order_type} orders.")
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Price must be a number. Got: '{price}'")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0. Got: {p}")
    return p


def validate_stop_price(stop_price, order_type):
    if order_type != "STOP_MARKET":
        return None
    if stop_price is None:
        raise ValueError("stopPrice is required for STOP_MARKET orders.")
    try:
        sp = float(stop_price)
    except (TypeError, ValueError):
        raise ValueError(f"stopPrice must be a number. Got: '{stop_price}'")
    if sp <= 0:
        raise ValueError(f"stopPrice must be greater than 0. Got: {sp}")
    return sp
