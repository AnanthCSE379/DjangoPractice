from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Asset
from .forms import RegistrationForm


def register(request):
    if not request.user.is_staff:
        return redirect('admin:login')

    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Asset added successfully')
            return redirect('assets:list')
    return render(request,'assets/asset_form.html',context={"form":form})


def display(request):
    if not request.user.is_staff:
        return redirect('admin:login')

    details = Asset.objects.order_by('-created_at')
    return render(request,'assets/asset_list.html',context={"details":details})


def delete(request,pk):
    if not request.user.is_staff:
        return redirect('admin:login')

    asset = get_object_or_404(Asset,id=pk)
    # GET shows the confirmation. Only POST deletes the record.
    if request.method == "POST":
        asset.delete()
        messages.success(request,'Asset deleted successfully')
        return redirect('assets:list')
    return render(request,'assets/asset_confirm_delete.html',context={"asset":asset})
