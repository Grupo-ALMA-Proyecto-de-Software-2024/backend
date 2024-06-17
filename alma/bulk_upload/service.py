from django.core.files.uploadedfile import UploadedFile


def process_zip_file(datafile: UploadedFile) -> None:
    print("Processing zip file!!!!!!!!!!!")
