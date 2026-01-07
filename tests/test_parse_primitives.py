from bs4 import BeautifulSoup

from book_scraper.scraping.parse_primitives import (
    parse_availability,
    parse_price,
    parse_rating,
    parse_title,
    parse_url,
)

# Happy path tests for parse primitives


def test_happy_path_parse_title():
    html = """
         <article class="product_pod">
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    title = parse_title(pod)
    assert title == "A Light in the Attic"


def test_happy_path_parse_url():
    html = """
         <article class="product_pod">
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    url = parse_url(pod)
    assert (
        url
        == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )


def test_happy_path_parse_availability():
    html = """
        <article class="product_pod">
            <p class="instock availability">
                In stock (22 available)
            </p>
        </article>
    """

    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    availability = parse_availability(pod)
    assert availability


def test_happy_path_parse_price():
    html = """
         <article class="product_pod">
            <div class="product_price">
                <p class="price_color">£51.77</p>
            </div>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    price = parse_price(pod)
    assert price == 51.77


def test_happy_path_parse_rating():
    html = """
     <article class="product_pod">
        <p class="star-rating Three">
        </p>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    rating = parse_rating(pod)
    assert rating == 3


# Missing data tests for parse primitives
def test_missing_data_parse_price():
    html = """
     <article class="product_pod">
        <div class="product_price">
            <p class="price_color"></p>
        </div>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    price = parse_price(pod)
    assert price is None


def test_missing_data_parse_rating():
    html = """
     <article class="product_pod">
        <p class="star-rating ">
        </p>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    rating = parse_rating(pod)
    assert rating is None


def test_missing_data_parse_availability():
    html = """
     <article class="product_pod">
        <p class="instock availability">
            Out of stock
        </p>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    availability = parse_availability(pod)
    assert availability == False


def test_missing_data_parse_title():
    html = """
     <article class="product_pod">
        <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title=""></a></h3>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    title = parse_title(pod)
    assert title == ""


def test_missing_data_parse_url():
    html = """
     <article class="product_pod">
        <h3><a title="A Light in the Attic">A Light in the Attic</a></h3>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    url = parse_url(pod)
    assert url is None


# Malformed HTML tests for parse primitives


def test_malformed_html_parse_title():
    html = """
     <article class="product_pod">
        <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    title = parse_title(pod)
    assert title == "A Light in the Attic"


def test_malformed_html_parse_price():
    html = """
     <article class="product_pod">
        <div class="product_price">
            <p class="price_color">£51.77
        </div>
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    price = parse_price(pod)
    assert price == 51.77


def test_malformed_html_parse_availability():
    html = """
     <article class="product_pod">
        <p class="instock availability">
            In stock (22 available)
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    availability = parse_availability(pod)
    assert availability == True


def test_malformed_html_parse_rating():
    html = """
     <article class="product_pod">
        <p class="star-rating Three"
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    rating = parse_rating(pod)
    assert rating == 3


def test_malformed_html_parse_url():
    html = """
     <article class="product_pod">
        <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic
        </article>
     """
    soup = BeautifulSoup(html, "lxml")
    pod = soup.select_one("article.product_pod")
    url = parse_url(pod)
    assert (
        url
        == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
