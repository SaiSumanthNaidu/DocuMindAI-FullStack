import re

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Document
from .serializers import DocumentSerializer
from .auth_serializers import RegisterSerializer

from .ocr_utils import extract_text
from PIL import Image

import pytesseract
from pdf2image import convert_from_path

from .document_parser import analyze_document


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class DocumentUploadView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def extract_aadhaar_region(self, file_path):

        image = Image.open(file_path)

        width, height = image.size

        crop = image.crop(
            (
                int(width * 0.10),
                int(height * 0.20),
                int(width * 0.90),
                int(height * 0.55)
            )
        )

        crop = crop.convert("L")

        crop = crop.resize(
            (
                crop.width * 8,
                crop.height * 8
            )
        )

        text = pytesseract.image_to_string(
            crop,
            lang="eng",
            config="--oem 3 --psm 6"
        )

        return text

    def extract_aadhaar_number_region(self, file_path):

        image = Image.open(file_path)

        width, height = image.size

        # Bottom center region where Aadhaar number exists
        crop = image.crop(
            (
                int(width * 0.20),
                int(height * 0.60),
                int(width * 0.80),
                int(height * 0.90)
            )
        )

        crop = crop.convert("L")

        crop = crop.resize(
            (
                crop.width * 10,
                crop.height * 10
            )
        )

        text = pytesseract.image_to_string(
            crop,
            lang="eng",
            config="--oem 3 --psm 6 digits"
        )

        return text

    def extract_pan_region(self, file_path):

        image = Image.open(file_path)

        width, height = image.size

        crop = image.crop(
            (
                int(width * 0.05),
                int(height * 0.40),
                int(width * 0.95),
                int(height * 0.85)
            )
        )

        crop = crop.convert("L")

        crop = crop.resize(
            (
                crop.width * 4,
                crop.height * 4
            )
        )

        text = pytesseract.image_to_string(
            crop,
            lang="eng",
            config="--oem 3 --psm 4"
        )

        return text

    def extract_voter_region(self, file_path):

        image = Image.open(file_path)

        width, height = image.size

        crop = image.crop(
            (
                int(width * 0.10),
                int(height * 0.08),
                int(width * 0.95),
                int(height * 0.85)
            )
        )

        crop = crop.convert("L")

        crop = crop.resize(
            (
                crop.width * 7,
                crop.height * 7
            )
        )

        text = pytesseract.image_to_string(
            crop,
            lang="eng",
            config="--oem 3 --psm 11"
        )

        return text
    
    def extract_dl_region(self, file_path):

        image = Image.open(file_path)

        width, height = image.size

        crop = image.crop(
            (
                int(width * 0.15),
                int(height * 0.10),
                int(width * 0.95),
                int(height * 0.95)
            )
        )

        crop = crop.convert("L")

        crop = crop.resize(
            (
                crop.width * 8,
                crop.height * 8
            )
        )

        text = pytesseract.image_to_string(
            crop,
            lang="eng",
            config="--oem 3 --psm 11"
        )

        crop.save("dl_debug.jpg")

        return text
    
    def extract_invoice_region(self, file_path):

        image = Image.open(file_path)

        width, height = image.size

        crop = image.crop(
            (
                int(width * 0.05),
                int(height * 0.05),
                int(width * 0.95),
                int(height * 0.95)
            )
        )

        crop = crop.convert("L")

        crop = crop.resize(
            (
                crop.width * 4,
                crop.height * 4
            )
        )

        text = pytesseract.image_to_string(
            crop,
            lang="eng",
            config="--oem 3 --psm 6"
        )

        return text

    def perform_create(self, serializer):

        document = serializer.save(
            user=self.request.user
        )

        front_text = ""
        back_text = ""

        try:

            front_path = document.front_file.path

            # ======================
            # FRONT FILE
            # ======================

            if front_path.lower().endswith(".pdf"):

                pages = convert_from_path(
                    front_path,
                    poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
                )

                for page in pages:

                    temp_path = "temp_page.jpg"

                    page.save(
                        temp_path,
                        "JPEG"
                    )

                    front_text += (
                        extract_text(
                            temp_path
                        )
                        + "\n"
                    )

            else:

                front_text = extract_text(
                    front_path
                )

                if (
                    "AADHAAR" in front_text.upper()
                    or "DOB" in front_text.upper()
                ):

                    aadhaar_region = self.extract_aadhaar_region(
                        front_path
                    )

                    front_text += (
                        "\n\nAADHAAR_REGION:\n"
                        + aadhaar_region
                    )

                    aadhaar_number_region = (
                        self.extract_aadhaar_number_region(
                            front_path
                        )
                    )

                    front_text += (
                        "\n\nAADHAAR_NUMBER_REGION:\n"
                        + aadhaar_number_region
                    )

                if "INCOME TAX" in front_text.upper():

                    pan_region = self.extract_pan_region(
                        front_path
                    )

                    front_text += (
                        "\n\nPAN_REGION:\n"
                        + pan_region
                    )

                if (
                    "INVOICE" in front_text.upper()
                    or "GSTIN" in front_text.upper()
                    or "TOTAL" in front_text.upper()
                ):

                    invoice_region = self.extract_invoice_region(
                        front_path
                    )

                    front_text += (
                        "\n\nINVOICE_REGION:\n"
                        + invoice_region
                    )

                if (
                    "DRIVING" in front_text.upper()
                    or "LICENCE" in front_text.upper()
                    or "LICENSE" in front_text.upper()
                    or "VALIDITY" in front_text.upper()
                    or "DATE OF FIRST ISSUE" in front_text.upper()
                    or re.search(r"TS\d{10,}", front_text.upper())
                ):

                    dl_region = self.extract_dl_region(
                        front_path
                    )

                    front_text += (
                        "\n\nDL_REGION:\n"
                        + dl_region
                    )
                
                if (
                    "ELECTION" in front_text.upper()
                    or "ELECTOR" in front_text.upper()
                ):

                    voter_region = self.extract_voter_region(
                        front_path
                    )

                    front_text += (
                        "\n\nVOTER_REGION:\n"
                        + voter_region
                    )   

            # ======================
            # BACK FILE
            # ======================

            if document.back_file:

                back_path = (
                    document.back_file.path
                )

                if back_path.lower().endswith(".pdf"):

                    pages = convert_from_path(
                        back_path,
                        poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
                    )

                    for page in pages:

                        temp_path = "temp_page.jpg"

                        page.save(
                            temp_path,
                            "JPEG"
                        )

                        back_text += (
                            extract_text(
                                temp_path
                            )
                            + "\n"
                        )

                else:

                    back_text = extract_text(
                        back_path
                    )

            document.front_text = front_text

            document.back_text = back_text

            document.extracted_text = (
                front_text +
                "\n\n" +
                back_text
            )

            document.structured_data = (
                analyze_document(
                    front_text,
                    back_text
                )
            )

            document.save()

        except Exception as e:

            document.structured_data = {
                "error": str(e)
            }

            document.save()


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        documents = Document.objects.filter(
            user=request.user
        )

        latest_document = None

        if documents.exists():
            latest_document = (
                documents.last().title
            )

        return Response({
            "total_documents":
                documents.count(),
            "latest_document":
                latest_document,
            "uploaded_documents":
                [
                    doc.title
                    for doc in documents
                ]
        })


class ResumeSearchView(
    generics.ListAPIView
):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Document.objects.filter(
            user=self.request.user
        )

        keyword = self.request.GET.get(
            "keyword"
        )

        if keyword:

            queryset = queryset.filter(
                extracted_text__icontains=keyword
            )

        return queryset


class MyDocumentsView(
    generics.ListAPIView
):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Document.objects.filter(
            user=self.request.user
        )