"""Preisquelle für die Preisüberwachung.

Aktuell eine Mock Quelle, die plausible Preise für eine feste Liste von
CS2 Marktplatzobjekten erzeugt. Die Schwankung erfolgt um einen realistischen
Basispreis. Damit ist die Demo unabhängig von externen APIs (Massnahme zu
Risiko R2). Die Bild URLs zeigen auf das echte Steam CDN (icon_url Hashes
stammen aus der Steam Market API).

Eine echte HTTP Quelle (Steam Market priceoverview) lässt sich später über
dieselbe fetch_prices Schnittstelle anbinden, ohne die übrige Anwendung zu
ändern.
"""

import random
from datetime import datetime, timezone

from models import PriceEntry

STEAM_CDN = "https://community.cloudflare.steamstatic.com/economy/image"

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


def fetch_prices() -> list[PriceEntry]:
    """Ruft aktuelle Preise ab (Mock mit zufälliger Schwankung)."""
    now = datetime.now(timezone.utc)
    entries: list[PriceEntry] = []
    for name, meta in WATCHED_ITEMS.items():
        variation = random.uniform(-0.05, 0.05)
        price = round(meta["base"] * (1 + variation), 2)
        entries.append(
            PriceEntry(
                item_name=name,
                price=price,
                currency="CHF",
                source="mock",
                image_url=_image_url(meta["icon"]),
                timestamp=now,
            )
        )
    return entries
