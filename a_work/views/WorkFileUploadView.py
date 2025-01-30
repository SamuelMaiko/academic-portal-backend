from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from a_work.models import Work, WorkFile
from a_work.serializers import WorkFileSerializer
from a_work.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

class WorkFileUploadView(APIView):
    permission_classes=[IsAuthenticated, IsAdmin]

    def post(self, request, work_id):
        files = request.FILES.getlist("files") 

        if not files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            work = Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({"error": "Work not found"}, status=status.HTTP_404_NOT_FOUND)

        uploaded_files = []
        for file in files:
            work_file = WorkFile.objects.create(work=work, file=file)
            uploaded_files.append(work_file)

        serializer = WorkFileSerializer(uploaded_files, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
