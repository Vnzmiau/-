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
            applicant=request.user,
            profession=profession,
            education=education,
            work_experience=work_experience
        )
        if file_data:
            application.file.save(file_data['name'],ContentFile(file_data['content']))
        return JsonResponse({'msg':'Application created succesfully','data': {'id': application.id, 'profession': application.profession, 'education': application.education}}, status=201)
    elif request.method in ['PUT','PATCH']:
        if application_id is None:
            return JsonResponse({'error': 'Application ID is required for update'}, status=400)
        try:
            application=Application.objects.get(id=application_id)
            data=json.loads(request.body)
            if request.method == 'PUT':
                application.profession = data.get('profession', application.profession)
                application.education = data.get('education', application.education)
                application.work_experience = data.get('work_experience', application.work_experience)
            elif request.method == 'PATCH':
                if 'profession' in data:
                    application.profession=data['profession']
                if 'education' in data :
                    application.education=data['education']
                if 'work_experience' in data:
                    application.work_experience = data['work_experience']
            
        