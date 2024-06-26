from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile

from .service import process_csv_file, BulkUploadError


UPLOAD_TEMPLATE = "admin/upload_file.html"


def bulk_upload_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES["datafile"]:
        datafile: UploadedFile = request.FILES["datafile"]

        try:
            process_csv_file(datafile)
            messages.success(request, "File uploaded and processed successfully.")
        except BulkUploadError as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(request.path)
    return render(request, UPLOAD_TEMPLATE)


def get_bulk_upload_urls() -> list:
    return [
        path("bulk-upload/", bulk_upload_view, name="bulk-upload"),
    ]
