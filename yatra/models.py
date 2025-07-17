from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='city_images/')
    description = models.TextField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Destination(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="destinations")
    name = models.CharField(max_length=50)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class DetailedDescription(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="details")
    days = models.IntegerField(default=5)
    price = models.IntegerField(default=20000)
    rating = models.IntegerField(default=5)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    desc = models.TextField()
    day1 = models.CharField(max_length=200, blank=True)
    day2 = models.CharField(max_length=200, blank=True)
    day3 = models.CharField(max_length=200, blank=True)
    day4 = models.CharField(max_length=200, blank=True)
    day5 = models.CharField(max_length=200, blank=True)
    day6 = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Details for {self.destination.name}"
    
# Model for passenger details associated with a trip
class PassengerDetail(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_same_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    trip_date = models.DateField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    num_passengers = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Trip ID: {self.trip_id}"


# Model for storing contact form submissions
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Model for transaction records
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    trip_same_id = models.IntegerField(default=1)
    amount = models.CharField(max_length=8)
    status = models.CharField(default="Failed", max_length=15)
    payment_method = models.CharField(max_length=15, blank=True)
    date_time = models.CharField(default=timezone.now().strftime('%Y-%m-%d %H:%M:%S'), max_length=19)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"



class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # for URLs
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email