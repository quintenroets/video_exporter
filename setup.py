from setuptools import find_packages, setup

NAME = "video_exporter"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description="",
    name=NAME,
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    entry_points={"console_scripts": ["export_videos = video_exporter.main:main"]},
)
