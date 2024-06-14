from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    activation_code = models.CharField(max_length=6, blank=True, null=True)  # Field to store activation code
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name='profile')
    username = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="image", default=None, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    secondary_phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    

    def __str__(self):
        return self.first_name if self.first_name else str(self.user)



class Address(models.Model):
    TITLE_CHOICES = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('business', 'Business'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userauths_addresses')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, null=True, default='Home')
    street_address = models.TextField()
    city_district_town = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.title} - {self.street_address}, {self.city_district_town}, {self.state}, {self.pincode}'


