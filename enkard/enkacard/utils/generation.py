# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image, ImageChops,ImageFilter
from enkard.enkacard.utils import open_file
from .options import *
from .gradient import userAdaptGrandient, colorBg
import os
# NOTE: this used to say .replace("utils","assets") (plural), but open_file.py's
# `assets` path points at a folder literally named "asset" (singular) - that
# mismatch meant every getIconAdd()/openImageElement() call was reading from a
# folder that doesn't exist. Fixed to match open_file.py.
path = os.path.dirname(__file__).replace("utils","assets")


def centryImage(userImages, teample = 1):
        
    if teample == 1:
        x,y = userImages.size
        if max(x, y) / min(x, y) < 1.1:
            baseheight = 787
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, -58
        
            pass
        elif x > y:
            baseheight = 787
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, int(271 -userImages.size[0]/2)
        else:
            basewidth = 575
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            if hsize < 787:
                baseheight = 787
                hpercent = (baseheight / float (y)) 
                wsize = int ((float (x) * float (hpercent)))
                userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
                return userImages, int(271 -userImages.size[0]/2)
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
            return userImages, 0


def openImageElement(element,teample = 1):
    if teample == 1:
        if element == "Fire":
            return Image.open(f'{path}/Template_one/background/PYRO.png').convert("RGBA")
        elif element== "Grass":
            return Image.open(f'{path}/Template_one/background/DENDRO.png').convert("RGBA")
        elif element == "Electric":
            return Image.open(f'{path}/Template_one/background/ELECTRO.png').convert("RGBA")
        elif element == "Water":
            return Image.open(f'{path}/Template_one/background/GYDRO.png').convert("RGBA")
        elif element == "Wind":
            return Image.open(f'{path}/Template_one/background/ANEMO.png').convert("RGBA")
        elif element== "Rock":
            return Image.open(f'{path}/Template_one/background/GEO.png').convert("RGBA")
        elif element == "Ice":
            return Image.open(f'{path}/Template_one/background/CRYO.png').convert("RGBA")
        else:
            return Image.open(f'{path}/Template_one/background/ERROR.png').convert("RGBA")

def openImageElementConstant(element, teampt = 1):
    if teampt == 1:
        if element == "Fire":
            return Image.open(f'{path}/constant/PYRO.png')
        elif element== "Grass":
            return Image.open(f'{path}/constant/DENDRO.png')
        elif element == "Electric":
            return Image.open(f'{path}/constant/ELECTRO.png')
        elif element == "Water":
            return Image.open(f'{path}/constant/GYDRO.png')
        elif element == "Wind":
            return Image.open(f'{path}/constant/ANEMO.png')
        elif element== "Rock":
            return Image.open(f'{path}/constant/GEO.png')
        elif element == "Ice":
            return Image.open(f'{path}/constant/CRYO.png')
        else:
            return Image.open(f'{path}/constant/ERROR.png')

def maskaAdd(element,charter, teample = 1):
    charter = charter.convert("RGBA")
    if teample == 1:
        bg = openImageElement(element)
        bgUP = bg.copy()
        bg.alpha_composite(charter,(-734,-134))
        im = Image.composite(bg, bgUP, open_file.MaskaBgTeampleOne.convert('L'))
        bg.alpha_composite(im,(0,0))
        # NOTE: the original never returned `bg` here, so every caller received
        # None. Fixed so create_picture()/generationOne() get an actual image back.
        return bg


def userImage(img,element = None, adaptation = False):
    userImagess,pozitionX = centryImage(img)
    if adaptation:
        grandient = userAdaptGrandient(userImagess.convert("RGB").copy())
        Effect = open_file.UserEffectTeampleOne.copy().convert('RGBA')
        grandient = ImageChops.soft_light(grandient,Effect)
        
        Effect.alpha_composite(userImagess,(pozitionX,0))
        im = Image.composite(Effect, grandient, open_file.MaskaUserBg2TeampleOne.convert("L"))
        return im
    else:
        try:
            bg = openImageElement(element)
            effect = bg.copy()
        except Exception as e:
            print(e)

        bg.alpha_composite(userImagess,(pozitionX,0))
        im = Image.composite(bg, effect, open_file.MaskaUserBg2TeampleOne.convert("L"))
        bg.alpha_composite(im,(0,0))
        return bg



def star(x):
    if x == 1:
        imgs = Image.open(f'{path}/stars/Star1.png')
    elif x == 2:
        imgs = Image.open(f'{path}/stars/Star2.png')
    elif x == 3:
        imgs = Image.open(f'{path}/stars/Star3.png')
    elif x == 4:
        imgs = Image.open(f'{path}/stars/Star4.png')
    elif x == 5:
        imgs = Image.open(f'{path}/stars/Star5.png')

    return imgs.copy().convert("RGBA")



def getIconAdd(name, icon = False, size = None, is_percentage = False, element = False):
    """
    Look up the stat icon for a display name coming from the new library's
    output (e.g. "CRIT Rate", "Max HP", "Cryo DMG Bonus" - see test_result.json),
    instead of the old FIGHT_PROP_* ids.

    `icon` is kept only for backwards compatibility with old call sites and is
    no longer used to filter - STAT_ICON_MAP/ELEMENT_DMG_ICON_MAP membership is
    now what decides whether a stat gets an icon.
    """
    filename = None

    if name in ELEMENT_DMG_ICON_MAP:
        base_icon, up_icon = ELEMENT_DMG_ICON_MAP[name]
        filename = up_icon if element else base_icon
    else:
        filename = STAT_ICON_MAP.get((name, bool(is_percentage)))
        if not filename:
            # fall back to the non-percent icon if only that variant is mapped
            filename = STAT_ICON_MAP.get((name, False))

    if not filename:
        return False

    try:
        icons = Image.open(f'{path}/icon/{filename}')
    except FileNotFoundError:
        return False

    if size:
        icons.thumbnail(size)
        return icons.convert("RGBA").copy()
    else:
        return icons.convert("RGBA").copy()