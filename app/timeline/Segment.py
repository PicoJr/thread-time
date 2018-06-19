class Segment(object):
    def __init__(self, group, time_start, time_end, extra):
        self.group = group
        self.time_start = time_start
        self.time_end = time_end
        self.text = None
        self._init_extra(extra)

    def _init_extra(self, extra):
        if "text" in extra:
            self.text = extra["text"]
