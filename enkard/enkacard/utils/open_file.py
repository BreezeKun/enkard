from PIL import Image
import threading
from weakref import WeakValueDictionary
from pathlib import Path

lock = threading.Lock()
cache = WeakValueDictionary()
assets = Path(__file__).parent.parent / 'assets'
print(assets)

font = str(assets / 'font' / 'Genshin_Impact.ttf')

mapping = {
    'TalantsFrameTeampleOne': assets/'Template_one'/'talents'/'TALANTS_FRAME.png',
    'TalantsFrameGoldLvlTeampleOne': assets/'Template_one'/'talents'/'TALANTS_FRAME_GOLD_LVL.png',
    'TalantsCountTeampleOne': assets/'Template_one'/'talents'/'TALANTS_COUNT.png',

    'AttributeTeampleOne': assets/'Template_one'/'stats'/'STATS.png',
    'AttributeBgTeampleOne': assets/'Template_one'/'stats'/'STATS_FRAME.png',
    'AttributeDopValueTeampleOne': assets/'Template_one'/'stats'/'STATS_DOP_VALUE.png',

    'UserBgTeampleOne': assets/'Template_one'/'mask'/'ADAPTATION.png',
    'UserEffectTeampleOne': assets/'Template_one'/'mask'/'ADAPTATION5.png',
    'MaskaBgTeampleOne': assets/'Template_one'/'mask'/'maska.png',
    'MaskaUserBgTeampleOne': assets/'Template_one'/'mask'/'maskaUserArt.png',
    'MaskaUserBg2TeampleOne': assets/'Template_one'/'mask'/'ADAPTATION2.png',

    'ClossedBg': assets /'constant'/'CLOSED_BG.png',
    'Clossed': assets /'constant'/'CLOSED.png',
    'ConstantBG': assets /'constant'/'CONSTATN_BG.png',
    'StarBg': assets /'stars'/'bg.png',


    'FRENDS': assets /'icon'/'FRIENDS.png',
    'ErrorBgTeampleOne': assets /'Template_one'/'background'/'ERROR.png',

    'ArtifactNameBgTeampleOne': assets/'Template_one'/'artifacts'/'ARTIFACT_SET_BG.png',
    'ArtifactNameFrameTeampleOne': assets/'Template_one'/'artifacts'/'ARTIFACT_SET_FRAME.png',

    'ArtifactBgTeampleOne': assets/'Template_one'/'artifacts'/'ARTIFACT_BG.png',
    'ArtifactBgUpTeampleOne': assets/'Template_one'/'artifacts'/'ARTIFACT_UP.png',
    'ArtifactDopValueTeampleOne': assets/'Template_one'/'artifacts'/'ARTIFACT_BG_DOP_VAL.png',

    'WeaponBgTeampleOne': assets/'Template_one'/'weapons'/'WEAPON_FRAME_TWO.png',
    'WeaponBgUpTeampleOne': assets/'Template_one'/'weapons'/'WEAPON_FRAME_TWO_UP.png',

    'NameBgTeampleOne': assets/'Template_one'/'character_info'/'CHARTER_FRAME.png',


    'C_STAR_4': assets/'stars'/'c_stars_4.png',
    'C_STAR_5': assets/'stars'/'c_stars_5.png',
    

}

def __dir__():
    return sorted(set([*globals(), *mapping]))

def __getattr__(name):
    try:
        path = mapping[name]
    except KeyError:
        raise AttributeError(name) from None
    
    with lock:
        try:
            image = cache[name]
        except KeyError:
            cache[name] = image = Image.open(path)
        
        return image