import json

from websocket import WebSocket


class SocketConnection:
    def __init__(self, config):
        self.config = config
        self.socket = WebSocket()

    def connect(self, bot_count: int = 1):
        self.socket.connect(self.config["server_url"])
        self.send_intro(bot_count)

    def send_intro(self, bot_count: int):
        self.socket.send(json.dumps(self.__wrap_data(
            "",
            data={"useraccounts": bot_count},
            operation="handshake"
        )))

    def request_pixel(self, placer):
        username = placer.username

        self.socket.send(json.dumps(self.__wrap_data(username)))
        print("request send!")
        res = self.socket.recv()
        print(res)
        res = json.loads(res)

        if res.get("operation") != "place-pixel":
            return None
        else:
            return res["data"]

    @staticmethod
    def __wrap_data(username: str, data: dict = None, operation: str = "request-pixel") -> dict:
        return {
            "operation": operation,
            "data": data or {},
            "user": username
        }

    def close(self):
        self.socket.close()
