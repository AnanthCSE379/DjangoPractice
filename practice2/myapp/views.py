from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Patient
# Create your views here.

def startpage(request):
    return render(request,'startpage.html')

def register(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.total_days = (patient.discharge_date - patient.admit_date).days
            days = patient.total_days

            if days < 0:
                form.add_error('discharge_date','Discharge cannot be before admission')
                return render(request,'register.html',context={"form":form})

            # Each rate applies only to the days in that slab.
            if days <= 3:
                patient.amount = days * 2000
            elif days <= 8:
                patient.amount = 3 * 2000 + (days - 3) * 1500
            else:
                patient.amount = 3 * 2000 + 5 * 1500 + (days - 8) * 1000

            if patient.amount > 15000:
                patient.amount -= patient.amount // 10  # Subtract 10%.

            patient.save()
            return redirect('display')
    return render(request,'register.html',context={"form":form})
def display(request):
    obj = Patient.objects.all()
    return render(request,'display.html',context={"details":obj})

def payment(request):
    if (request.method == "POST"):
        pid = request.POST.get("pid")
        patient = Patient.objects.get(patientid=pid)
        if (patient):
            return render(request,'payment.html',context={"details":patient})
        else:
            return render(request,'payment.html',context={"error":"Id does not exist"})
    return render(request,'payment.html')
        
