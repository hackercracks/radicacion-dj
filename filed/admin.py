from django.contrib import admin
from .models import FileType, StateType, File, Agent, Category, VeriyDoc
# Register your models here.
admin.site.register(File)
admin.site.register(FileType)
admin.site.register(StateType)
admin.site.register(Agent)
admin.site.register(Category)
admin.site.register(VeriyDoc)