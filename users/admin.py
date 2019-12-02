from django.contrib import admin
from .models import FirebaseUser, Profile

admin.site.register(FirebaseUser)
admin.site.register(Profile)
