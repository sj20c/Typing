from rest_framework import serializers
from .models import HappyMoment


class HappyMomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HappyMoment
        fields = ["id", "date", "title", "detail", "tags", "intensity", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_tags(self, value):
        # 공백 제거 + 중복 제거 + 빈 문자열 제거
        cleaned = []
        seen = set()
        for t in (value or []):
            t = (t or "").strip()
            if not t:
                continue
            if t in seen:
                continue
            seen.add(t)
            cleaned.append(t)
        return cleaned
