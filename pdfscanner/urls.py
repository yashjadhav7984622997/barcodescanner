# pdfscanner/urls.py
from django.urls import path
from .views import scan_pdf, download_folder

urlpatterns = [
    path('', scan_pdf, name='scan_pdf'),
    path('download-folder/<int:pdf_document_id>/', download_folder, name='download_folder'),
]
# urls.py

from django.conf import settings
from django.conf.urls.static import static



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
