from django.db import models

# Create your models here.
# pdfscanner/models.py
from django.db import models

class PDFDocument(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')

class BarcodeData(models.Model):
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE)
    barcode_value = models.CharField(max_length=255)
    page_image = models.ImageField(upload_to='barcodes/')
