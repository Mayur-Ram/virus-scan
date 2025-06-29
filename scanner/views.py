from django.shortcuts import render
from django.conf import settings
import os
from .utils import get_file_hashes, scan_file

def index(request):
    return render(request, 'scanner/index.html')

def scan_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        md5, sha256 = get_file_hashes(file_path)
        result = scan_file(file_path)

        context = {
            'filename': file.name,
            'md5': md5,
            'sha256': sha256,
            'entropy': result['entropy'],
            'suspicious': result['suspicious_strings'],
            'verdict': result['verdict']
        }

        return render(request, 'scanner/result.html', context)
    return render(request, 'scanner/index.html')
