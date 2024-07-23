from django.http import FileResponse
from django.shortcuts import get_object_or_404, render

from a_work.models import Work, WorkImage


# Create your views here.
def download_image(request, image_id):
    image = get_object_or_404(WorkImage, id=image_id)
    file_path = image.image.path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=image.image.name)
    return response
