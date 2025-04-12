from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import cv2
import pytesseract
import re
import numpy as np
# Create your views here.
from django.http import JsonResponse

@api_view(["POST"])
def adhaar(request):
    try:
        if request.method == "POST":
            # Check if the image is provided
            if 'image' not in request.FILES:
                return JsonResponse({"error": "No image file provided."}, status=400)
            
            image_file = request.FILES['image']
            # Convert the image file to a NumPy array (OpenCV compatible)
            file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            
            # Extract Aadhaar number and other info
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
            
            # Return extracted details as JSON response
            json = {
                "name": name_line,
                "DOB": dob.group() if dob else "Not found",
                "Aadhaar Number": aadhaar.group() if aadhaar else "Not found",
                "Gender": gender if gender else "Not Found"
            }
            return JsonResponse(json)

    except Exception as e:
        # Return error message if something goes wrong
        return JsonResponse({"error": str(e)}, status=500)
