from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import ProfileUpdateSerializer


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieve the profile details of the authenticated user.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Profile details retrieved successfully.",
            examples={
                "application/json": {
                    "bio": "",
                    "first_name": "Sam",
                    "last_name": "Maiko",
                    "phone_number": "",
                    "linkedin": None,
                    "country": "Kenya",
                    "county": "Nairobi"
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=['Profile']
)
    
    def get(self, request):
        profile=request.user.profile
        serializer=ProfileUpdateSerializer(profile)
        return Response(serializer.data)
            
    
    @swagger_auto_schema(
    operation_description="Update the profile details of the authenticated user.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name', example='This is an example first name.'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name', example='This is an example last name.'),
            'bio': openapi.Schema(type=openapi.TYPE_STRING, description='User bio', example='This is an example bio.'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number', example='+1234567890'),
            'linkedin': openapi.Schema(type=openapi.TYPE_STRING, description='LinkedIn profile URL', example='https://linkedin.com/in/example'),
            'country': openapi.Schema(type=openapi.TYPE_STRING, description='Country', example='Kenya'),
            'county': openapi.Schema(type=openapi.TYPE_STRING, description='County', example='Nairobi'),
        },
        required=['first_name','last_name']
    ),
    responses={
        200: openapi.Response(
            description="Profile details updated successfully.",
            examples={
                "application/json": {
                    "bio": "",
                    "first_name": "Sam",
                    "last_name": "Maiko",
                    "phone_number": "",
                    "linkedin": None,
                    "country": "Kenya",
                    "county": "Nairobi"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "first_name": [
                        "This field is required."
                    ],
                    "last_name": [
                        "This field is required."
                    ]
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=['Profile']
)        
    
    def put(self, request):
        profile=request.user.profile
        serializer=ProfileUpdateSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            