__all__ = ["weaponAdd", 
    "nameBanner", 
    "stats",
    "constant", 
    "create_picture", 
    "talants",
    "naborArtifact", 
    "artifacAdd", 
    "addConst",
    "addTallants", 
    "addArtifact",
    "appedFrame",
    "openUserImg",
    "generationOne",
    ]

import math, re, os, asyncio
from pathlib import Path
from PIL import ImageDraw, Image
from .generation import *
from .function_pills import imgD, imagSize, centrText
from .options import *
from . import open_file

# project root, two levels above this file (.../<package>/utils/create_banner_one.py)
path = str(Path(__file__).resolve().parent.parent.parent)


async def openUserImg(img):
    """
    Accepts either:
      - an already-open PIL Image
      - a URL string
      - a local file path string
      - None
    """
    if img is None:
        return None
    if not isinstance(img, str):
        return img.convert("RGBA")

    linkImg = re.search(r"(?P<url>https?://[^\s]+)", img)
    if linkImg:
        img = await imgD(link=linkImg.group())
    else:
        img = Image.open(os.path.join(path, img))
    return img.convert("RGBA")


async def weaponAdd(weapon, lvlName):
    """
    `weapon` is the "weapon" dict from the new library's output, e.g.:
    {
        "name": "...", "level": 90, "refinement": 3, "image": "https://...",
        "rarity": 5,
        "stats": {"Base ATK": {"is_percentage": false, "formatted_value": "608"},
                   "CRIT Rate": {"is_percentage": true, "formatted_value": "33.1%"}}
    }
    """
    if not weapon:
        return None

    WeaponBg = open_file.WeaponBgTeampleOne.copy().convert("RGBA")
    WeaponBgUp = open_file.WeaponBgUpTeampleOne.copy().convert("RGBA")
    d = ImageDraw.Draw(WeaponBg)

    name = weapon["name"]
    lvl = weapon["level"]
    lvlUp = weapon["refinement"]

    statItems = list(weapon.get("stats", {}).items())
    baseAtt = statItems[0][1]["formatted_value"] if statItems else "0"
    dopStatName, dopStatInfo = statItems[1] if len(statItems) > 1 else (None, None)

    imageStats = None
    dopStat = "0"
    if dopStatInfo:
        dopStat = dopStatInfo.get("formatted_value", "0")
        imageStats = getIconAdd(
            dopStatName, size=(26, 26), is_percentage=bool(dopStatInfo.get("is_percentage"))
        )

    if imageStats:
        WeaponBg.alpha_composite(imageStats, (300, 53))

    stars = star(weapon["rarity"])
    image = await imagSize(link=weapon["image"], size=(114, 121))
    WeaponBg.alpha_composite(image, (0, 0))
    WeaponBg.alpha_composite(WeaponBgUp, (0, 0))

    position, font = await centrText(name, witshRam=315, razmer=24, start=159, Yram=30, y=13)
    d.text(position, str(name), font=font, fill=coloring)
    d.text((435, 53), f"R{lvlUp}", font=fontSize(24), fill=(248, 199, 135, 255))
    position, font = await centrText(f"{lvlName}: {lvl}/90", witshRam=152, razmer=17, start=235, Yram=28, y=90)
    d.text(position, f"{lvlName}: {lvl}/90", font=font, fill=coloring)

    position, font = await centrText(str(baseAtt), witshRam=90, razmer=24, start=180, Yram=30, y=50)
    d.text(position, str(baseAtt), font=font, fill=coloring)

    # `formatted_value` already carries the "%" for percentage stats, no need to add one.
    position, font = await centrText(str(dopStat), witshRam=90, razmer=24, start=320, Yram=30, y=50)
    d.text(position, str(dopStat), font=font, fill=coloring)

    WeaponBg.alpha_composite(stars, (0, 0))
    return WeaponBg


