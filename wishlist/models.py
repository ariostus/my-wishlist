from django.db import models
import datetime
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles')

    def __str__(self):
        return self.user.username


class WishList(models.Model):
    title = models.CharField(max_length=100, help_text="Your wishlist's title")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    description = models.TextField(max_length=300, help_text="A brief description of your wishlist", blank=True, null=True, default=' ')

    def __str__(self):
        return f"{self.title} - {self.author}"
    
    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('wish-list', args=[str(self.id)])


    




class WishlistElement(models.Model):
    name = models.CharField(max_length=100, help_text="Choose a name for your wish")
    date = models.DateField(default=datetime.date.today)
    notes = models.TextField(max_length=1000, help_text="Enter optional notes", null=True, blank=True)
    link = models.URLField(help_text="Link(s) to buy your product", null=True, blank=True)
    status = models.BooleanField(help_text="Have you realized your wish?", default=False)
    list = models.ForeignKey(WishList, on_delete=models.CASCADE, null=True)



    def __str__(self):
        """String for representing wishlist element model"""
        return self.name


    class Meta:
        ordering = ['status', '-date']
    
    def get_absolute_url(self):
        return reverse("wish-detail", args=[str(self.id)])
    


