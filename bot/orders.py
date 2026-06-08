from dataclasses import dataclass, field
from typing import Optional
from bot.client import BinanceFuturesClient, BinanceClientError
from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, validate_stop_price,
)


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = "GTC"


@dataclass
class OrderResult:
    order_id: int
    symbol: str
    side: str
    order_type: str
    status: str
    orig_qty: str
    executed_qty: str
    avg_price: str
    raw: dict

    def is_filled(self):
        return self.status == "FILLED"


def build_order_request(symbol, side, order_type, quantity, price=None, stop_price=None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    stop_price = validate_stop_price(stop_price, order_type)
    return OrderRequest(
        symbol=symbol, side=side, order_type=order_type,
        quantity=quantity, price=price, stop_price=stop_price,
    )


def _parse_result(raw):
    return OrderResult(
        order_id=raw.get("orderId", 0),
        symbol=raw.get("symbol", ""),
        side=raw.get("side", ""),
        order_type=raw.get("type", ""),
        status=raw.get("status", ""),
        orig_qty=raw.get("origQty", "0"),
        executed_qty=raw.get("executedQty", "0"),
        avg_price=raw.get("avgPrice", "0") or raw.get("price", "0"),
        raw=raw,
    )


def place_order(client, request):
    payload = {
        "symbol": request.symbol,
        "side": request.side,
        "type": request.order_type,
        "quantity": request.quantity,
    }
    if request.order_type == "LIMIT":
        payload["price"] = request.price
        payload["timeInForce"] = request.time_in_force
    if request.order_type == "STOP_MARKET":
        payload["stopPrice"] = request.stop_price
    raw = client.place_order(**payload)
    return _parse_result(raw)
