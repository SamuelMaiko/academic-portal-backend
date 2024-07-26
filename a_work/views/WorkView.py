from datetime import timedelta

from a_work.models import Work
from a_work.serializers import WorkSerializer
from django.db.models import Q
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class WorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieves a list of work based on search parameters, including optional filters for words and deadlines.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search using the work codes',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='words',
                in_=openapi.IN_QUERY,
                description='Filter work by no. of words',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='deadline',
                in_=openapi.IN_QUERY,
                description='Filter work based on deadline. Options: "today", "tomorrow"',
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of work ",
                examples={
                    "application/json": [
                            {
                                "id": 8,
                                "work_code": "WK1508",
                                "deadline": "2024-07-17T15:00:00+03:00",
                                "words": 2000,
                                "type": "Reflection Paper",
                                "created_at": "2024-07-17T11:03:54.820923+03:00",
                                "is_bookmarked": False,
                                "has_writer": False,
                                "is_mine": False
                            },
                            {
                                "id": 4,
                                "work_code": "WK2304",
                                "deadline": "2024-07-20T17:30:00+03:00",
                                "words": 2000,
                                "type": "Essay",
                                "created_at": "2024-07-17T11:03:45.296038+03:00",
                                "is_bookmarked": False,
                                "has_writer": False,
                                "is_mine": False
                            },
                    ]
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "error": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Work']
    )

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