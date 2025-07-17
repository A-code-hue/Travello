from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.forms import formset_factory
from django.http import JsonResponse
from datetime import datetime
import json
import requests
from django import forms

from .models import Destination, DetailedDescription, PassengerDetail, Transaction, Contact, City, Newsletter
from .forms import ContactForm
from .utils import recommend_tours


# Home Page
def index(request):
    if request.method == 'POST':
        preference = request.POST.get('preference')
        if preference:
            request.session['preference'] = preference
            return redirect('index')  # prevent scroll and re-submit

    cities = City.objects.all()
    dests = Destination.objects.all()

    dest1 = []
    for i in range(6):
        try:
            temp = DetailedDescription.objects.get(destination_id=(i + 1) * 2)
            dest1.append(temp)
        except DetailedDescription.DoesNotExist:
            continue

    # Get preference from session (optional display)
    preference = request.session.pop('preference', None)

    return render(request, 'index.html', {
        'cities': cities,
        'dests': dests,
        'dest1': dest1,
        'preference': preference,
    })


# User Registration
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username'] 
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already Taken')
            return redirect('register')

        User.objects.create_user(username=username, password=password1, email=email, last_name=last_name, first_name=first_name).save()
        messages.info(request, 'User Created Successfully')
        return redirect('login')

    return render(request, 'register.html')


# User Login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_login(request, user)

            # Redirect superuser to admin dashboard
            if user.is_superuser:
                return redirect('admin_dashboard')

            # Normal user goes to index
            dests = Destination.objects.all()
            return render(request, 'index.html', {'dests': dests})
        else:
            from django.contrib import messages
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'login.html')


# User Logout
def logout(request):
    auth.logout(request)
    return redirect('index')


# About Page
def about(request):
    return render(request, 'about.html')


# List Destinations by City
@login_required(login_url='login')
def destination_list(request, city):
    dests = DetailedDescription.objects.filter(destination__city__name=city)
    return render(request, 'travel_destination.html', {'dests': dests, 'city': city})


def destination_details(request, destination_name):
    dest = get_object_or_404(DetailedDescription, destination__name=destination_name)
    request.session['price'] = dest.price
    request.session['destination_name'] = destination_name
    return render(request, 'destination_details.html', {'dest': dest})

# Form class for each passenger
class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=1, max_value=100)

# Passenger detail submission view
@login_required
def pessanger_detail_def(request, city_name):
    # Get passenger count from GET or default to 1
    num_passengers = int(request.GET.get('num_passengers', 1))
    
    KeyValueFormSet = formset_factory(KeyValueForm, extra=0, min_num=1, validate_min=True)

    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        trip_date_str = request.POST.get('trip_date')

        if formset.is_valid() and trip_date_str:
            trip_date = datetime.strptime(trip_date_str, "%Y-%m-%d").date()
            if trip_date < datetime.now().date():
                return redirect('index')

            try:
                obj = PassengerDetail.objects.get(trip_id=1)
            except PassengerDetail.DoesNotExist:
                return redirect('index')

            trip_same_id = obj.trip_same_id
            price = request.session.get('price', 20000)
            city = request.session.get('city', city_name)
            user = request.user

            # Get ACTUAL number of submitted forms
            actual_passengers = formset.total_form_count()
            
            # Store all passenger details
            for form in formset:
                PassengerDetail.objects.create(
                    trip_same_id=trip_same_id,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    age=form.cleaned_data['age'],
                    trip_date=trip_date,
                    payment=price,
                    user=user,
                    city=city,
                    num_passengers=actual_passengers  # Store actual count
                )

            # Update trip ID
            obj.trip_same_id += 1
            obj.save()

            # Calculate payment details
            total_price = actual_passengers * price
            gst = round(total_price * 0.13, 2)
            final_amount = total_price + gst

            # Store ALL payment details in session
            request.session.update({
                'Trip_same_id': trip_same_id,
                'pay_amount': final_amount,
                'no_of_person': actual_passengers,
                'per_person_price': price,
                'total_before_tax': total_price,
                'gst_amount': gst,
                'final_amount': final_amount
            })

            return render(request, 'payment.html', {
                'no_of_person': actual_passengers,
                'price1': total_price,
                'GST': gst,
                'final_total': final_amount,
                'city': city,
                'Trip_id': trip_same_id
            })
    else:
        # For GET requests, create forms for the requested number of passengers
        formset = KeyValueFormSet(initial=[{} for _ in range(num_passengers)])

    context = {
        'formset': formset,
        'city_name': city_name,
        'num_passengers': num_passengers,
        'today': datetime.now().date().isoformat(),
    }
    return render(request, 'sample.html', context)



