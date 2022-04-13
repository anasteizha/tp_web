from django.contrib import admin

# Register your models here.

from app.models import *


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(RatingQuestion)
admin.site.register(RatingAnswer)

