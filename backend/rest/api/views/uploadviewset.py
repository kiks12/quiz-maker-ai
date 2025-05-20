
import fitz
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from ..quizai import GemmaAI
import json


class UploadViewSet(ViewSet):
    gemma_ai = GemmaAI()
    parser_classes = (MultiPartParser, FormParser)

    """
    SAMPLE POST REQUEST FORM-DATA
    
    file: pdf-file
    metadata: JSON {
        "quiz_types": ["multiple_choice", "true_or_false", "identification", "enumeration", "essay_type"],
        "items_per_type": {
            "multiple_choice": 5,
            "true_or_false": 5,
            "identification": 5,
            "enumeration": 5,
            "essay_type": 5
        }
    }
    """

    def create(self, request):
        data = request.POST
        file = request.FILES.get('file')
        metadata = json.loads(data["metadata"]) if "metadata" in data else {}

        if not file:
            return Response({
                "error": "No uploaded file from request. "
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            full_text = self.read_text_from_pdf(file)
            prompt, created_quiz = self.gemma_ai.create_quiz(
                full_text, metadata)

            return Response(
                {
                    "message": "File processed successfully.",
                    "metadata": metadata,
                    "text": full_text,
                    "prompt": prompt,
                    "created_quiz": created_quiz
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_text_from_pdf(self, file):
        pdf_bytes = file.read()  # adjust decode if it's binary
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        return full_text
