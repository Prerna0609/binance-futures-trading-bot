import hashlib
import hmac
import time
from urllib.parse import urlencode
import requests

BASE_URL = "https://testnet.binancefuture.com"
RECV_WINDOW = 5000


class BinanceClientError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"Binance API error {code}: {message}")


class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, base_url=BASE_URL):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({
            "X-MBX-APIKEY": self._api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params):
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = RECV_WINDOW
        query_string = urlencode(params)
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method, endpoint, params=None, signed=False):
        params = params or {}
        if signed:
            params = self._sign(params)
        url = f"{self._base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = self._session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self._session.post(url, data=params, timeout=10)
            elif method.upper() == "DELETE":
                response = self._session.delete(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                err = response.json()
                raise BinanceClientError(err.get("code", -1), err.get("msg", "Unknown"))
            except Exception:
                raise
        data = response.json()
        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceClientError(data["code"], data.get("msg", "Unknown error"))
        return data

    def get_server_time(self):
        data = self._request("GET", "/fapi/v1/time")
        return data["serverTime"]

    def place_order(self, **kwargs):
        params = {k: v for k, v in kwargs.items() if v is not None}
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)

    def get_open_orders(self, symbol=None):
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/fapi/v1/openOrders", params=params, signed=True)
