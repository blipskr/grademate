from django.contrib import admin

from .models import User, Group, Exam, Bet, Result

# Register your models here.

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(Bet)
admin.site.register(Result)