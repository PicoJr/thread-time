import json

from timeline.Segment import Segment


class Timeline(object):
    def __init__(self, segments, time_unit, config):
        self.segments = segments
        self.time_unit = time_unit
        self.config = config
        self.time_start = min(segments, key=lambda segment: segment.time_start).time_start
        self.time_end = max(segments, key=lambda segment: segment.time_end).time_end
        self.groups = len(set(s.group for s in self.segments))  # todo case groups empty
        self.scaled_height = self.config.HEIGHT / self.groups
        self.ratio = self.config.WIDTH / (self.time_end - self.time_start)

    def _draw_grid(self, dwg):
        for x in range(0, self.config.WIDTH, self.config.TICKS):
            dwg.add(dwg.line((x, 0), (x, self.config.HEIGHT), stroke='black', stroke_width=0.1))

    def _draw_time_axis(self, dwg):
        dwg.add(dwg.rect((0, self.config.HEIGHT), (self.config.WIDTH, self.config.TIME_AXIS_HEIGHT), fill='white'))
        y_time_tick = self.config.HEIGHT + self.config.TIME_AXIS_HEIGHT / 2
        for x_tick_time in range(0, self.config.WIDTH, self.config.TICKS):
            tick_time = "{:10.2f}".format(x_tick_time * (1 / self.ratio))
            dwg.add(dwg.text(tick_time, (x_tick_time, y_time_tick), font_size=self.config.FONT_SIZE))

    def _draw_background(self, dwg):
        dwg.add(dwg.rect((0, 0), (self.config.WIDTH, self.config.HEIGHT), fill='white'))

    def _draw_segments(self, dwg):
        for segment in self.segments:
            self._draw_segment(segment, dwg)

    def _draw_segment(self, segment, dwg):
        x0 = (segment.time_start - self.time_start) * self.ratio
        x1 = (segment.time_end - self.time_start) * self.ratio
        y0 = self.scaled_height * (segment.group % self.groups)
        scaled_width = (x1 - x0)
        color = self.config.PALETTE[segment.group % len(self.config.PALETTE)]
        dwg.add(dwg.rect((x0, y0), (scaled_width, self.scaled_height), rx=1, ry=1, fill=color, fill_opacity=0.5))
        segment_label = "{} ({} {})".format(segment.text, segment.time_end - segment.time_start, self.time_unit)
        dwg.add(dwg.text(segment_label, (x0, y0 + self.scaled_height * 0.25), font_size=self.config.FONT_SIZE))
        time_start_label = "{} {}".format(segment.time_start - self.time_start, self.time_unit)
        time_end_label = "{} {}".format(segment.time_end - self.time_start, self.time_unit)
        dwg.add(dwg.text(time_start_label, (x0, y0 + self.scaled_height * 0.5), font_size=self.config.FONT_SIZE))
        dwg.add(dwg.text(time_end_label, (x0, y0 + self.scaled_height * 0.75), font_size=self.config.FONT_SIZE))

    def draw(self, dwg):
        self._draw_background(dwg)
        self._draw_grid(dwg)
        self._draw_segments(dwg)
        self._draw_time_axis(dwg)

    @staticmethod
    def load(file_name, config):
        with open(file_name) as json_file:
            data = json.load(json_file)
            segments = Timeline._load_segments(data)
            time_unit = "???"
            if "time_unit" in data:
                time_unit = data["time_unit"]
            return Timeline(segments, time_unit, config)

    @staticmethod
    def _load_segments(data):
        segments = []
        for segment_data in data["segments"]:
            extra = {}
            if "text" in segment_data:
                extra["text"] = segment_data["text"]
            assert segment_data["time_start"] < segment_data["time_end"]
            segments.append(Segment(segment_data["group"], segment_data["time_start"], segment_data["time_end"], extra))
        return segments
