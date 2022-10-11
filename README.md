# Video exporter

Export videos to html index file

Features:
* Collects all videos present any level deep in exported folder
* Creates overview that presents video titles, created times, duration times and order
* Keeps track of which videos have already been watched
* Keep track of position of videos that have been watched partly
* Automatically open last partly watched video or oldest video not watched before

Optional options:
* Export destination location

## Installation

```shell
pip install git+https://github.com/quintenroets/video_exporter
```

## Usage

### Cli

```shell
export_videos folder
```

### Python scripts

```shell
import video_exporter
```

* Download single url:

```shell
video_exporter.export(path)
```

* Export multiple path:

```shell
video_exporter.export(paths)
```
