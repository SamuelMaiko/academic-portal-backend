import io
import zipfile

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from a_work.models import Work, WorkImage


def download_images_as_zip(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    images = work.images.all()

    # Create a byte stream to hold the zip file
    buffer = io.BytesIO()
    
    # Create a zip file in memory
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for image in images:
            image_path = image.image.path
            image_name = image.image.name
            zip_file.write(image_path, arcname=image_name)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="images_{work_id}.zip"'
    return response
