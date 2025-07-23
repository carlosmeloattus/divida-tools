import requests
from typing import Optional
from dataclasses import dataclass

@dataclass
class APIClient:
    base_url: str
    endpoint: str
    auth_url: str
    basic_auth: str
    tenant: str
    user: str
    password: str
    token: Optional[str] = None

    def __post_init__(self):
        self.token = self._login()

    def _login(self) -> str:
        headers = {
            "Authorization": f"Basic {self.basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "password",
            "username": f"{self.user}@{self.tenant}",
            "password": self.password
        }
        url = f"{self.base_url.rstrip('/')}{self.auth_url}"
        resp = requests.post(url, headers=headers, data=data)
        resp.raise_for_status()
        token = resp.json().get("access_token")
        if not token:
            raise RuntimeError(f"Login falhou: {resp.text}")
        return token

    def envia_divida(self, divida_json: dict) -> requests.Response:
        url = f"{self.base_url.rstrip('/')}{self.endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        resp = requests.post(url, json=divida_json, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp
