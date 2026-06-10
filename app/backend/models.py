"""Pydantic Modelle für die Preisdaten."""

from datetime import datetime
from pydantic import BaseModel, Field


class PriceEntry(BaseModel):
    """Ein einzelner Preisdatenpunkt für ein beobachtetes Objekt."""
    item_name: str
    price: float = Field(gt=0)
    currency: str = "CHF"
    source: str
    image_url: str | None = None
    timestamp: datetime


class PricesResponse(BaseModel):
    """Antwort für aktuelle Preise."""
    prices: list[PriceEntry]


class HistoryResponse(BaseModel):
    """Antwort für historische Preise."""
    history: list[PriceEntry]


class RefreshResponse(BaseModel):
    """Antwort nach einem Preisabruf."""
    fetched: int