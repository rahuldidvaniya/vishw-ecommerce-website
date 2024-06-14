from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg
from django.conf import settings
from django.utils import timezone
from userauths.models import Address

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING_CHOICES = [
    (1, 'One Star'),
    (2, 'Two Stars'),
    (3, 'Three Stars'),
    (4, 'Four Stars'),
    (5, 'Five Stars'),
]

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="TVs", unique=True)
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src ="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    
class Brand(models.Model):
    bid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Apple", unique=True)
    image = models.ImageField(upload_to="brand", default="brand.jpg")
    banner_image = models.ImageField(upload_to="brand", default="brand.jpg")

    class Meta:
        verbose_name_plural = "Brands"

    def brand_image(self):
        return mark_safe('<img src ="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

class Tags(models.Model):
    pass



class Products(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name = "category")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name = "brand")
    title = models.CharField(max_length=100, default="TV", unique=True)
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is a product")
    link_video = models.CharField(max_length=100, default="www.youtube.com")

    price = models.CharField(max_length=20, default="1.99")
    old_price = models.CharField(max_length=20, default="1.99")

    specifications = RichTextUploadingField(null=True, blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=True)
    mobile_phone = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src ="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title if self.title else "No title"

    def get_percentage(self):
        if self.old_price and self.price:
            # Remove commas and convert to float
            old_price = float(self.old_price.replace(',', ''))
            price = float(self.price.replace(',', ''))

            # Calculate the percentage
            return round(((price - old_price) / old_price) * 100, 2)

        return 0.0  # Default value if prices are not available
    
    def get_average_rating(self):
        # Calculate the average rating for the product's reviews
        return self.reviews.aggregate(Avg('rating'))['rating__avg']
    
    def decrease_quantity(self, ordered_quantity):
        """Decrease the product quantity when an order is placed."""
        if ordered_quantity <= self.quantity:
            self.quantity -= ordered_quantity
            self.save()
        else:
            raise ValueError("Ordered quantity cannot be greater than available quantity.")

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product.images", default="product.jpg")
    product = models.ForeignKey(Products, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

####################################################### Cart, Order, OrderItems and Address ###################################################

  



###################################### Product Review Wishlist Address ######################################################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title if self.product and self.product.title else "No product title"
    def get_rating(self):
        return self.rating
    
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title


    

#contact us model
class Contact_Us(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

from django.db import models
from django.conf import settings






class Order(models.Model):
    ORDER_RECEIVED = 'received'
    ORDER_PROCESSED = 'processed'
    ORDER_SHIPPED = 'shipped'
    ORDER_DELIVERED = 'delivered'

    ORDER_STATUS_CHOICES = [
        (ORDER_RECEIVED, 'Order Received'),
        (ORDER_PROCESSED, 'Order Processed'),
        (ORDER_SHIPPED, 'Order Shipped'),
        (ORDER_DELIVERED, 'Order Delivered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.AutoField(primary_key=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Order Received')
    total_items = models.IntegerField()
    sub_total = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.CharField(max_length=200)
    order_time = models.DateTimeField(default=timezone.now)
    address = models.ForeignKey('userauths.Address', on_delete=models.CASCADE, null=True)
    selected_address_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.get_order_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Sale(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='sales')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(null=False, blank=False)

    def __str__(self):
        return self.title
    
    
class TermAndConditions(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(null=False, blank=False)

    def __str__(self):
        return self.title


    
