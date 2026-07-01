"""Preisquelle für die Preisüberwachung.

Primär werden Preise über die Steam Market API abgerufen. Bei Nichtverfügbarkeit
der API greift ein Mock-Fallback mit plausiblen Basispreisen. Die Bild URLs
zeigen auf das echte Steam CDN.
"""

import logging
import random
from datetime import datetime, timezone

import httpx

from models import PriceEntry

logger = logging.getLogger(__name__)

STEAM_CDN = "https://community.cloudflare.steamstatic.com/economy/image"
STEAM_API = "https://steamcommunity.com/market/priceoverview/"
EUR_TO_CHF = 0.96

_ICON_AK47 = (
    "i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3Uql"
    "XOLrxM-vMGmW8VNxu5Dx60noTyLwlcK3wiFO0POlPPNSI_-RHGavzOtyufRkASq2lkxx"
    "4W-HnNyqJC3FZwYoC5p0Q7FfthW6wdWxPu-371Pdit5HnyXgznQeHYY5wyA"
)
_ICON_AWP = (
    "i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3Uql"
    "XOLrxM-vMGmW8VNxu5Dx60noTyLwiYbf_jdk7uW-V6V-Kf2cGFidxOp_pewnF3nhxEt0"
    "sGnSzN76dH3GOg9xC8FyEORftRe-x9PuYurq71bW3d8UnjK-0H0YSTpMGQ"
)
_ICON_DEAGLE = (
    "i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3Uql"
    "XOLrxM-vMGmW8VNxu5Dx60noTyL1m5fn8Sdk7vORbqhsLfWAMWuZxuZi_uI_TX6wxxkj"
    "sGXXnImsJ37COlUoWcByEOMOtxa5kdXmNu3htVPZjN1bjXKpkHLRfQU"
)
_ICON_USP = (
    "i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3Uql"
    "XOLrxM-vMGmW8VNxu5Dx60noTyLkjYbf7itX6vytbbZSI-WsG3SA_uV_vO1WTCa9kxQ1"
    "vjiBpYL8JSLSMxghCMEjEeNe5hHpw9zhYuOz5VfcitpBmyqt3X9O6itrsesFUfYmrKzTkUifZqPQtnZK"
)

WATCHED_ITEMS = {
    "AK-47 | Redline (Field-Tested)": {"base": 34.78, "icon": _ICON_AK47},
    "AWP | Asiimov (Field-Tested)": {"base": 141.87, "icon": _ICON_AWP},
    "Desert Eagle | Blaze (Factory New)": {"base": 886.34, "icon": _ICON_DEAGLE},
    "USP-S | Kill Confirmed (Field-Tested)": {"base": 74.52, "icon": _ICON_USP},
}


def _image_url(icon: str) -> str:
    """Baut die Steam CDN Bild URL aus dem icon_url Hash."""
    return f"{STEAM_CDN}/{icon}/360fx360f"


def _fetch_steam_price(name: str) -> float | None:
    """Ruft den aktuellen Preis von der Steam Market API ab."""
    try:
        response = httpx.get(
            STEAM_API,
            params={"currency": 3, "appid": 730, "market_hash_name": name},
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("success"):
            return None
        raw = data.get("lowest_price", "")
        price_str = raw.replace("CHF", "").replace(",", ".").strip()
        return round(float(price_str), 2)
    except Exception:
        return None


def fetch_prices() -> list[PriceEntry]:
    """Ruft aktuelle Preise ab. Steam API primär, Mock als Fallback."""
    now = datetime.now(timezone.utc)
    entries: list[PriceEntry] = []
    for name, meta in WATCHED_ITEMS.items():
        price = _fetch_steam_price(name)
        if price is not None:
            source = "steam"
        else:
            logger.warning("Steam API nicht verfügbar für %s, verwende Mock", name)
            variation = random.uniform(-0.05, 0.05)
            price = round(meta["base"] * (1 + variation), 2)
            source = "mock"
        entries.append(
            PriceEntry(
                item_name=name,
                price=price,
                currency="CHF",
                source=source,
                image_url=_image_url(meta["icon"]),
                timestamp=now,
            )
        )
    return entries