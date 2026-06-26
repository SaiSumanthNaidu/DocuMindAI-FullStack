from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Document

        fields = [
            "id",
            "title",
            "front_file",
            "back_file",
            "front_text",
            "back_text",
            "extracted_text",
            "structured_data",
            "uploaded_at"
        ]

        read_only_fields = [
            "front_text",
            "back_text",
            "extracted_text",
            "structured_data",
            "uploaded_at"
        ]