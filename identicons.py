
import hashlib
from PIL import Image, ImageDraw

background_color = (244, 244, 244)


class IdenticonGenerator(object):
    def __init__(self, str):
        hash_list = self.get_hash(str)
        color = self.generate_color_from_hash(hash=hash_list)
        grid = self.build_grid(hash_list)
        grid_list = self.grid_to_list(grid)
        pixels = self.make_pixels(grid_list)
        identicon_image = self.draw_identicon(color, grid_list, pixels)
        identicon_image.save(hash_list + '.png', format='PNG')

    def get_hash(self, str):
        hash_data = hashlib.md5(str.encode('utf8'))
        print(hash_data.hexdigest())
        return hash_data.hexdigest()

    def generate_color_from_hash(self, hash):
        r, g, b = tuple(hash[i:i + 2] for i in range(0, 2 * 3, 2))
        print(r, g, b)
        return f'#{r}{g}{b}'

    def build_grid(self, hash):
        hash_tail = hash[2:]
        # make 3x5 grid, this is a half of a symetric grid
        half_grid = [
            [hash_tail[col:col + 2] for col in range(row, row + 2 * 3, 2)]
            for row in range(0, 2 * 3 * 5, 2 * 3)]
        # print(half_grid)
        # now mirror that
        hex_grid = self.mirror_half_grid(half_grid)
        grid_data_to_int = [list(map(lambda e: int(e, base=16), row)) for row
                            in hex_grid]
        filtered_grid = [[byte if byte % 2 == 0 else 0 for byte in row] for row
                         in grid_data_to_int]
        return filtered_grid

    def mirror_half_grid(self, half_grid):
        mirror_of_half = [list(reversed(row)) for row in half_grid]
        grid = [row + mirror_row[1:] for row, mirror_row in zip(half_grid,
                                                                mirror_of_half)]
        return grid

    def grid_to_list(self, grid):
        listed = [element for row in grid for element in row]

        return listed

    def make_pixels(self, grid_list):
        pixels = []
        for i, val in enumerate(grid_list):
            x = int(i % 5 * 50) + 20
            y = int(i // 5 * 50) + 20
            top_left = (x, y)
            bottom_right = (x + 50, y + 50)
            pixels.append([top_left, bottom_right])
        return pixels

    def draw_identicon(self, color, grid_list, pixels_data):
        identicon_image = Image.new('RGB', (50 * 5 + 20 * 2, 50 * 5 + 20 * 2),
                                    background_color)
        draw = ImageDraw.Draw(identicon_image)
        for grid, pixel in zip(grid_list, pixels_data):
            if grid != 0:
                draw.rectangle(pixel, fill=color)

        return identicon_image


ha = IdenticonGenerator(input('String is: '))
