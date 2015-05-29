from PIL import Image
import random
import collections
import logging
import pdb

logging.basicConfig(filename='/usr/home/sdmiller/recur.log', level=logging.DEBUG)

Point = collections.namedtuple('Point', ['x', 'y'])

def generate_heights(start, end, roughness=0.5, min_seg=1):
    seg_length = end.x - start.x
    if seg_length < min_seg:
        return start, end

    mid_x = (start.x + end.x) // 2
    mid_y = (start.y + end.y) / 2 + seg_length * roughness * random.uniform(-1, 1)
    midpoint = Point(mid_x, mid_y)

    return generate_heights(start, midpoint, min_seg=min_seg) + generate_heights(midpoint, end, min_seg=min_seg)[1:]

def interp(i, start, end):
    length = end.x - start.x
    proportion = i / length
    inv_proportion = 1 - proportion
    return inv_proportion * start.y + proportion * end.y

def generate_image(imgx, imgy):
    img = Image.new('RGB', (imgx, imgy), "black") # create a new black image
    pixels = img.load() # create the pixel map

    segment_width = 100

    terrain = generate_heights(Point(0, imgy/2), Point(imgx, imgy/2), min_seg=segment_width)
    terrain_max = max(terrain, key=lambda p: p.y).y

    terrain_prev = terrain[0]
    terrain = terrain[1:]

    for i in range(imgx):    # for every pixel:
        fun_color_rotation = random.randint(0,2)
        if (i > terrain[0].x):
            terrain_prev = terrain[0]
            terrain      = terrain[1:]
        height_at_point = interp(i % segment_width, terrain_prev, terrain[0])
        for j in range(imgy):
            j_inv = imgy - j

            # set the colour accordingly
            is_sky = (imgy - j) > height_at_point

            sky_grad = int((1- j/(imgy/2)) * 255)
            earth_grad = int(j_inv/terrain_max * 255)

            fun_colors = collections.deque([earth_grad, 0, 0])
            fun_colors.rotate(fun_color_rotation)
            pixels[i, j] = (sky_grad if not i % 10 and not j % 10 else 0,) * 3 if is_sky else tuple(fun_colors)

    return img

if __name__ == "__main__":
    img = generate_image(640, 640)
    img.show()