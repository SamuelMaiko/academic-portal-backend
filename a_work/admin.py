from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Work)
admin.site.register(WorkImage)
admin.site.register(WorkFile)
admin.site.register(DefaultWork)
admin.site.register(Type)