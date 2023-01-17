import plib


class Path(plib.Path):
    @classmethod
    @property
    def root(cls):
        return cls(__file__).parent

    @classmethod
    @property
    def templates(cls):
        return cls.root / "assets" / "templates"

    @classmethod
    @property
    def template1(cls):
        return cls.templates / "video.html"

    @classmethod
    @property
    def template2(cls):
        return cls.templates / "video2.html"

    def is_video(self):
        return self.filetype == "video"
