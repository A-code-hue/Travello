from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from yatra.models import Destination, Transaction, Newsletter
from .forms import DestinationForm

@staff_member_required
def dashboard(request):
    user_count = User.objects.count()
    destinations = Destination.objects.all()
    transactions = Transaction.objects.all()
    subscribers = Newsletter.objects.count()

    return render(request, 'adminpanel/dashboard.html', {
        'user_count': user_count,
        'destinations': destinations,
        'transactions': transactions,
        'subscribers': subscribers,
    })

@staff_member_required
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'adminpanel/destination_list.html', {'destinations': destinations})

@staff_member_required
def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_destination_list')
    else:
        form = DestinationForm()
    return render(request, 'adminpanel/destination_form.html', {'form': form, 'title': 'Add Destination'})

@staff_member_required
def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('admin_destination_list')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'adminpanel/destination_form.html', {'form': form, 'title': 'Edit Destination'})

@staff_member_required
def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('admin_destination_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': destination})
