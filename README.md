### A library to create genshin character build cards [ref: example/]

## installation
```shell
pip install git+https://github.com/BreezeKun/enkard.git
```

### Usage:
```python
import json
import asyncio
from enkard.enkacard.utils.create_banner_one import generationOne
from enkard.enka import GenshinClient, gi
from enkard.enkacard.encbanner import CreateBanner

async def main() -> None:
    async with GenshinClient(gi.Language.ENGLISH) as client:
        response = await client.fetch_showcase(1817389136)
        data = response.model_dump()
        response = CreateBanner(data=data, akasha=True, custom_image={"Skirk":"https://skirk.png"}).generate()
        with open("test_result.json", "w", encoding="utf-8") as f:
                    json.dump(response, f, indent=4, ensure_ascii=False)
                    
        for name, dat in response.items():
            banner = await generationOne(
                dat,
                adapt=False,
            )
            banner.save(f"{name}.png")

asyncio.run(main())
#custom image - {char1:https..,char2:https...}
#akasha - check test_result.json i havnt added it in card
```

### Template Example
<img src = "example/skirk_card.png">hmm</img>

<marquee>Note: This is not final version of what i want to create it might have issues</marquee><br>
report: Tg- https://t.me/+Drq73Q20_f9hYmJl
