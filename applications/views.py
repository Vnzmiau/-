from django.shortcuts import render
from django.http import JsonResponse
from .models import Application
from django.core.files.base import ContentFile
import json

def home(request):
    return render(request,'applications/home.html')

def manageApplications(request):
    if request.method == 'POST':
        try:
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
        except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
             return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'GET':
        applications=Application.objects.all()
        context={'applications':applications}
        return render(request,'applications/manageApplications.html',context)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

       