from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from yatra.models import City, Destination, DetailedDescription, PassengerDetail, Transaction, Newsletter, Contact, BlogPost
from .forms import CityForm, DestinationForm, DetailedDescriptionForm, PassengerDetailForm, TransactionForm, BlogPostForm

@staff_member_required
def dashboard(request):
    user_count = User.objects.count()
    destinations = Destination.objects.all()
    transactions = Transaction.objects.all()
    subscribers = Newsletter.objects.count()
    contacts_count = Contact.objects.count()
    blogposts_count = BlogPost.objects.count()

    return render(request, 'adminpanel/dashboard.html', {
        'user_count': user_count,
        'destinations': destinations,
        'transactions': transactions,
        'subscribers': subscribers,
        'contacts_count': contacts_count,
        'blogposts_count': blogposts_count,
    })

# --- City CRUD ---

@staff_member_required
def city_list(request):
    cities = City.objects.all()
    return render(request, 'adminpanel/city_list.html', {'cities': cities})

@staff_member_required
def city_create(request):
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_city_list')
    else:
        form = CityForm()
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Add City'})

@staff_member_required
def city_edit(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES, instance=city)
        if form.is_valid():
            form.save()
            return redirect('admin_city_list')
    else:
        form = CityForm(instance=city)
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Edit City'})

@staff_member_required
def city_delete(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        city.delete()
        return redirect('admin_city_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': city})

# --- Destination CRUD ---

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
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Add Destination'})

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
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Edit Destination'})

@staff_member_required
def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('admin_destination_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': destination})

# --- DetailedDescription CRUD ---

@staff_member_required
def detail_list(request):
    details = DetailedDescription.objects.all()
    return render(request, 'adminpanel/detail_list.html', {'details': details})

@staff_member_required
def detail_create(request):
    if request.method == 'POST':
        form = DetailedDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_detail_list')
    else:
        form = DetailedDescriptionForm()
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Add Detail'})

@staff_member_required
def detail_edit(request, pk):
    detail = get_object_or_404(DetailedDescription, pk=pk)
    if request.method == 'POST':
        form = DetailedDescriptionForm(request.POST, request.FILES, instance=detail)
        if form.is_valid():
            form.save()
            return redirect('admin_detail_list')
    else:
        form = DetailedDescriptionForm(instance=detail)
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Edit Detail'})

@staff_member_required
def detail_delete(request, pk):
    detail = get_object_or_404(DetailedDescription, pk=pk)
    if request.method == 'POST':
        detail.delete()
        return redirect('admin_detail_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': detail})

# --- PassengerDetail CRUD ---

@staff_member_required
def passenger_list(request):
    passengers = PassengerDetail.objects.all()
    return render(request, 'adminpanel/passenger_list.html', {'passengers': passengers})

@staff_member_required
def passenger_create(request):
    if request.method == 'POST':
        form = PassengerDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_passenger_list')
    else:
        form = PassengerDetailForm()
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Add Passenger'})

@staff_member_required
def passenger_edit(request, pk):
    passenger = get_object_or_404(PassengerDetail, pk=pk)
    if request.method == 'POST':
        form = PassengerDetailForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            return redirect('admin_passenger_list')
    else:
        form = PassengerDetailForm(instance=passenger)
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Edit Passenger'})

@staff_member_required
def passenger_delete(request, pk):
    passenger = get_object_or_404(PassengerDetail, pk=pk)
    if request.method == 'POST':
        passenger.delete()
        return redirect('admin_passenger_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': passenger})

# --- Transaction CRUD ---

@staff_member_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'adminpanel/transaction_list.html', {'transactions': transactions})

@staff_member_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Add Transaction'})

@staff_member_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('admin_transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Edit Transaction'})

@staff_member_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('admin_transaction_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': transaction})

# --- Newsletter (List and Delete only) ---

@staff_member_required
def newsletter_list(request):
    subscribers = Newsletter.objects.all()
    return render(request, 'adminpanel/newsletter_list.html', {'subscribers': subscribers})

@staff_member_required
def newsletter_delete(request, pk):
    subscriber = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('admin_newsletter_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': subscriber})



# --- Contact CRUD (List + Delete only) ---
@staff_member_required
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'adminpanel/contact_list.html', {'contacts': contacts})

@staff_member_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('admin_contact_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': contact})


# --- BlogPost CRUD ---

@staff_member_required
def blogpost_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'adminpanel/blogpost_list.html', {'posts': posts})

@staff_member_required
def blogpost_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_blogpost_list')
    else:
        form = BlogPostForm()
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Add Blog Post'})

@staff_member_required
def blogpost_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin_blogpost_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'adminpanel/form.html', {'form': form, 'title': 'Edit Blog Post'})

@staff_member_required
def blogpost_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('admin_blogpost_list')
    return render(request, 'adminpanel/confirm_delete.html', {'object': post})


from django.contrib import messages

@staff_member_required
def admin_booking_list(request):
    bookings = PassengerDetail.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/admin_booking_list.html', {'bookings': bookings})

@staff_member_required
def admin_approve_booking(request, trip_id):
    booking = get_object_or_404(PassengerDetail, trip_id=trip_id)
    booking.approved = True
    booking.canceled = False
    booking.save()
    messages.success(request, f'Booking {trip_id} approved.')
    return redirect('admin_booking_list')

@staff_member_required
def admin_cancel_booking(request, trip_id):
    booking = get_object_or_404(PassengerDetail, trip_id=trip_id)
    booking.canceled = True
    booking.approved = False
    booking.save()
    messages.success(request, f'Booking {trip_id} canceled.')
    return redirect('admin_booking_list')