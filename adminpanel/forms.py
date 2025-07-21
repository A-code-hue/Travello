from django import forms
from yatra.models import City, Destination, DetailedDescription, PassengerDetail, Transaction, Newsletter, Contact, BlogPost


from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep the current password."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'image', 'description', 'country']

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['city', 'name', 'img1', 'img2']

class DetailedDescriptionForm(forms.ModelForm):
    class Meta:
        model = DetailedDescription
        fields = [
            'destination', 'days', 'price', 'rating',
            'img1', 'img2', 'desc',
            'day1', 'day2', 'day3', 'day4', 'day5', 'day6',
        ]

class PassengerDetailForm(forms.ModelForm):
    class Meta:
        model = PassengerDetail
        fields = [
            'trip_same_id', 'first_name', 'last_name', 'age',
            'trip_date', 'payment', 'user', 'city', 'num_passengers'
        ]
        widgets = {
            'trip_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['username', 'trip_same_id', 'amount', 'status', 'payment_method', 'date_time']
        widgets = {
            'date_time': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'author', 'content', 'image', 'published']