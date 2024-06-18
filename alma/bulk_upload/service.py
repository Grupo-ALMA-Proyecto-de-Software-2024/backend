import os
import zipfile
import enum
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator
from collections import deque

from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError


class FileLevel(enum.Enum):
    ROOT = 0
    REGION = 1
    DISK = 2
    BAND = 3
    MOLECULE = 4
    DATA = 5

    @property
    def display_name(self) -> str:
        return {
            FileLevel.ROOT: "Root",
            FileLevel.REGION: "Region",
            FileLevel.DISK: "Disk",
            FileLevel.BAND: "Band",
            FileLevel.MOLECULE: "Molecule",
            FileLevel.DATA: "Data",
        }[self]


def bfs_traversal(root: Path, level: int) -> Generator[tuple[Path, int], None, None]:
    queue = deque([(root, level)])
    while queue:
        current, level = queue.popleft()
        yield current, level
        if current.is_dir():
            queue.extend((child, level + 1) for child in current.iterdir())


def process_zip_file(datafile: UploadedFile) -> None:
    if not zipfile.is_zipfile(datafile):
        raise ValidationError("Uploaded file is not a zip file")

    with (
        TemporaryDirectory() as tmpdirname,
        zipfile.ZipFile(datafile, "r") as zip_ref,
    ):
        tmp_dir = Path(tmpdirname)
        zip_ref.extractall(tmp_dir)
        extracted_folder_name = zip_ref.namelist()[0]
        root_dir = tmp_dir / extracted_folder_name

        for file_path, level in bfs_traversal(root_dir, FileLevel.ROOT.value):
            print(f"{file_path} - {FileLevel(level).display_name}")
