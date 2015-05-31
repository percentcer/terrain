from PIL import Image
import random
import collections

Point = collections.namedtuple('Point', ['x', 'y'])


def generate_heights(start, end, roughness=0.5, min_seg=1):
    seg_length = end.x - start.x
    if seg_length <= min_seg:
        return start, end

    mid_x = (start.x + end.x) // 2
    mid_y = (start.y + end.y) / 2 + seg_length * roughness * random.uniform(-1, 1)
    midpoint = Point(mid_x, mid_y)

    return generate_heights(start, midpoint, roughness, min_seg) + generate_heights(midpoint, end, roughness, min_seg)[1:]


def interp(position, start, end):
    proportion = (position - start.x) / (end.x - start.x)
    return (1 - proportion) * start.y + proportion * end.y


def generate_image(imgx, imgy):
    image = Image.new('RGB', (imgx, imgy), "black")
    pixels = image.load()

    segment_width = imgx / 16

    terrain = generate_heights(Point(0, imgy / 2), Point(imgx, imgy / 2),
                               roughness=imgy / imgx / 2,
                               min_seg=segment_width)

    terrain_prev = terrain[0]
    terrain = terrain[1:]

    for i in range(imgx):
        if i > terrain[0].x:
            terrain_prev = terrain[0]
            terrain = terrain[1:]
        height_at_point = interp(i, terrain_prev, terrain[0])
        fun_color_rotation = random.randint(0, 2)
        for j in range(imgy):
            j_inv = imgy - j

            is_sky = (imgy - j) > height_at_point

            sky_grad = int((1 - j / (imgy / 2)) * 255)
            earth_grad = int((j_inv / height_at_point) ** 3 * 255)

            fun_colors = collections.deque([earth_grad, 0, 0])
            fun_colors.rotate(fun_color_rotation)

            # creates dots in the sky
            dot_spacing = segment_width // 8
            sky_color = sky_grad if not i % dot_spacing and not j % dot_spacing else 0

            pixels[i, j] = (sky_color,) * 3 if is_sky else tuple(fun_colors)

    return image


if __name__ == "__main__":
    img = generate_image(1500, 500)
    img.save("output.png")
