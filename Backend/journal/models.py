from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class HappyMoment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="happy_moments"
    )

    date = models.DateField()  # KST 기준 날짜(서버 TIME_ZONE=Asia/Seoul)

    title = models.CharField(max_length=120)          # 한 줄 행복
    detail = models.TextField(blank=True, default="") # 설명(선택)

    tags = ArrayField(
        models.CharField(max_length=30),
        default=list,
        blank=True
    )

    # 행복 강도: 1~5 (선택 입력 허용하고 싶으면 null=True, blank=True)
    intensity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user_id} {self.date} {self.title}"