async def nameBanner(character, lvlName):
    NameBg = open_file.NameBgTeampleOne.copy().convert("RGBA")
    d = ImageDraw.Draw(NameBg)
    name = character["name"]
    centrName, fonts = await centrText(name, witshRam=220, razmer=33, start=2)
    d.text((centrName, 28), name, font=fonts, fill=coloring)
    d.text((187, -1), str(character.get("friendship_level", 0)), font=fontSize(24), fill=coloring)
    centrName, fonts = await centrText(f"{lvlName}: {character['level']}/90", witshRam=148, razmer=17, start=5)
    d.text((centrName, 2), f"{lvlName}: {character['level']}/90", font=fonts, fill=coloring)
    stars = star(character["rarity"])
    NameBg.alpha_composite(stars, (59, 68))
    return NameBg


async def _drawStatRow(AttributeBg, name, info, position):
    Attribute = open_file.AttributeTeampleOne.copy().convert("RGBA")
    d = ImageDraw.Draw(Attribute)

    isPerc = bool(info.get("is_percentage"))
    iconImg = getIconAdd(name, is_percentage=isPerc)
    if iconImg:
        icon = await imagSize(image=iconImg, fixed_width=23)
        Attribute.alpha_composite(icon, (4, 0))

    value = str(info.get("value", ""))
    pX, fnt = await centrText(value, witshRam=119, razmer=20, start=325)
    d.text((pX, 3), value, font=fnt, fill=coloring)
    d.text((42, 4), name, font=fontSize(18), fill=coloring)

    AttributeBg.alpha_composite(Attribute, position)
    return AttributeBg


async def stats(character):
    """
    `character["stats"]` is now a dict of {display_name: {"value": "...", "is_percentage": bool}}
    (see test_result.json) instead of the old list of (FIGHT_PROP_id, StatObject) tuples.
    """
    statsData = character.get("stats", {})
    postion = (26, 37)
    AttributeBg = open_file.AttributeBgTeampleOne.copy().convert("RGBA")
    drawn = set()

    # Max HP / ATK / DEF are always drawn first, same as the original template.
    for name in PRIMARY_STATS:
        info = statsData.get(name)
        if not info:
            continue
        AttributeBg = await _drawStatRow(AttributeBg, name, info, postion)
        postion = (postion[0], postion[1] + 39)
        drawn.add(name)

    # Only one elemental DMG Bonus stat is ever shown - keep the highest valued one,
    # same behaviour as the original code picking the max among ids 40-46.
    elementalBonuses = {k: v for k, v in statsData.items() if k in ELEMENT_DMG_ICON_MAP}
    bestElemental = None
    if elementalBonuses:
        bestElemental = max(elementalBonuses.items(), key=lambda kv: parseStatValue(kv[1].get("value")))

    for name, info in statsData.items():
        if name in drawn or name in STAT_SKIP:
            continue
        if name in ELEMENT_DMG_ICON_MAP:
            if not bestElemental or name != bestElemental[0]:
                continue
        elif (name, bool(info.get("is_percentage"))) not in STAT_ICON_MAP:
            # not one of the recognised "extra" stats for this panel - skip it
            continue

        if parseStatValue(info.get("value")) == 0:
            continue

        AttributeBg = await _drawStatRow(AttributeBg, name, info, postion)
        postion = (postion[0], postion[1] + 39)
        drawn.add(name)

    return AttributeBg


async def constant(character, element):
    constantRes = []
    for key in character.get("constellations", []):
        closeConstBg = open_file.ClossedBg.copy().convert("RGBA")
        closeConsticon = open_file.Clossed.copy().convert("RGBA")
        openConstBg = openImageElementConstant(element).convert("RGBA")
        imageIcon = await imgD(link=key["icon"])
        imageIcon = imageIcon.resize((43, 48))
        if not key.get("unlocked"):
            closeConstBg.alpha_composite(imageIcon, (19, 20))
            closeConstBg.alpha_composite(closeConsticon, (-1, 0))
            const = closeConstBg
        else:
            openConstBg.alpha_composite(imageIcon, (19, 20))
            const = openConstBg
        constantRes.append(const)
    return constantRes


