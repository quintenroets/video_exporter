from .exporter import Exporter


def export(folders, dest=None, merge_folders=False):
    Exporter(folders, dest, merge_folders=merge_folders).export()
