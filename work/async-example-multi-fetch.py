import asyncio
import aiohttp

from decorators import decorator

@decorator
async def fetch_url(session, url):
    async with session.get(url) as response:
        content = await response.text()
        print(f"Fetched {url} with length {len(content)}")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        await asyncio.gather(*tasks)

# Usage
urls = ["http://example.com", "http://example.org", "http://example.net"]
asyncio.run(main(urls))
