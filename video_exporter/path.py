import plib

root = plib.Path(__file__).parent


class Path(plib.Path):
    templates = root.parent / "assets" / "templates"
    template1 = templates / "video.html"
    template2 = templates / "video2.html"
