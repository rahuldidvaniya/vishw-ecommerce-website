from core.models import Products, Category, ProductImages, ProductReview, Wishlist, Brand
from .models import Products, ProductReview
from django.db.models import Avg
from django.contrib import messages
from userauths.models import Profile

 # Import the Profile model

def default(request):
    categories = Category.objects.all()
    wishlist = None  # Initialize wishlist variable
    profile_picture = None  # Initialize profile picture variable
    
    if request.user.is_authenticated:
        # Fetch wishlist items for authenticated users
        wishlist = Wishlist.objects.filter(user=request.user)
        
        # Fetch profile picture for authenticated users
        try:
            profile = Profile.objects.get(user=request.user)
            profile_picture = profile.image.url if profile.image else None
        except Profile.DoesNotExist:
            pass
    
    return {
        'categories': categories,
        'wishlist': wishlist,
        'profile_picture': profile_picture,
    }


def cart_total_amount(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                price_for_calculation = str(item['price']).replace(',', '')  # Convert to string before calling replace
                total_price = int(item['qty']) * float(price_for_calculation)
                cart_total_amount += total_price
            except (KeyError, ValueError) as e:
                # Handle the case where price_for_calculation is missing or not a valid float
                # For simplicity, you can log the error or ignore the problematic item
                print(f"Error processing item {p_id}: {e}")

    # Format the total amount without decimal places
    formatted_cart_total_amount = '{:,.0f}'.format(cart_total_amount)

    return {'cart_total_amount': formatted_cart_total_amount}




def get_products(request):
     products = Products.objects.all()
     wishlist = Wishlist.objects.all()
     mobile_phones = Products.objects.filter(mobile_phone=True)

     return {
         'products':products,
         'w':wishlist,
         "m":mobile_phones
     }






