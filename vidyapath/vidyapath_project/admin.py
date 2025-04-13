from django.contrib import admin

# Register your models here.
from .models import Registration
from .models import PlacedStudent, Company


admin.site.register(PlacedStudent)
admin.site.register(Company)

admin.site.register(Registration)