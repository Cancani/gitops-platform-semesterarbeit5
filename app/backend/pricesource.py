"""Preisquelle für die Preisüberwachung (US08).

Aktuell eine Mock Quelle, die deterministisch plausible Preise für eine feste
Liste digitaler Marktplatzobjekte erzeugt. Damit ist die Demo unabhaengig von
externen APIs (Massnahme zu Risiko R2). Eine echte HTTP Quelle (z.B. Steam
Market) liesse sich ueber dieselbe fetch_prices Schnittstelle anbinden.
"""

import random
from datetime import datetime, timezone

from models import PriceEntry

# Beobachtete Objekte mit Basispreis in USD
WATCHED_ITEMS = {
    "AK-47 Redline": 25.0,
    "AWP Asiimov": 80.0,
    "Glock-18 Fade": 320.0,
    "Karambit Doppler": 950.0,
}


def fetch_prices() -> list[PriceEntry]:
    """Ruft aktuelle Preise ab (Mock mit zufaelliger Schwankung)."""
    now = datetime.now(timezone.utc)
    entries: list[PriceEntry] = []
    for item, base in WATCHED_ITEMS.items():
        variation = random.uniform(-0.05, 0.05)  # plus minus 5 Prozent
        price = round(base * (1 + variation), 2)
        entries.append(
            PriceEntry(
                item_name=item,
                price=price,
                currency="USD",
                source="mock",
                timestamp=now,
            )
        )
    return entries