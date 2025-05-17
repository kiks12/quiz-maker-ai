
import fitz
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status


class UploadViewSet(ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')

        if not file_uploaded:
            return Response({"error": "No File uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Process the file in memory (example: read lines or content)
        try:
            pdf_bytes = file_uploaded.read()  # adjust decode if it's binary
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()

            return Response(
                {
                    "message": "File processed successfully.",
                    "text": full_text
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
