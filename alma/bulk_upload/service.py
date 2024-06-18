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

    @classmethod
    def model_mapping(cls) -> dict[int, str]:
        return {
            cls.ROOT.value: "Region",
            cls.REGION.value: "Disk",
            cls.DISK.value: "Band",
            cls.BAND.value: "Molecule",
            cls.MOLECULE.value: "Data",
        }

    @property
    def display_name(self) -> str:
        if self == self.ROOT:
            return "Root"
        return self.model_mapping()[self.value]

    @classmethod
    def values(cls) -> list[int]:
        return [level.value for level in cls]


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
            path = file_path.relative_to(root_dir)
            print(f"{path} - {FileLevel(level).display_name}")

            # TODO: Create entities based on the file path and level
            # Example: create_region(file_path)

            # TODO: Create relationships between entities: region -> disk -> band -> molecule -> data
