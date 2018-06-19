import argparse

import svgwrite

from timeline.Config import Config
from timeline.Timeline import Timeline


def main():
    parser = argparse.ArgumentParser(description='generate svg from json')
    parser.add_argument('input', help='json measurements')
    parser.add_argument('--out', default='out.svg', help='svg output')
    parser.add_argument('--config', help='config')
    args = parser.parse_args()
    dwg = svgwrite.Drawing(args.out, profile='tiny')
    config = Config()
    if args.config:
        config = Config.load(args.config)
    timeline = Timeline.load(args.input, config)
    timeline.draw(dwg)
    dwg.save()


if __name__ == '__main__':
    main()
