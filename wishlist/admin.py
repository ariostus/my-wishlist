from django.contrib import admin
from .models import WishlistElement, WishList, UserProfile

admin.site.register(WishlistElement)
admin.site.register(WishList)
admin.site.register(UserProfile)