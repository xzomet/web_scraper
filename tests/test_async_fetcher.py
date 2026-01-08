# test_async_fetcher.py
import asyncio

from book_scraper.scraping.async_fetcher import AsyncFetcher


async def test():
    fetcher = AsyncFetcher(max_concurrent=3)
    urls = [
        "https://httpbin.org/delay/1",  # Takes 1 second
        "https://httpbin.org/delay/2",  # Takes 2 seconds
        "https://httpbin.org/delay/1",  # Takes 1 second
    ]

    results = await fetcher.fetch_many(urls)
    print(f"Fetched {len([r for r in results if r])} pages")


asyncio.run(test())
