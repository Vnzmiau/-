from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Application
from django.core.files.base import ContentFile
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import  MyUserCreationForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request,'applications/home.html')

@csrf_exempt
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

@csrf_exempt
def manageApplication(request, application_id=None):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return JsonResponse({'error': 'Application does not exist'}, status=404)
    if request.method == 'GET':
        data = {
            'id': application.id,
            'profession': application.profession,
            'education': application.education,
            'work_experience': application.work_experience,
            'file': application.file.url if application.file else None
        }
        return JsonResponse({'msg': 'Application retrieved successfully', 'data': data}, status=200)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            application.profession = data.get('profession', application.profession)
            application.education = data.get('education', application.education)
            application.work_experience = data.get('work_experience', application.work_experience)
            file_data = data.get('file')
            if file_data:
                application.file.save(file_data['name'], ContentFile(file_data['content']))
            application.save()
            return JsonResponse({'msg': 'Application updated successfully', 'data': {'id': application.id, 'profession': application.profession, 'education': application.education}}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            if 'profession' in data:
                application.profession = data['profession']
            if 'education' in data:
                application.education = data['education']
            if 'work_experience' in data:
                application.work_experience = data['work_experience']
            file_data = data.get('file')
            if file_data:
                application.file.save(file_data['name'], ContentFile(file_data['content']))
            application.save()
            return JsonResponse({'msg': 'Application updated successfully', 'data': {'id': application.id, 'profession': application.profession, 'education': application.education}}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
    elif request.method == 'DELETE':
        try:
            application.delete()
            return JsonResponse({'msg': 'Application deleted successfully'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def registerPage(request):
    form=MyUserCreationForm()
    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request,'base/login_register.html',{'form':form})
