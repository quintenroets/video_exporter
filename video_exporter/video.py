from dataclasses import asdict, dataclass
from datetime import datetime

import cli

from .path import Path

view_keyword = "__VIEW__"
videos_keyword = "Videos"


@dataclass
class Item:
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def dict(self):
        return asdict(self)


@dataclass
class VideoInfo(Item):
    path: Path
    title: str
    mtime: float
    duration: float

    @classmethod
    def from_path(cls, path: Path):
        duration = get_duration(path)
        return cls(path, path.stem, path.mtime, duration)


def get_duration(path: Path):
    milliseconds = cli.get(f'mediainfo --Inform="Video;%Duration%"', path) or 0
    # Some durations are in float format
    seconds = int(float(milliseconds)) // 1000
    return seconds


class Video(VideoInfo):
    @property
    def tag(self):
        mtime = datetime.fromtimestamp(self.mtime).strftime("%d-%m-%Y %H:%M")
        href = self.html_path.as_uri()
        tag = (
            f"<h2><a href='{href}' style='text-decoration: none' target = '_blanck'>"
            f"&ensp;{self.title}<small>&ensp;({self.duration_string})&ensp;[{mtime}]</small></a></h2><hr>"
        )
        return tag

    @property
    def duration_string(self):
        # durations are in float format
        seconds = int(float(self.duration))

        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        hours_str = str(int(hours))
        minutes_str = str(minutes)
        if hours:
            minutes_str = minutes_str.zfill(2)
        seconds_str = str(seconds).zfill(2)

        duration_string = minutes_str + ":" + seconds_str
        if hours:
            duration_string = hours_str + ":" + duration_string

        return duration_string

    @property
    def html_path(self):
        return (self.path.parent / videos_keyword / self.path.stem).with_suffix(".html")

    def should_export(self, merge_folders):
        return view_keyword not in self.path.stem or not merge_folders

    def export_html(self, merge_folders: bool = False):
        if not self.html_path.exists() and self.should_export(merge_folders):
            self.start_export_html(merge_folders=merge_folders)

    def get_sources(self, merge_folders: bool):
        if merge_folders:
            sources = [path for path in self.path.parent.iterdir() if path.is_video()]
        else:
            sources = [self.path]
            second_view_path = self.path.with_stem(self.path.stem + view_keyword)
            if second_view_path.exists():
                sources.append(second_view_path)

        sources = sorted(sources, key=lambda path: path.size, reverse=True)[:2]
        return sources

    def start_export_html(self, merge_folders: bool):
        sources = self.get_sources(merge_folders)
        template_path = Path.template1 if len(sources) == 1 else Path.template2
        content = template_path.text.replace("**TITLE**", self.title)
        replacements = {
            "SOURCENAME": sources[0],
            "SOURCENAME1": sources[0],
            "SOURCENAME2": sources[-1],
            "TEMPLATES": Path.templates,
        }
        for k, v in replacements.items():
            content = content.replace(f"**{k}**", v.as_uri())

        self.html_path.text = content
        sources[0].copy_properties_to(self.html_path)

    @property
    def sort_order(self):
        return self.path.tag, self.path.mtime
