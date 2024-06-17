import zipfile
from pathlib import Path

from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.urls import path
from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile

# import settings


class BulkUploadAdminView(admin.ModelAdmin):
    change_list_template = "admin/yourmodel_change_list.html"

    def get_urls(self) -> list:
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload/",
                self.admin_site.admin_view(self.upload_file),
                name="upload-file",
            ),
        ]
        return custom_urls + urls

    def upload_file(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST" and request.FILES["datafile"]:
            datafile: UploadedFile = request.FILES["datafile"]

            # Unzip and process the file here
            self.process_zip_file(datafile)

            self.message_user(request, "File uploaded and processed successfully.")
            return HttpResponseRedirect("../")
        return render(request, "admin/upload_file.html")

    def process_zip_file(self, datafile: UploadedFile) -> None:
        # with zipfile.ZipFile(datafile, "r") as zip_ref:
        #     extract_path = Path(settings.MEDIA_ROOT) / "extracted"
        #     zip_ref.extractall(extract_path)
        #     # Add your data processing logic here
        #     # Example: process each file in the extracted folder
        print("Processing zip file")
