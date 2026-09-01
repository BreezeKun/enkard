import asyncio
import random
import os
import datetime
from typing import Optional
from collections import Counter


from collections import Counter
from typing import Optional


class GenereteData:
    def __init__(self, data: dict, custom_image:Optional[dict], akasha_data:Optional[dict]):
        self.data = data or {}
        self.custom_image = custom_image
        self.main_data = {}
        self.akasha_data = akasha_data

    def gen_character(self):
        calculated_types = {
            2000,  # Max HP
            2001,  # ATK
            2002,  # DEF
            20,    # CRIT Rate
            22,    # CRIT DMG
            23,    # Energy Recharge
            28,    # Elemental Mastery
        }

        for character in self.data.get("characters") or []:

            # Basic character information

            icon = character.get("icon") or {}
            namecard = character.get("namecard") or {}

            data = {
                "name": character.get("name"),
                "level": character.get("level"),
                "max_level": 90,
                "ascension": character.get("ascension"),
                "friendship_level": character.get("friendship_level"),
                "custom_image": self.custom_image.get(character["name"]) if self.custom_image else None,
                "ranking":None,
                "icon": {
                    "side": icon.get("side"),
                    "circle": icon.get("circle"),
                    "gacha": icon.get("gacha"),
                    "front": icon.get("front"),
                },

                "element": character.get("element"),
                "rarity": character.get("rarity"),

                "namecard": {
                    "icon": namecard.get("icon"),
                    "full": namecard.get("full"),
                },

                "costume": character.get("costume"),

                "stats": {},
                "artifact": [],
                "arti_count": {},
                "weapon": {},

                "constellations": [],
                "constellations_unlocked": character.get(
                    "constellations_unlocked"
                ),

                "talents": [],
            }

            #ranking
            if self.akasha_data:
                for akasha_character in self.akasha_data.get("data") or []:
                    if akasha_character.get("name") == character.get("name"):

                        fit = (akasha_character.get("calculations") or {}).get("fit") or {}

                        ranking = fit.get("ranking")
                        out_of = fit.get("outOf")

                        if ranking is not None and out_of:
                            data["ranking"] = {
                                "rank": ranking,
                                "outOf": out_of,
                                "rank%": round((ranking / out_of) * 100, 2),
                            }

                        break


            # Artifacts

            artifacts = character.get("artifacts") or []

            for artifact in artifacts:

                if not artifact:
                    continue

                main_stat = artifact.get("main_stat") or {}

                sub_stats = artifact.get("sub_stats") or []

                arti = {
                    "name": artifact.get("set_name"),
                    "level": artifact.get("level"),
                    "rarity": artifact.get("rarity"),
                    "type": artifact.get("equip_type"),
                    "image": artifact.get("icon"),

                    "main_stat": {
                        "name": main_stat.get("name"),
                        "value": main_stat.get("formatted_value"),
                        "is_percentage": main_stat.get("is_percentage"),
                    },

                    "sub_stats": [
                        {
                            "formatted_value": sub_stat.get(
                                "formatted_value"
                            ),
                            "is_percentage": sub_stat.get(
                                "is_percentage"
                            ),
                            "name": sub_stat.get("name"),
                        }
                        for sub_stat in sub_stats
                        if sub_stat
                    ],
                }

                data["artifact"].append(arti)

            # Artifact set count

            data["arti_count"] = dict(
                Counter(
                    artifact["name"]
                    for artifact in data["artifact"]
                    if artifact.get("name")
                )
            )

            # Weapon

            weapon = character.get("weapon")

            if weapon:

                weapon_stats = weapon.get("stats") or []

                data["weapon"] = {
                    "name": weapon.get("name"),
                    "level": weapon.get("level"),
                    "refinement": weapon.get("refinement"),
                    "image": weapon.get("icon"),
                    "rarity": weapon.get("rarity"),

                    "stats": {
                        stat.get("name"): {
                            "is_percentage": stat.get(
                                "is_percentage"
                            ),
                            "formatted_value": stat.get(
                                "formatted_value"
                            ),
                        }
                        for stat in weapon_stats
                        if stat and stat.get("name")
                    },
                }

            # Character stats

            character_stats = character.get("stats") or {}

            data["stats"] = {
                stat.get("name"): {
                    "value": stat.get("formatted_value"),
                    "is_percentage": stat.get("is_percentage"),
                }
                for stat in character_stats.values()
                if (
                    stat
                    and stat.get("type") in calculated_types
                    and stat.get("name")
                )
            }

            #adding specal stats

            specialized_stat = character.get("specialized_stat")

            if specialized_stat and round(specialized_stat.get("value", 0)) != 0:
                data["stats"][specialized_stat["name"]] = {
                    "value": specialized_stat["formatted_value"],
                    "is_percentage": specialized_stat["is_percentage"],
                }

            # Constellations

            constellations = character.get("constellations") or []

            data["constellations"] = [
                {
                    "id": constellation.get("id"),
                    "name": constellation.get("name"),
                    "icon": constellation.get("icon"),
                    "unlocked": constellation.get("unlocked"),
                }
                for constellation in constellations
                if constellation
            ]

            # Talents

            talents = character.get("talents") or []

            data["talents"] = [
                {
                    "id": talent.get("id"),
                    "name": talent.get("name"),
                    "level": talent.get("level"),
                    "icon": talent.get("icon"),
                    "is_upgraded": talent.get("is_upgraded"),
                }
                for talent in talents
                if talent
            ]

            # Save character

            name = character.get("name")

            if name:
                self.main_data[name] = data

        return self.main_data

def get_akasha(uid):
    import subprocess
    import json

    url = f"https://akasha.cv/api/getCalculationsForUser/{uid}"

    headers = [
        "-H",
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36",

        "-H",
        "Accept: application/json",

        "-H",
        "Referer: https://akasha.cv/",

        "-H",
        "Origin: https://akasha.cv",
    ]

    try:
        result = subprocess.run(
            ["curl", "-sS", *headers, url],
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )

        return json.loads(result.stdout)

    except subprocess.TimeoutExpired:
        print("Akasha request timed out")
        return None

    except subprocess.CalledProcessError as e:
        print(f"Akasha curl failed: {e.stderr}")
        return None

    except json.JSONDecodeError as e:
        print(f"Invalid Akasha response: {e}")
        return None


class CreateBanner:
    def __init__(
        self,
        data: dict,
        akasha: Optional[bool] = False,
        custom_image: Optional[dict] = None,
        lang: Optional[str] = "en",
    ):
        self.data = data
        self.lang = lang
        self.custom_image = custom_image

        akasha_data = None

        if akasha:
            uid = self.data.get("uid")

            if uid:
                akasha_data = get_akasha(uid)

        self.generated_data = GenereteData(
            data=self.data,
            custom_image=self.custom_image,
            akasha_data=akasha_data
        ).gen_character()

    def generate(self, banner_id: Optional[int] = 1):
        return self.generated_data
