import json
import re

import svgwrite


class Config(object):
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 200
        self.TIME_AXIS_HEIGHT = 10
        self.TICKS = 20
        self.PALETTE = [svgwrite.rgb(244, 67, 54)]
        self.FONT_SIZE = 4

    @staticmethod
    def load(file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            config = Config()
            config.WIDTH = data.get("width", 800)
            config.HEIGHT = data.get("height", 200)
            config.FONT_SIZE = data.get("font_size", 2)
            config.TICKS = data.get("time_ticks", 2)
            config.TIME_AXIS_HEIGHT = data.get("time_axis_height", 10)
            palette = []
            for palette_entry in data.get("palette", []):
                rgb = [int(rgb_value) for rgb_value in re.findall("\d+", palette_entry)]
                palette.append(svgwrite.rgb(rgb[0], rgb[1], rgb[2]))
            config.PALETTE = palette
            return config