async def create_picture(character, adapt, splash=None):
    element = character["element"]
    customImage = character.get("custom_image")
    imgs = (await openUserImg(customImage)) if customImage else await openUserImg(character["icon"].get("gacha"))

    if imgs:
        frame = userImage(imgs, element=element, adaptation=adapt)
    else:
        # no custom crop supplied - fall back to a full splash image
        link = splash or (character.get("namecard") or {}).get("full") or character["icon"]["gacha"]
        banner = await imagSize(link=link, size=(2048, 1024))
        frame = maskaAdd(element, banner)
    return frame


async def talants(character):
    count = 0
    tallantsRes = []
    for key in character.get("talents", []):
        if key["level"] > 9:
            talantsBg = open_file.TalantsFrameGoldLvlTeampleOne.copy().convert("RGBA")
        else:
            talantsBg = open_file.TalantsFrameTeampleOne.copy().convert("RGBA")
        talantsCount = open_file.TalantsCountTeampleOne.copy().convert("RGBA")
        d = ImageDraw.Draw(talantsCount)
        imagesIconTalants = await imgD(link=key["icon"])
        imagesIconTalants = imagesIconTalants.resize((50, 50))
        talantsBg.alpha_composite(imagesIconTalants, (8, 7))

        lvlText = str(key["level"])
        if len(lvlText) == 2:
            d.text((6, -1), lvlText, font=fontSize(15), fill=(248, 199, 135, 255))
        else:
            d.text((9, -1), lvlText, font=fontSize(15), fill=(248, 199, 135, 255))

        talantsBg.alpha_composite(talantsCount, (19, 53))
        tallantsRes.append(talantsBg)
        count += 1
        if count == 3:
            break
    return tallantsRes


async def naborArtifact(info, ArtifactNameBg):
    """`info` is the "arti_count" dict: {"Set Name": count, ...}"""
    naborAll = []
    for key in info:
        if info[key] > 1:
            ArtifactNameFrame = open_file.ArtifactNameFrameTeampleOne.copy().convert("RGBA")
            d = ImageDraw.Draw(ArtifactNameFrame)
            centrName, fonts = await centrText(key, witshRam=240, razmer=15, start=4, Yram=24, y=1)
            d.text(centrName, str(key), font=fonts, fill=coloring)
            d.text((267, -2), str(info[key]), font=fontSize(24), fill=coloring)
            naborAll.append(ArtifactNameFrame)
    position = (151, 34)
    for key in naborAll:
        if len(naborAll) == 1:
            ArtifactNameBg.alpha_composite(key, (151, 54))
        else:
            ArtifactNameBg.alpha_composite(key, position)
            position = (position[0], position[1] + 29)
    return ArtifactNameBg


async def creatDopStat(subStats):
    """`subStats` is a list of {"name","formatted_value","is_percentage"} dicts."""
    res = []
    for key in subStats:
        name = key["name"]
        isPerc = bool(key.get("is_percentage"))
        imageStats = getIconAdd(name, is_percentage=isPerc)
        if not imageStats:
            continue

        v = f"+{key['formatted_value']}"
        ArtifactDopStat = open_file.ArtifactDopValueTeampleOne.copy().convert("RGBA")
        imageStats = await imagSize(image=imageStats, fixed_width=17)
        ArtifactDopStat.alpha_composite(imageStats, (3, 1))
        px, fnt = await centrText(v, witshRam=142, razmer=24, start=33)
        d = ImageDraw.Draw(ArtifactDopStat)
        d.text((px, -2), v, font=fnt, fill=coloring)
        res.append(ArtifactDopStat)

    return res


