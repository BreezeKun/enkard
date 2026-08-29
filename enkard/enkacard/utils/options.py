from PIL import ImageFont
from . import open_file

coloring = (255,255,255,255)

def fontSize(t):
    return ImageFont.truetype(open_file.font, t)

#t32 = ImageFont.truetype(font, 32) fontSize(32)
#t24 = ImageFont.truetype(font, 24) fontSize(24)
#t18 = ImageFont.truetype(font, 18) fontSize(18)
#t17 = ImageFont.truetype(font, 17) fontSize(17)
#t15 = ImageFont.truetype(font, 15) fontSize(15)
#t12 = ImageFont.truetype(font, 12) fontSize(12)

stat_perc = {3, 6, 9, 11, 12, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 3002, 3004, 3005, 3007, 3008, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3018, 3019, 3020, 3021, 3024}
IconAddTrue = ["FIGHT_PROP_PHYSICAL_ADD_HURT","FIGHT_PROP_HEAL_ADD","FIGHT_PROP_GRASS_ADD_HURT","FIGHT_PROP_FIRE_ADD_HURT","FIGHT_PROP_MAX_HP","FIGHT_PROP_CUR_ATTACK","FIGHT_PROP_CUR_DEFENSE","FIGHT_PROP_ELEMENT_MASTERY","FIGHT_PROP_CRITICAL","FIGHT_PROP_CRITICAL_HURT","FIGHT_PROP_CHARGE_EFFICIENCY","FIGHT_PROP_ELEC_ADD_HURT","FIGHT_PROP_ROCK_ADD_HURT","FIGHT_PROP_ICE_ADD_HURT","FIGHT_PROP_WIND_ADD_HURT","FIGHT_PROP_WATER_ADD_HURT"]
dopStatAtribute = {"FIGHT_PROP_MAX_HP": "BASE_HP", "FIGHT_PROP_CUR_ATTACK":"FIGHT_PROP_BASE_ATTACK","FIGHT_PROP_CUR_DEFENSE":"FIGHT_PROP_BASE_DEFENSE"}


# --- Added to support the new library's plain-dict output (see test_result.json) ---
# The new client returns stats keyed by human-readable name ("CRIT Rate", "Max HP", ...)
# instead of the old FIGHT_PROP_* ids, so the icon lookup below is keyed the same way.

# These three are always drawn first on the stat panel, in this order.
PRIMARY_STATS = ["Max HP", "ATK", "DEF"]

# Stats that exist in the data but should never be drawn on the character stat panel
# (e.g. a weapon's "Base ATK" duplicate that sometimes leaks into stats dicts).
STAT_SKIP = {"Base ATK"}

# (display name, is_percentage) -> icon filename inside {assets}/icon/
STAT_ICON_MAP = {
    ("Max HP", False): "HP.png",
    ("HP", False): "HP.png",
    ("HP", True): "HP_PERCENT.png",
    ("ATK", False): "ATTACK.png",
    ("ATK", True): "ATTACK_PERCENT.png",
    ("Base ATK", False): "ATTACK.png",
    ("DEF", False): "DEFENSE.png",
    ("DEF", True): "DEFENSE_PERCENT.png",
    ("Elemental Mastery", False): "MASTERY.png",
    # NOTE: kept intentionally "swapped" to match the existing asset filenames
    # (CRITICAL_HURT.png is the Crit Rate icon, CRITICAL.png is the Crit DMG icon).
    ("CRIT Rate", True): "CRITICAL_HURT.png",
    ("CRIT DMG", True): "CRITICAL.png",
    ("Energy Recharge", True): "CHARGE_EFFICIENCY.png",
    ("Healing Bonus", True): "HEALED_ADD.png",
    ("Incoming Healing Bonus", True): "HEAL.png",
    ("Physical DMG Bonus", True): "PHYSICAL_ADD_HURT.png",
}

# elemental DMG Bonus stat name -> (base icon, "up" icon)
# Only the base icon is currently used (matches the previous behaviour), the "up"
# icon is kept available in case you want to switch it on for the substat rows.
ELEMENT_DMG_ICON_MAP = {
    "Pyro DMG Bonus": ("PYRO.png", "PYRO_UP.png"),
    "Electro DMG Bonus": ("ELECTRO.png", "ELECTRO_UP.png"),
    "Hydro DMG Bonus": ("HYDRO.png", "HYDRO_UP.png"),
    "Anemo DMG Bonus": ("ANEMO.png", "ANEMO_UP.png"),
    "Cryo DMG Bonus": ("CRYO.png", "CRYO_UP.png"),
    "Geo DMG Bonus": ("GEO.png", "GEO_UP.png"),
    "Dendro DMG Bonus": ("DENDRO.png", "DENDRO_UP.png"),
}


def parseStatValue(value):
    """Turn '85.5%' / '18,501' / 63 into a float, safely (used for sorting/zero-checks)."""
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    cleaned = str(value).replace("%", "").replace(",", "").strip()
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0