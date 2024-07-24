from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import Work
from a_work.serializers import WorkSerializer


class WorkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_param=request.GET.get("search","")
        words=request.GET.get("words",None)
        deadline=request.GET.get("deadline",None)

        print(search_param)
        # removing the assigned and uptaken work
        work=Work.objects.filter(Q(uptaken_by=None) & Q(assigned_to=None)).all()
        # filtering the work based on search params
        work=work.filter(work_code__icontains=search_param)
        # filtering the work by words
        if words is not None:
            work=work.filter( words=words)
            
        # filtering the work by day
        if deadline:
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            tomorrow_start = today_end
            tomorrow_end = tomorrow_start + timedelta(days=1)

        if deadline=="today":
            today=timezone.localtime().date()
            work=work.filter(deadline__date=today)
        elif deadline=="tomorrow":
            tomorrow=timezone.localtime().date()+timedelta(days=1)
            work=work.filter(deadline__date=tomorrow)
            
            
        serializer=WorkSerializer(work, many=True, context={'request':request})
        return Response(serializer.data)