import os

import pygame as pg

utils_dir = os.path.split(os.path.abspath(__file__))[0]
parent_dir = os.path.dirname(os.path.normpath(utils_dir))
print(parent_dir)
data_dir = os.path.join(parent_dir, "game/assets")


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()
