from django.contrib import admin
from .models import Destination, DetailedDescription, PassengerDetail, Transaction, Contact, City, Newsletter

# Register your models here.
admin.site.register(City)
admin.site.register(Destination)
admin.site.register(DetailedDescription)
admin.site.register(PassengerDetail)
admin.site.register(Transaction)

admin.site.register(Newsletter)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message')


from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')

admin.site.register(BlogPost, BlogPostAdmin)