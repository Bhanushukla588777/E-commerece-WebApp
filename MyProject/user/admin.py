from django.contrib import admin

# Register your models here.
from .models import *


class contactusAdmin(admin.ModelAdmin):
    list_display = ("name","email","mobile","message")
admin.site.register(contact,contactusAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ('id',"cname","cpic","cdate")
admin.site.register(category,categoryAdmin)

class signupAdmin(admin.ModelAdmin):
    list_display = ("name","father","mother","email","dob","contact","passwd","ppic","address")
admin.site.register(signup,signupAdmin)

class productsAdmin(admin.ModelAdmin):
    list_display = ('id',"name","ppic","color","tprice","disprice","pdes","category","pdate")
admin.site.register(products,productsAdmin)

class signinAdmin(admin.ModelAdmin):
    list_display = ("email","passwd")
admin.site.register(signin,signinAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display = ('id',"pid","userid","remarks","status","odate")
admin.site.register(order,orderAdmin)

class addtocartAdmin(admin.ModelAdmin):
    list_display = ('id',"pid","userid","status","cdate")
admin.site.register(addtocart,addtocartAdmin )