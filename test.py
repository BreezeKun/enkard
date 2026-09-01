import json
import asyncio

from enkard.enkacard.utils.create_banner_one import generationOne
from enkard.enka import GenshinClient, gi
from enkard.enkacard.encbanner import CreateBanner


async def main() -> None:
    async with GenshinClient(gi.Language.ENGLISH) as client:
        response = await client.fetch_showcase(1817389136)
        data = response.model_dump()

        response = CreateBanner(
            data=data,
            akasha=True
        ).generate()

        with open("test_result.json", "w", encoding="utf-8") as f:
            json.dump(
                response,
                f,
                indent=4,
                ensure_ascii=False
            )

        dat = response

        print(dat["Traveler"])

        banner = await generationOne(
            dat["Traveler"],
            adapt=False,
            lvl="Level",
            uid="1817389136",
            hide_uid=False,
        )

        banner.save("test.png")


asyncio.run(main())