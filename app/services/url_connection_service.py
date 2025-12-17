import requests

class UrlConnectionService:
    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    def fetch(self) -> str:
        response = requests.get(self.url, timeout=self.timeout)
        response.raise_for_status()
        return response.text