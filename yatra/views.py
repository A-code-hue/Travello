from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    cities = City.objects.all()
    dests = Destination.objects.all()

    dest1 = []
    for i in range(6):
        try:
            temp = DetailedDescription.objects.get(destination_id=(i + 1) * 2)
            dest1.append(temp)
        except DetailedDescription.DoesNotExist:
            continue

    return render(request, 'index.html', {
        'cities': cities,
        'dests': dests,
        'dest1': dest1,
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
            auth.login(request, user)
            messages.info(request, 'Successfully Logged In')
            dests = Destination.objects.all()
            return render(request, 'index.html', {'dests': dests})
        else:
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


class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=1, max_value=100)


def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)

    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            trip_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            if trip_date < datetime.now().date():
                return redirect('index')

            try:
                obj = PassengerDetail.objects.get(trip_id=1)
            except PassengerDetail.DoesNotExist:
                return redirect('index')

            trip_same_id = obj.trip_same_id
            request.session['Trip_same_id'] = trip_same_id
            price = request.session.get('price', 20000)
            city = request.session.get('city', city_name)
            user = request.user

            for form in formset:
                PassengerDetail.objects.create(
                    trip_same_id=trip_same_id,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    age=form.cleaned_data['age'],
                    trip_date=trip_date,
                    payment=price,
                    user=user,
                    city=city
                )

            obj.trip_same_id += 1
            obj.save()

            total_passengers = formset.total_form_count()
            total_price = total_passengers * price
            gst = round(total_price * 0.13, 2)
            final_amount = total_price + gst

            request.session['pay_amount'] = final_amount

            return render(request, 'payment.html', {
                'no_of_person': total_passengers,
                'price1': total_price,
                'GST': gst,
                'final_total': final_amount,
                'city': city
            })

    else:
        formset = KeyValueFormSet()

    return render(request, 'sample.html', {'formset': formset, 'city_name': city_name})


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

@csrf_exempt
@login_required(login_url='login')
def verify_payment(request):
    if request.method == 'GET':
        pidx = request.GET.get('pidx')
        print(f"[verify_payment] Payment verification started with pidx={pidx}")

        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        headers = {
            'Authorization': 'key a870cce9f5cf4c8d812c9d30c6149d2d',  # Make sure this is your valid secret key
            'Content-Type': 'application/json',
        }
        data = json.dumps({'pidx': pidx})
        res = requests.post(url, headers=headers, data=data)
        new_res = res.json()
        print(f"[verify_payment] Khalti lookup response: {new_res}")

        if new_res.get('status') == 'Completed':
            username = request.user.get_username()
            trip_same_id = request.session.get('Trip_same_id')
            pay_amount = request.session.get('pay_amount')

            print(f"[verify_payment] Session Data - username: {username}, trip_same_id: {trip_same_id}, pay_amount: {pay_amount}")

            if not trip_same_id or not pay_amount:
                print("[verify_payment] Missing trip_same_id or pay_amount in session. Cannot create transaction.")
                messages.error(request, "Session expired or invalid payment details.")
                return redirect('index')

            amount_str = str(pay_amount)

            Transaction.objects.create(
                username=username,
                trip_same_id=trip_same_id,
                amount=amount_str,
                payment_method='Khalti',
                status='Successful'
            )
            print("[verify_payment] Transaction created successfully.")

            # Do NOT update pay_done since field does not exist

            # Render a payment success page instead of redirecting immediately
            return render(request, 'payment_success.html', {
                'amount': amount_str,
                'trip_id': trip_same_id,
                'username': username,
            })
        else:
            print(f"[verify_payment] Payment not completed or failed. Status: {new_res.get('status')}")
            messages.error(request, "Payment verification failed or incomplete.")
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