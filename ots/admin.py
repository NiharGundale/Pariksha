from django.contrib import admin
from ots.models import Candidate,Question,Result

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Question)
admin.site.register(Result)

