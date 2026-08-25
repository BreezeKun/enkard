import enka
import asyncio
import json

async def main() -> None:
    async with enka.GenshinClient(enka.gi.Language.ENGLISH) as client:
        response = await client.fetch_showcase(1817389136)

        print(type(response))

        with open("test.json", "w") as f:
            json.dump(response.model_dump(), f, indent=4)

asyncio.run(main())