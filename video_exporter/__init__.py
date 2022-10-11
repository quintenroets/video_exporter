from .exporter import Exporter


def export(folders, dest=None):
    Exporter(folders, dest).export()
