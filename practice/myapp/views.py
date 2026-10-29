from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import StaffPersonal
# Create your views here.

def startpage(request):
    return render(request,'startpage.html')

def register(request):
    form = RegistrationForm()
    if (request.method == "POST"):
        form = RegistrationForm(request.POST)
        if (form.is_valid()):
            faculty = form.save(commit=False)
            faculty.save()
            return redirect('faculties')
    return render(request,'create.html',context={"form":form})

def search(request):
    return render(request,'search.html')

def faculties(request):
    facs = StaffPersonal.objects.all()
    cont = {"facs":facs}
    return render(request,'faculties.html',context=cont)

def update(request,idx):
    old_details = StaffPersonal.objects.get(id=idx)
    form = RegistrationForm(instance=old_details)
    if (request.method == "POST"):
        form = RegistrationForm(request.POST, instance=old_details)
        if (form.is_valid()):
            faculty = form.save(commit=False)
            faculty.save()
            return redirect('faculties')
    return render(request,'update.html',context={"form":form})

def delete(request,idx):
    fac = StaffPersonal.objects.get(id=int(idx))
    fac.delete()
    return redirect('faculties')
