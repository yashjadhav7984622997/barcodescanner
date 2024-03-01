# pdfscanner/util.py
import os
import fitz  # PyMuPDF
from PIL import Image
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
from .models import BarcodeData

def convert_pdf_to_images(pdf_path, output_folder, image_format='png', resolution=300):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize variables for barcode detection
    current_barcode_data = None
    current_page_images = []

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Convert the page to a Pixmap
        pixmap = page.get_pixmap(matrix=fitz.Matrix(resolution/72, resolution/72))

        # Convert the Pixmap to a PIL Image
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        # Save the image
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.{image_format}")
        image.save(image_path, format=image_format)

        # Check for barcodes in the saved image
        barcodes_qr = decode(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
        barcodes_linear = decode(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), symbols=[ZBarSymbol.CODE128])

        if barcodes_qr or barcodes_linear:
            # If a barcode is detected on the current page
            if current_barcode_data:
                # Save the previous pages with the same barcode data
                save_pages(current_page_images, current_barcode_data, output_folder)

            # Reset variables for the new barcode
            if barcodes_qr:
                current_barcode_data = barcodes_qr[0].data.decode("utf-8")
            elif barcodes_linear:
                current_barcode_data = barcodes_linear[0].data.decode("utf-8")

            current_page_images = [image_path]
        else:
            # If no barcode is detected, continue collecting pages
            current_page_images.append(image_path)

    # Save the last set of pages
    if current_barcode_data:
        save_pages(current_page_images, current_barcode_data, output_folder)

    # Close the PDF document
    pdf_document.close()
import os
import shutil
def save_pages(pages, barcode_data, output_folder):
    # Save the pages with the same barcode data
    output_folder_barcode = os.path.join(output_folder, barcode_data)
    
    if not os.path.exists(output_folder_barcode):
        os.makedirs(output_folder_barcode)

    for i, page_path in enumerate(pages):
        new_page_path = os.path.join(output_folder_barcode, f"page_{i + 1}.png")

        # Use shutil.move to handle the move operation
        shutil.move(page_path, new_page_path)


# Additional function to scan and save barcodes in the database
# pdfscanner/util.py

# ... (previous code)

# Additional function to scan and save barcodes in the database
def scan_and_save_barcodes(pdf_document, output_folder):
    # Create a folder based on the PDF document ID
    pdf_folder = os.path.join(output_folder, str(pdf_document.id))
    os.makedirs(pdf_folder, exist_ok=True)

    # Use the convert_pdf_to_images function to get the barcode images
    convert_pdf_to_images(pdf_document.pdf_file.path, pdf_folder)

    # Get the list of images in the pdf_folder
    pdf_images = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Call save_pages to organize pages with the same barcode data
    save_pages(pdf_images, str(pdf_document.id), output_folder)