async def creatArtifact(artifact):
    """`artifact` is one entry from the "artifact" list."""
    dopVaulImg = await creatDopStat(artifact.get("sub_stats", []))
    ArtifactBgUp = open_file.ArtifactBgUpTeampleOne.copy().convert("RGBA")
    ArtifactBg = open_file.ArtifactBgTeampleOne.copy().convert("RGBA")
    artimg = await imagSize(link=artifact["image"], size=(175, 175))
    ArtifactBg.alpha_composite(artimg, (-32, -27))
    ArtifactBg.alpha_composite(ArtifactBgUp, (0, 0))
    d = ImageDraw.Draw(ArtifactBg)

    mainStat = artifact["main_stat"]
    val = mainStat["value"]
    centrName, fonts = await centrText(str(val), witshRam=52, razmer=17, start=65)
    d.text((centrName, 62), str(val), font=fonts, fill=coloring)

    imageStats = getIconAdd(mainStat["name"], size=(19, 24), is_percentage=bool(mainStat.get("is_percentage")))
    if imageStats:
        ArtifactBg.alpha_composite(imageStats, (3, 0))

    d.text((77, 82), str(artifact["level"]), font=fontSize(17), fill=coloring)
    starsImg = star(artifact["rarity"])
    ArtifactBg.alpha_composite(starsImg, (16, 96))

    positions = (159, 8)
    for k in dopVaulImg:
        ArtifactBg.alpha_composite(k, positions)
        positions = (positions[0], positions[1] + 28)
    return ArtifactBg


async def artifacAdd(character):
    artifacRes = []
    ArtifactNameBg = open_file.ArtifactNameBgTeampleOne.copy().convert("RGBA")
    for artifact in character.get("artifact", []):
        artifacRes.append(await creatArtifact(artifact))

    rezArtSet = await naborArtifact(character.get("arti_count", {}), ArtifactNameBg)
    return {"artifact": artifacRes, "nabor": rezArtSet}


def addConst(frameConst, constantRes):
    position = (2, 157)
    for key in constantRes:
        frameConst.alpha_composite(key, (position[0], position[1]))
        position = (position[0], position[1] + 84)
    return frameConst


def addTallants(frameTallants, talatsRes):
    positionAddTallants = (530, 342)
    for key in talatsRes:
        frameTallants.alpha_composite(key, (positionAddTallants[0], positionAddTallants[1]))
        positionAddTallants = (positionAddTallants[0], positionAddTallants[1] + 95)
    return frameTallants


def addArtifact(frameArtifact, artifacRes):
    position = (1141, 42)
    for key in artifacRes:
        frameArtifact.alpha_composite(key, (position[0], position[1]))
        position = (position[0], position[1] + 143)
    return frameArtifact



async def appedFrame(frame, weaponRes, nameRes, statRes, constantRes, talatsRes, artifacRes, artifactSet):
    banner = addConst(frame.convert("RGBA"), constantRes)
    banner = addTallants(banner, talatsRes)
    banner = addArtifact(banner, artifacRes)
    if weaponRes:
        # weaponAdd() now returns None when the character has no weapon entry
        banner.alpha_composite(weaponRes, (610, 39))
    banner.alpha_composite(nameRes, (138, 646))
    banner.alpha_composite(statRes, (610, 189))
    banner.alpha_composite(artifactSet, (610, 617))
    return banner


async def generationOne(character, adapt=False, lvl="Level", uid=None, hide_uid=True, splash=None):
    """
    Entry point matching the new library's output shape - pass in one character's
    dict, e.g. `data["Skirk"]` from test_result.json.
    """
    element = character["element"]

    task = [
        create_picture(character, adapt, splash),
        weaponAdd(character.get("weapon"), lvl),
        stats(character),
        constant(character, element),
        talants(character),
        artifacAdd(character),
    ]

    try:
        frame, weaponRes, statRes, constantRes, talatsRes, artifactData = await asyncio.gather(*task)
        nameRes = await nameBanner(character, lvl)

        result = await appedFrame(
            frame, weaponRes, nameRes, statRes, constantRes, talatsRes,
            artifactData["artifact"], artifactData["nabor"]
        )
        return result
    except Exception as e:
        raise