# Contact Form Submission
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']

        Contact.objects.create(name=name, phone=phone, email=email, message=message)
        return render(request, 'index.html', {'name': name})

    return render(request, 'contact.html')


# Upcoming Trips
@login_required(login_url='login')
def upcoming_trips(request):
    username = request.user.get_username()
    today = datetime.now().date()
    trips = PassengerDetail.objects.filter(username=username, pay_done=1, Trip_date__gte=today)
    return render(request, 'upcoming trip1.html', {'person': trips})


# Travel Recommendations
@login_required(login_url='login')
def get_recommendations(request):
    if request.method == 'POST':
        preference = request.POST.get('preference')
        recommendations = recommend_tours(preference)
        return render(request, 'recommendations.html', {'recommendations': recommendations.to_dict(orient='records')})
    return redirect('index')


# Khalti Payment Initiation
def initiate_payment(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    amount = request.POST.get('amount')

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": "Order01",
        "purchase_order_name": "Test Purchase",
        "customer_info": {
            "name": "Anish Gurung",
            "city": "Kathmandu",
            "username": "9869055270"
        }
    })
    headers = {
        'Authorization': 'key a870cce9f5cf4c8d812c9d30c6149d2d',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()
    return redirect(response_data.get('payment_url', '/'))

# Payment verification & summary
@csrf_exempt
@login_required(login_url='login')
def verify_payment(request):
    if request.method == 'GET':
        pidx = request.GET.get('pidx')
        if not pidx:
            messages.error(request, "Payment ID missing.")
            return redirect('index')

        print(f"[verify_payment] Starting verification for pidx={pidx}")

        # Khalti payment verification endpoint
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        headers = {
            'Authorization': 'key a870cce9f5cf4c8d812c9d30c6149d2d',
            'Content-Type': 'application/json',
        }
        data = json.dumps({'pidx': pidx})

        try:
            res = requests.post(url, headers=headers, data=data)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"[verify_payment] Error contacting Khalti API: {e}")
            messages.error(request, "Error verifying payment with Khalti.")
            return redirect('index')

        response_data = res.json()
        print(f"[verify_payment] Khalti response: {response_data}")

        if response_data.get('status') == 'Completed':
            username = request.user.get_username()
            trip_same_id = request.session.get('Trip_same_id')
            pay_amount = request.session.get('pay_amount')
            no_of_passengers = request.session.get('no_of_person')

            # Validate session data
            if not all([trip_same_id, pay_amount, no_of_passengers]):
                print("[verify_payment] Missing required session data for payment.")
                messages.error(request, "Session expired or payment details missing.")
                return redirect('index')

            # Create transaction record
            from yatra.models import Transaction  # Adjust import as needed
            Transaction.objects.create(
                username=username,
                trip_same_id=trip_same_id,
                amount=str(pay_amount),
                payment_method='Khalti',
                status='Successful'
            )
            print("[verify_payment] Transaction saved successfully.")

            # Calculate GST and subtotal
            gst = round(pay_amount * 0.13 / 1.13, 2)
            subtotal = pay_amount - gst
            per_person_price = round(pay_amount / no_of_passengers, 2)

            return render(request, 'payment_success.html', {
                'amount': pay_amount,
                'trip_id': trip_same_id,
                'username': username,
                'no_of_passengers': no_of_passengers,
                'per_person_price': per_person_price,
                'gst': gst,
                'subtotal': subtotal,
            })
        else:
            print(f"[verify_payment] Payment not completed. Status: {response_data.get('status')}")
            messages.error(request, "Payment verification failed or incomplete.")
            return redirect('index')

    # If not GET, redirect to home or show error
    messages.error(request, "Invalid request method.")
    return redirect('index')


# User's Booked Trips (History)
@login_required(login_url='login')
def data_fetch(request):
    trips = PassengerDetail.objects.filter(username=request.user.get_username())
    return render(request, 'data_fetch.html', {'person': trips})


from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, 'blog_detail.html', {'post': post})



def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(email=email)
                messages.success(request, 'Thank you for subscribing!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.warning(request, 'Please enter a valid email.')

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('index')