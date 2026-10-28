from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Apartment, Registration, Student
from .forms import RegistrationForm


# Your original Student exercise.
def myView(request):
    if request.method == "POST":
        name = request.POST.get('name',"")
        age = request.POST.get('age',"")
        marks = request.POST.get('marks',"")
        total_marks = request.POST.get('totalmarks',"")

        percentage = int(marks)/float(total_marks) * 100

        Student.objects.create(name=name,age=int(age),marks=int(marks),total=int(total_marks))
        details = {
            'name':name,
            'age':age,
            'marks':marks,
            'total_marks':total_marks,
            'percentage':percentage
            }
        return render(request,'startpage.html',context=details)

    details = Student.objects.all()
    d = {'details':details}
    return render(request,'startpage.html',context=d)


# Two simple functions contain the fixed rules from the question.
def get_floor(flat_type):
    if flat_type == '3 BHK':
        return 0
    elif flat_type == '2 BHK':
        return 1
    else:
        return 2


def get_area(flat_type):
    if flat_type == '3 BHK':
        return 1200
    elif flat_type == '2 BHK':
        return 1000
    else:
        return 800


def home(request):
    return render(request, 'home.html')


# READ all apartments.
def display_apartments(request):
    apartments = Apartment.objects.all()
    return render(request, 'Apartment.html', {'apartments': apartments})


# READ all customers.
def display_registrations(request):
    customers = Registration.objects.all()
    return render(request, 'Customer.html', {'customers': customers})


# CREATE: validate form, check flat, save customer, reduce availability.
def register_flat(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            floor = get_floor(customer.flat_type)
            apartment = Apartment.objects.filter(
                apartment_name=customer.apartment_name, floor_number=floor
            ).first()

            if apartment is None:
                form.add_error(None, 'This apartment does not have the requested floor.')
            elif apartment.available_flats == 0:
                form.add_error(None, 'No flats available.')
            else:
                customer.total_cost = get_area(customer.flat_type) * apartment.price_per_sqft
                customer.save()
                apartment.available_flats -= 1
                apartment.save()
                return redirect('receipt', pk=customer.id)

    return render(request, 'Registration.html', {'form': form})


# READ one customer and display the receipt.
def receipt(request, pk):
    customer = get_object_or_404(Registration, id=pk)
    area = get_area(customer.flat_type)
    details = {
        'customer': customer,
        'floor': get_floor(customer.flat_type),
        'area': area,
        'rate': customer.total_cost / area,
    }
    return render(request, 'Receipt.html', details)


# UPDATE: instance=customer fills the form with the existing record.
def edit_registration(request, pk):
    customer = get_object_or_404(Registration, id=pk)
    old_floor = get_floor(customer.flat_type)
    old_apartment = Apartment.objects.filter(
        apartment_name=customer.apartment_name, floor_number=old_floor
    ).first()
    form = RegistrationForm(instance=customer)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            floor = get_floor(customer.flat_type)
            apartment = Apartment.objects.filter(
                apartment_name=customer.apartment_name, floor_number=floor
            ).first()

            if apartment is None:
                form.add_error(None, 'This apartment does not have the requested floor.')
            elif old_apartment is None:
                form.add_error(None, 'Previous inventory is missing or inconsistent.')
            elif apartment != old_apartment and apartment.available_flats == 0:
                form.add_error(None, 'No flats available.')
            else:
                # Only a change of flat needs an inventory and price change.
                if apartment != old_apartment:
                    old_apartment.available_flats += 1
                    old_apartment.save()
                    apartment.available_flats -= 1
                    apartment.save()
                    customer.total_cost = get_area(customer.flat_type) * apartment.price_per_sqft
                customer.save()
                return redirect('receipt', pk=customer.id)

    return render(request, 'Registration.html', {'form': form, 'editing': True})


# DELETE: return the flat, then delete the customer.
def delete_registration(request, pk):
    if request.method != 'POST':
        return HttpResponse('Please use the Delete button.', status=405)

    customer = get_object_or_404(Registration, id=pk)
    floor = get_floor(customer.flat_type)
    apartment = Apartment.objects.filter(
        apartment_name=customer.apartment_name, floor_number=floor
    ).first()
    if apartment is None:
        return HttpResponse('Apartment inventory not found.', status=404)

    apartment.available_flats += 1
    apartment.save()
    customer.delete()
    return redirect('display_registrations')
