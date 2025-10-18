import asyncio
import aiohttp


async def get_data(url: str, i: int, path: str):
    print(f"Start {i}")
    full_path = f"{url}/{path}/{i}"
    async with aiohttp.ClientSession() as session:
        async with session.get(full_path) as response:
            print(f"DONE {i}")

# asyncio.run(get_data("http://localhost:8000", 1, "async"))

async def main():
    await asyncio.gather(
        *[get_data("http://localhost:8000", i, "sync") for i in range(300)]
    )

asyncio.run(main())
