from django.contrib import admin
from appUser.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# adminview
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

   list_display = ('user','title', 'islogin')
   search_fields = ('title','user__username')
   
   
@admin.register(Packed)
class PackedAdmin(admin.ModelAdmin):

   list_display = ('title', 'price','pre','spor','sinema','slug')
 
   # bu kısmı admşnde gzliyoruz fakat modelde gizelmiyoruz çünkü içerisinde kayıt yaptırabiliyoruz   
# @admin.register(Userinfo)
# class UserinfoAdmin(admin.ModelAdmin):

#    list_display = ('user','tel', 'packed')

# burada stacedimnline classını bağlıyoruz
class UsermyInline(admin.StackedInline):
   model =  Usermy  #bağlamak istediğimiz modeli seçiyoruz 
   max_num = 1
   can_delete = False
   
   
class CustomUser(UserAdmin): # burada bağlantı işlemini yeni bnir clasa atıyoruz 
   inlines= [UsermyInline]
   
admin.site.unregister(User) # unut diyoruz ve admin.site.register(User,CustomUser) # tekrar register ediyoruz
admin.site.register(User,CustomUser)  # tekrar register ediyoruz