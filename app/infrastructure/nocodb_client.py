from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class NocoDbClient:
    """Простой HTTP‑клиент для работы с NocoDB API."""

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None) -> None:
        self.base_url = (base_url or os.getenv("NOCODB_BASE_URL", "")).rstrip("/")
        self.token = token or os.getenv("NOCODB_TOKEN")

        if not self.base_url:
            raise RuntimeError("Не задан NOCODB_BASE_URL для NocoDbClient.")

    def _build_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.token:
            headers["xc-token"] = self.token
        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: int = 15,
    ) -> Any:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=self._build_headers(),
            params=params,
            json=json,
            timeout=timeout,
        )

        if not response.ok:
            raise RuntimeError(
                f"NocoDB API error: {response.status_code} {response.text}"
            )

        if response.content:
            return response.json()

        return None

