from datetime import timedelta
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Count, Avg

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HappyMoment
from .serializers import HappyMomentSerializer
from .filters import HappyMomentFilter


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class HappyMomentViewSet(viewsets.ModelViewSet):
    serializer_class = HappyMomentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_class = HappyMomentFilter
    search_fields = ["title", "detail"]  # ?search=...
    ordering_fields = ["date", "created_at", "intensity"]

    def get_queryset(self):
        return HappyMoment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path=r"by-date/(?P<date>\d{4}-\d{2}-\d{2})")
    def by_date(self, request, date=None):
        d = parse_date(date)
        if not d:
            return Response({"detail": "Invalid date."}, status=400)

        qs = HappyMoment.objects.filter(user=request.user, date=d).order_by("-created_at")
        return Response(self.get_serializer(qs, many=True).data)


class WeeklyReportView(APIView):
    """
    GET /reports/weekly?weekStart=YYYY-MM-DD
    - writtenDays: 이번 주 행복 기록이 있었던 '날' 수 (0~7)
    - totalMoments: 이번 주 행복 순간 총 개수
    - topTags: 태그 TOP 5
    - bestDay: 행복 순간 가장 많았던 날짜
    - avgIntensity: 이번 주 평균 강도 (입력된 것만)
    - intensityDist: 1~5 분포
    """

    def get(self, request):
        week_start_raw = request.query_params.get("weekStart")
        if not week_start_raw:
            return Response({"detail": "weekStart is required (YYYY-MM-DD)."}, status=400)

        ws = parse_date(week_start_raw)
        if not ws:
            return Response({"detail": "Invalid weekStart format."}, status=400)

        we = ws + timedelta(days=6)
        qs = HappyMoment.objects.filter(user=request.user, date__gte=ws, date__lte=we)

        total_moments = qs.count()

        # writtenDays: 날짜 distinct 개수
        written_days = qs.values("date").distinct().count()

        # bestDay: 날짜별 count 최대
        best_day_obj = qs.values("date").annotate(c=Count("id")).order_by("-c", "date").first()
        best_day = best_day_obj["date"].isoformat() if best_day_obj else None
        best_day_count = best_day_obj["c"] if best_day_obj else 0

        # avgIntensity: null 제외 평균
        avg_intensity = qs.aggregate(v=Avg("intensity"))["v"]
        avg_intensity = round(avg_intensity, 2) if avg_intensity is not None else None

        # intensityDist: 1~5 분포
        dist = {str(i): 0 for i in range(1, 6)}
        for item in qs.exclude(intensity__isnull=True).values("intensity").annotate(c=Count("id")):
            dist[str(item["intensity"])] = item["c"]

        # topTags: 파이썬 집계(데이터량 적어서 OK)
        tag_map = {}
        for m in qs.only("tags"):
            for t in (m.tags or []):
                t = (t or "").strip()
                if not t:
                    continue
                tag_map[t] = tag_map.get(t, 0) + 1
        top_tags = sorted(tag_map.items(), key=lambda x: x[1], reverse=True)[:5]
        top_tags = [{"tag": t, "count": c} for t, c in top_tags]

        # streak: KST 오늘부터 연속으로 "하루에 하나라도 기록한 날" 수
        today = timezone.localdate()  # TIME_ZONE=Asia/Seoul이면 KST 기준
        streak = 0
        cursor = today
        while True:
            if HappyMoment.objects.filter(user=request.user, date=cursor).exists():
                streak += 1
                cursor = cursor - timedelta(days=1)
                if streak > 365:
                    break
            else:
                break

        return Response({
            "weekStart": ws.isoformat(),
            "weekEnd": we.isoformat(),
            "writtenDays": written_days,
            "totalMoments": total_moments,
            "streak": streak,
            "bestDay": best_day,
            "bestDayCount": best_day_count,
            "avgIntensity": avg_intensity,
            "intensityDist": dist,
            "topTags": top_tags,
        })
