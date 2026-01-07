"""
Module for parsing book data from HTML content.
Includes functions to extract information from both catalogue pods and detailed book pages.
"""

import logging
import re
from typing import Dict, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from book_scraper.config.settings import BASE_SITE, CATALOGUE_SITE

# Module-level logger
logger = logging.getLogger(__name__)


# Parsing catalogue pod HTML


def parse_title(pod: Tag) -> Optional[str]:
    """
    Extracts the book title from a catalogue pod.
    """
    title_tag = pod.find("h3").find("a")
    if title_tag and title_tag.has_attr("title"):
        return title_tag["title"].strip()
    logger.warning("Title not found in pod")
    return None


def parse_url(pod: Tag) -> Optional[str]:
    a_tag = pod.select_one("h3 > a")
    if not a_tag:
        logger.error("a_tag doesnt have h3 > a")
        return None
    href = a_tag.get("href")
    if not href:
        logger.error("no href in a_tag")
        return None
    return urljoin(BASE_SITE, href)


def parse_float(value: str) -> Optional[float]:
    m = re.search(r"[\d.,]+", value)
    if not m:
        return None
    return float(m.group(0).replace(",", ""))


def parse_price(pod: Tag) -> Optional[float]:
    p_tag = pod.select_one("p.price_color")
    if not p_tag:
        return None
    if not p_tag.text:
        return None
    return parse_float(p_tag.text)


def parse_rating(pod: Tag) -> Optional[int]:
    rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    p_tag = pod.select_one("p.star-rating")
    if not p_tag:
        return None
    if len(p_tag["class"]) < 2:
        return None
    rating_str = p_tag["class"][1]
    return rating_dict.get(rating_str)


def parse_availability(pod: Tag) -> Optional[bool]:
    p_tag = pod.select_one("p.instock")
    if not p_tag:
        return None
    if not p_tag.text:
        return None
    return "In stock" in p_tag.text


# Parsing detail page HTML


def parse_category_name(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    un_breadcrumb = soup.select_one("ul.breadcrumb")
    if not un_breadcrumb:
        logger.error("No breadcrumb found in HTML")
        return None
    li_tags = un_breadcrumb.select("li")
    if len(li_tags) < 3:
        logger.error("Breadcrumb does not have enough li tags")
        return None
    category_tag = li_tags[2].select_one("a")
    if not category_tag:
        logger.error("No category link found in breadcrumb")
        return None
    return category_tag.text.strip()


def parse_thumbnail_url(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    img_tag = soup.select_one("div.item.active > img")
    if not img_tag:
        logger.error("No image tag found in HTML")
        return None
    src = img_tag.get("src")
    if not src:
        logger.error("No src attribute found in image tag")
        return None
    return urljoin(CATALOGUE_SITE, src)


def parse_description(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    desc_header = soup.find("h2", string="Product Description")
    if not desc_header:
        logger.error("No product description header found in HTML")
        return None
    desc_paragraph = desc_header.find_next_sibling("p")
    if not desc_paragraph:
        logger.error("No product description paragraph found in HTML")
        return None
    return desc_paragraph.text.strip()


def parse_product_info(html: str) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="table table-striped")
    info: Dict[str, Optional[str]] = {}

    if not table:
        logger.error("No product information table found in HTML")
        return info

    for row in table.find_all("tr"):
        header = row.find("th")
        data = row.find("td")
        if header and data:
            info[header.text.strip()] = data.text.strip()
    return info


def parse_upc(product_info: Dict[str, Optional[str]]) -> Optional[str]:
    return product_info.get("UPC")


def parse_price_excl_tax(product_info: Dict[str, Optional[str]]) -> Optional[float]:
    price_str = product_info.get("Price (excl. tax)")
    if price_str:
        return parse_float(price_str)
    return None


def parse_price_incl_tax(product_info: Dict[str, Optional[str]]) -> Optional[float]:
    price_str = product_info.get("Price (incl. tax)")
    if price_str:
        return parse_float(price_str)
    return None


def parse_tax(product_info: Dict[str, Optional[str]]) -> Optional[float]:
    tax_str = product_info.get("Tax")
    if tax_str:
        return parse_float(tax_str)
    return None


def parse_int(value: str) -> Optional[int]:
    m = re.search(r"[\d]+", value)
    if not m:
        return None
    return int(m.group(0))


def parse_availability_count(product_info: Dict[str, Optional[str]]) -> Optional[int]:
    availability_str = product_info.get("Availability")
    if availability_str:
        return parse_int(availability_str)
    return None


def parse_num_reviews(product_info: Dict[str, Optional[str]]) -> Optional[int]:
    reviews_str = product_info.get("Number of reviews")
    if reviews_str and reviews_str.isdigit():
        return int(reviews_str)
    return None
