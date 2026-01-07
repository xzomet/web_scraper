from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    # fetched from list pages
    id: Optional[int] = None
    title: str = ""
    url: str = ""
    list_price: Optional[float] = None
    availability: Optional[bool] = None
    rating: Optional[int] = None

    # detail page
    upc: Optional[str] = None
    price_excl_tax: Optional[float] = None
    price_incl_tax: Optional[float] = None
    tax: Optional[float] = None
    availability_count: Optional[int] = None
    num_reviews: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

    scraped_at: datetime = field(default_factory=datetime.utcnow)
