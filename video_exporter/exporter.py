from dataclasses import dataclass
from typing import Iterator, List

from .path import Path
from .video import Video, videos_keyword


@dataclass
class Exporter:
    folders: List[Path] | Path
    dest: Path = None
    merge_folders: bool = False

    def __post_init__(self):
        if not isinstance(self.folders, List):
            self.folders = [self.folders]

        if self.dest is None:
            self.dest = (self.folders[0] / videos_keyword).with_suffix(".html")

    def get_video_paths(self) -> Iterator[Path]:
        for folder in self.folders:
            yield from Path(folder).find(
                lambda path: path.is_video(), recurse_on_match=True
            )

    def get_sorted_videos(self) -> List[Video]:
        def get_sort_order(video: Video):
            return video.sort_order

        videos = [Video.from_path(path) for path in self.get_video_paths()]
        videos = sorted(videos, key=get_sort_order)
        return videos

    def get_video_tags(self):
        for video in self.get_sorted_videos():
            if video.should_export(self.merge_folders):
                video.export_html(merge_folders=self.merge_folders)
                yield video.tag

    def export(self):
        folder = Path.templates.as_uri()
        css = f'<link href="{folder}/video_index.css" rel="stylesheet" />\n'
        js = f'<script src="{folder}/index_script.js"></script>\n'

        videos_tag = "".join(self.get_video_tags())
        body = f"<body style=\"background-image: url('{folder}/background_index.jpg')\">{videos_tag}</body>"
        content = css + js + body
        self.dest.text = content
        self.dest.tag = 9999
