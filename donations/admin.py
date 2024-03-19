from django.contrib import admin

# Register your models here.


from .models import Donation

admin.site.register(Donation)