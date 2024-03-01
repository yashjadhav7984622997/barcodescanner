# pdfscanner/views.py
import os
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PDFUploadForm
from .models import PDFDocument, BarcodeData
from .utils import scan_and_save_barcodes

def scan_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = PDFDocument.objects.create(pdf_file=request.FILES['pdf_file'])
            
            # Specify the destination folder based on the PDF document ID
            destination_folder = os.path.join('media', 'barcodes')
            
            scan_and_save_barcodes(pdf_document, destination_folder)
            print(f'pdf_document.id: {pdf_document.id}')
            return redirect('download_folder', pdf_document_id=pdf_document.id)
    else:
        form = PDFUploadForm()
    return render(request, 'pdfscanner/scan_pdf.html', {'form': form})


def download_folder(request, pdf_document_id):
    pdf_document = get_object_or_404(PDFDocument, pk=pdf_document_id)

    # Specify the directory where the images are stored
    pdf_folder = os.path.dirname(pdf_document.pdf_file.path)
    image_folder = os.path.join('media', 'barcodes', str(pdf_document.id))

    # Specify the output path for the zip file within the media folder
    zip_file_path = os.path.join('media','zip_folder', f'{pdf_document.id}_barcodes.zip')

    # Create the output folder if it doesn't exist
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

    # Create a zip file containing all images
    shutil.make_archive(zip_file_path[:-4], 'zip', image_folder)

    # Prepare the response to send the zip file
    response = HttpResponse(open(zip_file_path, 'rb'))
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = f'attachment; filename="{pdf_document.pdf_file.name}_barcodes.zip"'

    return response
