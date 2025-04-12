from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import cv2
import pytesseract
import re
import numpy as np
# Create your views here.

@api_view(["POST"])
def adhaar(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)

    image_file = request.FILES['image']

    # Tesseract path only for local dev (Windows)
    import platform
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return Response({"error": "Invalid image"}, status=400)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    aadhaar = re.search(r'\d{4}\s\d{4}\s\d{4}', text)
    dob = re.search(r'\d{2}/\d{2}/\d{4}', text)

    name_line = "Not Found"
    for line in text.split('\n'):
        line = line.strip()
        if re.match(r'^[A-Za-z ]{3,}$', line) and not re.search(r'\b(MALE|FEMALE|INDIA|GOVERNMENT|DOB|YOB)\b', line.upper()):
            name_line = line
            break

    gender = None
    for line in text.split("\n"):
        for word in line.strip().split(" "):
            if word.lower() in ['male','female']:
                gender = word
                break

    json = {
        "name" : name_line,
        "DOB" : dob.group() if dob else "Not found",
        "Adhaar Number" : aadhaar.group() if aadhaar else "Not found",
        "Gender" : gender if gender != None else "Not Found"
    }

    return Response(json)
