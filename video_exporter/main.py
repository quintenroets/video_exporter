import argparse

import video_exporter


def main():
    parser = argparse.ArgumentParser(description="Export videos to html index file")
    parser.add_argument("path", help="Root folder under which all videos reside")
    parser.add_argument(
        "dest", nargs="?", help="The file to save the export to", default=None
    )
    args = parser.parse_args()

    video_exporter.export(args.path, args.dest)


if __name__ == "__main__":
    main()
