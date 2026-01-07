from datetime import datetime

from bs4 import Tag

from book_scraper.models.book import Book
from book_scraper.scraping.parse_primitives import (
    parse_availability,
    parse_availability_count,
    parse_category_name,
    parse_description,
    parse_num_reviews,
    parse_price,
    parse_price_excl_tax,
    parse_price_incl_tax,
    parse_product_info,
    parse_rating,
    parse_tax,
    parse_thumbnail_url,
    parse_title,
    parse_url,
)


class BookBuilder:
    def __init__(self) -> None:
        self._data = {}

    def with_catalogue_pod(self, pod: Tag) -> "BookBuilder":
        self._data["url"] = parse_url(pod)
        self._data["title"] = parse_title(pod)
        self._data["list_price"] = parse_price(pod)
        self._data["rating"] = parse_rating(pod)
        self._data["availability"] = parse_availability(pod)
        return self

    def with_detail_html(self, html: str) -> "BookBuilder":
        self._data["description"] = parse_description(html)
        self._data["category_name"] = parse_category_name(html)
        self._data["thumbnail_url"] = parse_thumbnail_url(html)
        product_info = parse_product_info(html)
        self._data["price_excl_tax"] = parse_price_excl_tax(product_info)
        self._data["price_incl_tax"] = parse_price_incl_tax(product_info)
        self._data["tax"] = parse_tax(product_info)
        self._data["num_reviews"] = parse_num_reviews(product_info)
        self._data["availability_count"] = parse_availability_count(product_info)
        return self

    def build(self) -> Book:
        REQUEIRED_FIELDS = ["url", "title"]
        for field in REQUEIRED_FIELDS:
            if field not in self._data:
                raise ValueError(f"Missing required field: {field}")
        self._data["scraped_at"] = datetime.utcnow()
        return Book(**self._data)
