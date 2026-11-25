import json
import asyncio

from enkard.enkacard.utils.create_banner_one import generationOne
from enka import GenshinClient, gi
from enkard.enkacard.encbanner import CreateBanner


async def main() -> None:
    async with GenshinClient(gi.Language.ENGLISH) as client:
        response = await client.fetch_showcase(1817389136)
        data = response.model_dump()
        with open("test.json", "w", encoding="utf-8") as f:
                    json.dump(
                        data,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )
        response = CreateBanner(
            data=data,
            custom_image={"Skirk":"https://ik.imagekit.io/cocogoat/1352449904-10000114_WWvIz_L1L"}
        ).generate()

        with open("test_result.json", "w", encoding="utf-8") as f:
            json.dump(
                response,
                f,
                indent=4,
                ensure_ascii=False
            )

        dat = response

        banner = await generationOne(
            dat["Skirk"],
            adapt=True,
        )
        banner.save("test.png")


asyncio.run(main())