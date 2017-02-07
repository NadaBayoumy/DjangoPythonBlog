from django.contrib import admin
from .models import Category , Post , Reply ,ForbiddenWords

# Register your models here.
# class custom_category(admin.ModelAdmin):
#     list_display = ('','')
    

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(ForbiddenWords)