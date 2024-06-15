from django.shortcuts import render
from django.http import JsonResponse
from .models import Application
from django.core.files.base import ContentFile
import json

def home(request):
    return render(request,'applications/home.html')

def manageApplication(request,application_id=None):
    if request.method == 'POST':
        data=json.loads(request.body)
        profession=data.get('profession')
        education=data.get('education')
        work_experience=data.get('work_experience')
        file_data=data.get('file')
        application=Application.objects.create(
            applicant=request.user
            profession=profession,
            education=education,
            work_experience=work_experience
        )
        if file_data:
            application.file.save(file_data['name'],ContentFile(file_data['content']))
        return JsonResponse({'msg':'Application created succesfully','data': {'id': application.id, 'profession': application.profession, 'education': application.education}}, status=201)