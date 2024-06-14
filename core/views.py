from django.shortcuts import render, get_object_or_404
from core.models import Products, Category, ProductImages, ProductReview, Wishlist, Brand, Contact_Us, Order, OrderItem, TermAndConditions
from taggit.models import Tag
from django.db.models import Count, Avg, Q
from core.forms import ProductReviewForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from userauths.models import Profile
from django.db.models import Avg
from .models import ProductReview
from dal import autocomplete
from django.core import serializers
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userauths.models import Profile, Address
from .forms import ProfileForm, ContactForm, AddressForm   
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import strip_tags
from django.db.models import F, FloatField, Value
from django.db.models.functions import Replace, Cast, Round
import pdfkit
import os
import locale
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib import messages
from django.shortcuts import render
from .models import Order, OrderItem
from datetime import timedelta
import locale
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML





def index(request):
    products = Products.objects.all().order_by('-id')[:15]
    category = Category.objects.annotate(n_products=Count('category'))
    featured_products = Products.objects.filter(featured=True)
    brands = Brand.objects.annotate(num_products=Count('brand'))
    mobile_phones = Products.objects.filter(mobile_phone=True)[:8]



    # Calculate average rating for each product
    for product in products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    for product in featured_products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    for product in mobile_phones:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    context = {
        "products": products,
        "category": category,
        "featured_products": featured_products,
        "brands": brands,
        "mobile_phones": mobile_phones
    }
    
    return render(request, 'Core/index.html', context)




def product_list(request):
    # Fetch all products
    all_products = Products.objects.all().order_by('-id')
    brands = Brand.objects.all()

    # Get selected category, brand, and price range from request parameters
    selected_category_ids = request.GET.getlist('category')
    selected_brand_ids = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_rating = request.GET.get('rating')

    print("minimum price: ", min_price)
    print("maximum price: ", max_price)

    # Filter products based on selected category, brand, and price range
    if selected_category_ids:
        all_products = all_products.filter(category__id__in=selected_category_ids)
    if selected_brand_ids:
        all_products = all_products.filter(brand__id__in=selected_brand_ids)
    if min_price and min_price != '':
        all_products = all_products.filter(price__gte=float(min_price))
    if max_price and max_price != '':
        all_products = all_products.filter(price__lte=float(max_price))
    if selected_rating and selected_rating != 'None':
        all_products = all_products.annotate(rounded_rating=Round(Avg('reviews__rating'))).filter(rounded_rating=selected_rating)

    # Calculate average rating for each product
    for product in all_products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    # Paginate filtered products
    paginator = Paginator(all_products, 12)  # Assuming 12 products per page
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Generate pagination URL with filters
    pagination_url = f"/products/?page={page_number}"
    if selected_category_ids:
        for category_id in selected_category_ids:
            pagination_url += f"&category={category_id}"
    if selected_brand_ids:
        for brand_id in selected_brand_ids:
            pagination_url += f"&brand={brand_id}"
    if min_price:
        pagination_url += f"&min_price={min_price}"
    if max_price:
        pagination_url += f"&max_price={max_price}"
    if selected_rating:
        pagination_url += f"&rating={selected_rating}"

    context = {
        "products": products,
        "selected_category_ids": selected_category_ids,
        "selected_brand_ids": selected_brand_ids,
        "brands": brands,
        "selected_rating": selected_rating,
        "pagination_url": pagination_url
    }

    return render(request, 'Core/shop-3column.html', context)




def category_list_view(request):
    categories = Category.objects.all()

    context = {

        "categories":categories,

    }
    return render(request, 'Core/all-category.html', context )





def category_product_list_view(request, cid):
    # Fetch all products related to the specific category
    category = Category.objects.get(cid=cid)
    all_products = Products.objects.filter(category=category).order_by('-id')
    brands = Brand.objects.all()

    # Get selected category, brand, and price range from request parameters
    selected_brand_ids = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_rating = request.GET.get('rating')

    print("minimum price: ", min_price)
    print("maximum price: ", max_price)

    # Filter products based on selected brand and price range
    if selected_brand_ids:
        all_products = all_products.filter(brand__id__in=selected_brand_ids)
    if min_price or max_price:
        all_products = all_products.annotate(
            price_num=Cast(
                Replace('price', Value(','), Value('')), 
                output_field=FloatField()
            )
        )
    if min_price and min_price != '':
        all_products = all_products.filter(price_num__gte=min_price)
    if max_price and max_price != '':
        all_products = all_products.filter(price_num__lte=max_price)

    if selected_rating and selected_rating != 'None':
        all_products = all_products.annotate(
            rounded_rating=Round(Avg('reviews__rating'))
        ).filter(rounded_rating=selected_rating)

    # Calculate average rating for each product
    for product in all_products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    # Paginate filtered products
    paginator = Paginator(all_products, 12)  # Assuming 12 products per page
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    # Generate pagination URL with filters
    pagination_url = f"/category/{cid}/?page={page_number}"
    if selected_brand_ids:
        for brand_id in selected_brand_ids:
            pagination_url += f"&brand={brand_id}"
    if min_price:
        pagination_url += f"&min_price={min_price}"
    if max_price:
        pagination_url += f"&max_price={max_price}"
    if selected_rating:
        pagination_url += f"&rating={selected_rating}"

    context = {
        "products": products,
        "selected_brand_ids": selected_brand_ids,  # Pass selected brand IDs to template
        "brands": brands,
        "selected_rating": selected_rating,
        "pagination_url": pagination_url,  # Pass pagination URL to template
        "category": category,  # Pass the selected category to the template
    }

    return render(request, 'Core/category-product-list.html', context)


from django.core.paginator import Paginator

def brand_product_list_view(request, bid):
    brand = Brand.objects.get(bid=bid)
    products = Products.objects.filter(brand=brand)
    categories = Category.objects.all()
    total_products_count = products.count()

    # Handle category filtering
    selected_category_id = request.GET.get('category')
    if selected_category_id and selected_category_id != 'all':
        products = products.filter(category__id=selected_category_id)
        selected_category_id = int(selected_category_id)  # Convert to integer

    # Calculate average rating for each product
    for product in products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    # Create a Paginator object
    paginator = Paginator(products, 10)  # Show 15 products per page

    # Get the page number from the GET request
    page_number = request.GET.get('page')

    # Get the products for the current page
    products = paginator.get_page(page_number)

    context = {
        "brand": brand,
        "products": products,
        "categories": categories,
        "selected_category_id": selected_category_id,  # Pass selected category ID to template
        "total_products_count": total_products_count,
                }
    return render(request, 'Core/brand-product-list.html', context)



from django.core.exceptions import ObjectDoesNotExist


def product_detail_view(request, pid):
    try:
        product = Products.objects.get(pid=pid)

        # Check if the user has a delivered order containing the current product
        user_has_delivered_order = False
        if request.user.is_authenticated:
            try:
                OrderItem.objects.get(order__user=request.user, order__order_status=Order.ORDER_DELIVERED, product=product)
                user_has_delivered_order = True
            except OrderItem.DoesNotExist:
                pass

        products = Products.objects.filter(category=product.category).exclude(pid=pid)
        for prod in products:
            prod.average_rating = ProductReview.objects.filter(product=prod).aggregate(Avg('rating'))['rating__avg']

        # Getting next and previous products
        try:
            next_product = Products.objects.filter(category=product.category, id__gt=product.id).order_by('id').first()
        except ObjectDoesNotExist:
            next_product = None

        try:
            previous_product = Products.objects.filter(category=product.category, id__lt=product.id).order_by('-id').first()
        except ObjectDoesNotExist:
            previous_product = None

        # Getting all reviews
        reviews = ProductReview.objects.filter(product=product).order_by("-id")

        # Getting average reviews
        average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
        rounded_avg = round(average_rating['rating']) if average_rating['rating'] is not None else 0

        user_profile_image_url = None
        if request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=request.user)
                if user_profile and user_profile.image:
                    user_profile_image_url = user_profile.image.url
            except Profile.DoesNotExist:
                pass

        # Product Review form
        review_form = ProductReviewForm()

        # Allow user to make review if they have a delivered order containing the product
        make_review = user_has_delivered_order

        p_images = product.p_images.all()

        context = {
            "product": product,
            "products": products,
            "make_review": make_review,
            "p_image": p_images,
            "review_form": review_form,
            "reviews": reviews,
            "average_rating": rounded_avg,
            "next_product": next_product,
            "previous_product": previous_product,
            "user_profile_image_url": user_profile_image_url,
        }

        return render(request, "Core/product-detail.html", context)

    except Products.DoesNotExist:
        # Handle the case where the product with given pid does not exist
        return HttpResponse("Product not found", status=404)





def tag_list(request, tag_slug=None):
    products = Products.objects.all().order_by("-id")
    brands = Brand.objects.all()

    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])


    context = {
        "products":products,
        "tag":tag,
        "brands":brands,
    }

    return render(request, "core/tag.html", context)




def ajax_add_review(request, pid):
    product = get_object_or_404(Products, pk=pid)
    user = request.user

    timestamp = timezone.now()
    user_username = user.username

    # Fetch user's profile image URL
    user_profile_image_url = None
    if user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=user)
            if user_profile.image:
                user_profile_image_url = user_profile.image.url
        except Profile.DoesNotExist:
            pass

    review_data = {
        'user': user.id,
        'product': product.id,
        'review': request.POST.get('review', ''),
        'rating': request.POST.get('rating', 0),
        'date': timestamp.date(),
    }

    review_form = ProductReviewForm(review_data)

    if review_form.is_valid():
        review_form.save()
        return JsonResponse({
            'bool': True,
            'context': {
                'user': user_username,
                'review': review_data['review'],
                'rating': review_data['rating'],
                'time': timestamp.strftime("%d %b, %Y"),
                'user_profile_image_url': user_profile_image_url,  # Include user's profile image URL in the response
            },
        })
    else:
        errors = dict((key, [error for error in value]) for key, value in review_form.errors.items())
        return JsonResponse({
            'bool': False,
            'errors': errors
        })



from django.http import QueryDict
from django.http import QueryDict
from django.shortcuts import render
from django.db.models import Avg, Q
from .models import Products, Brand, ProductReview


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search_view(request):
    query = request.GET.get("q")
    initial_products = Products.objects.all()
    brands = Brand.objects.all()

    for product in initial_products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    # Apply search query filter if present
    if query:
        initial_products = initial_products.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__title__icontains=query) |
            Q(tags__name__in=query.split()) |
            Q(specifications__icontains=query) |
            Q(brand__title__icontains=query)
        ).order_by("-date").distinct()
    
    for product in initial_products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    # Get selected category, brand, price range, and rating from request parameters
    selected_category_ids = request.GET.getlist('category')
    selected_brand_ids = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_rating = request.GET.get('rating')

    # Filter products based on initial search results and additional filters
    products = initial_products

    if selected_category_ids:
        products = products.filter(category__id__in=selected_category_ids)
    if selected_brand_ids:
        products = products.filter(brand__id__in=selected_brand_ids)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if selected_rating and selected_rating != 'None':
        products = products.filter(reviews__rating=selected_rating)

    # Pagination
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "query": query,
        "selected_category_ids": selected_category_ids,
        "selected_brand_ids": selected_brand_ids,
        "min_price": min_price,
        "max_price": max_price,
        "selected_rating": selected_rating,
        "pagination_url": f"/search/?q={query}&",
        "brands": brands
    }

    return render(request, "core/search.html", context)



"""
def filter_product(request):
    displayed_product_ids = request.GET.getlist('displayed_product_ids[]')
    categories = request.GET.getlist("category[]")
    print("Received categories:", categories)

    products = Products.objects.filter(id__in=displayed_product_ids).order_by("-id").distinct()

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    
    # Calculate average rating for filtered products
    for product in products:
        product.average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

    # Render the filtered products HTML template
    data = render_to_string("core/async/product-list.html", {"products": products})

    # Include average rating data in the AJAX response
    response_data = {
        "data": data,
        "average_ratings": {product.id: product.average_rating for product in products}
    }

    return JsonResponse(response_data)
"""



def add_to_cart(request):
    product_id = str(request.GET.get('id'))
    quantity = int(request.GET.get('qty'))
    old_price = int(request.GET.get('old_price'))

    # Format the product price with thousand separators
    price_without_decimal = '{:,.0f}'.format(float(request.GET.get('price').replace(',', '')))

    cart_product = {
        product_id: {
            'title': request.GET.get('title'),
            'qty': quantity,
            'price': price_without_decimal,
            'image': request.GET.get('image'),
            'pid': request.GET.get('pid'),
            'old_price': old_price,
            'stock': request.GET.get('stock'),
            'product_id': product_id
        }
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            # Product already in cart, return an error response
            return JsonResponse({"error": "Product already added in the cart"}, status=400)
        else:
            # Product not in cart, add it
            cart_data[product_id] = cart_product[product_id]

        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    total_cart_items = sum(item['qty'] for item in request.session['cart_data_obj'].values())

    # Calculate the new total amount
    new_total_amount = sum(float(item['price'].replace(',', '')) * int(item['qty']) for item in request.session['cart_data_obj'].values())

    # Format the new total amount without decimal places
    formatted_total_amount = '{:,.0f}'.format(new_total_amount)

    request.session.save()

    return JsonResponse({
        "data": request.session['cart_data_obj'],
        'totalcartitems': total_cart_items,
        'new_total_amount': formatted_total_amount
    })

def cart_view(request):
    cart_total_amount = 0
    total_quantity = 0  # Initialize total quantity

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Check if item['price'] is a string
            if isinstance(item['price'], str):
                price_for_calculation = item['price'].replace(',', '')
                if price_for_calculation:  # Check if the string is not empty
                    try:
                        total_price = int(item['qty']) * float(price_for_calculation)
                        item['total_price'] = '{:,.0f}'.format(total_price)  # Format total_price without decimal places
                        cart_total_amount += total_price
                        # Add quantity to total_quantity
                        total_quantity += int(item['qty'])
                    except ValueError:
                        # Handle the case where price_for_calculation is not a valid float
                        messages.warning(request, f"Invalid price for product with ID: {p_id}")
            else:
                # Handle the case where item['price'] is already a float
                try:
                    total_price = int(item['qty']) * item['price']
                    item['total_price'] = '{:,.0f}'.format(total_price)  # Format total_price without decimal places
                    cart_total_amount += total_price
                    # Add quantity to total_quantity
                    total_quantity += int(item['qty'])
                except ValueError:
                    messages.warning(request, f"Invalid price for product with ID: {p_id}")

        cart_total_amount = '{:,.0f}'.format(cart_total_amount)  # Format cart_total_amount without decimal places
        return render(request, "Core/cart.html", {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'total_quantity': total_quantity,  # Include total quantity in the context
        })
    else:
        messages.warning(request, "Your cart is empty")
        return render(request, "Core/cart.html")


def update_cart(request):
    product_id = str(request.GET.get('id'))
    quantity = int(request.GET.get('qty'))

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            # Product already in cart, update quantity
            cart_data[product_id]['qty'] = quantity
            request.session['cart_data_obj'] = cart_data
            request.session.save()

    # Calculate the new total amount
    new_total_amount = 0
    for item in request.session['cart_data_obj'].values():
        new_total_amount += float(item['price'].replace(',', '')) * int(item['qty'])

    # Calculate the updated price for the product
    updated_product_price = float(cart_data[product_id]['price'].replace(',', '')) * quantity

    return JsonResponse({'new_total_amount': new_total_amount, 'updated_product_price': updated_product_price})


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
           cart_data = request.session['cart_data_obj']
           del request.session['cart_data_obj'][product_id]
           request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Create a new variable 'price_for_calculation' without comma
            price_for_calculation = item['price'].replace(',', '')
            total_price = int(item['qty']) * float(price_for_calculation)
            item['total_price'] = '{:,.0f}'.format(total_price)  # Format total_price without decimal places
            cart_total_amount += total_price
        cart_total_amount = '{:,.0f}'.format(cart_total_amount)

    context = render_to_string("Core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount} )
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj']), 'new_total_amount': cart_total_amount})




@login_required
def checkout_view(request):
    cart_total_amount = 0
    sub_total_old_price = 0
    total_quantity = 0
    delivery_charges = 0
    in_stock_items = {}

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Check if the item is out of stock
            if item['stock'] == '0':
                messages.warning(request, f"Few products in your cart are out of stock and have been removed from your cart.")
            else:
                in_stock_items[p_id] = item
                price_for_calculation = item['price'].replace(',', '')
                total_price = int(item['qty']) * float(price_for_calculation)
                cart_total_amount += total_price
                
                old_price = float(str(item.get('old_price', '0')).replace(',', ''))
                sub_total_old_price += old_price * int(item['qty'])
                
                total_quantity += int(item['qty'])

        # Replace the session data with the in-stock items
        request.session['cart_data_obj'] = in_stock_items

        # If all items are out of stock, redirect to a different page
        if not in_stock_items:
            messages.warning(request, "All items in your cart are out of stock.")
            return redirect('core:cart')

        total_cart_amount_old_price = sub_total_old_price
    
        cart_total_amount = float(cart_total_amount)
        if cart_total_amount < 20000:
            delivery_charges = 100
        
        cart_total_amount += float(delivery_charges)
        
        cart_total_amount = '{:,.2f}'.format(cart_total_amount).rstrip('0').rstrip('.')
        sub_total_old_price = '{:,.2f}'.format(sub_total_old_price).rstrip('0').rstrip('.')
        total_cart_amount_old_price = '{:,.2f}'.format(total_cart_amount_old_price).rstrip('0').rstrip('.')

    discount = '{:,.2f}'.format(float(sub_total_old_price.replace(',', '')) - float(cart_total_amount.replace(',', ''))).rstrip('0').rstrip('.')
    profile = Profile.objects.get(user=request.user)
    address = Address.objects.filter(user=request.user).first()
    
    
    host = request.get_host()
    paypal_dict = {
       'business': settings.PAYPAL_RECEIVER_EMAIL,
       'amount': float(cart_total_amount.replace(',', '')),
       'item_name': "Order-Item-No-3",
       'invoice': "INVOICE_NO-3",
       'currency_code': "USD",
       'notify_url': 'http://{}{}'.format(host, reverse('core:paypal-ipn')),
       'return_url': 'http://{}{}'.format(host, reverse('core:payment-completed')),
       'cancel_url': 'http://{}{}'.format(host, reverse('core:payment-failed')),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    if request.method == 'POST':
        # Get the form data from the POST request
        form_data = request.POST
        print(form_data)

        # Check if the form is the address form
        if 'address-form' in form_data:
            # Create a new address with the form data
            address = Address(
                user=request.user,
                title=form_data.get('title'),
                street_address=form_data.get('address'),
                city_district_town=form_data.get('City/District/Town'),
                state=form_data.get('State'),
                pincode=form_data.get('Pincode'),
                first_name = form_data.get('first_name'),
                last_name = form_data.get('last_name')
            )
            # Save the new address
            address.save()

            messages.success(request, 'Your address has been added!')
            return redirect('core:checkout')
        

    if 'selected_address_id' in request.session and request.session['selected_address_id']:
     del request.session['selected_address_id']



    if 'selected_address_id' not in request.session and address:
        request.session['selected_address_id'] = address.id
  

    return render(request, "Core/checkout.html", {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'total_quantity': total_quantity,
        'sub_total_old_price': sub_total_old_price,
        'total_cart_amount_old_price': total_cart_amount_old_price,
        'discount': discount,
        'delivery_charges': delivery_charges,
        'paypal_payment_button': paypal_payment_button,
        'profile': profile,
        'address': address,
    })

from datetime import timedelta


from .models import Sale  # Import the Sale model


@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    total_quantity = 0
    discount = 0
    sub_total_old_price = 0
    

    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            price_for_calculation = str(item['price']).replace(',', '')
            total_price = int(item['qty']) * float(price_for_calculation)
            item['total_price'] = '{:,.2f}'.format(total_price)
            cart_total_amount += total_price
            total_quantity += int(item['qty'])
            sub_total_old_price += float(item.get('old_price', 0)) * int(item['qty'])

        user_address = Address.objects.filter(user=request.user).first()

        if user_address is None:
            # Redirect to the page where the user can add an address
            return redirect('core:payment-completed')

        # Calculate delivery charges
        delivery_charges = 0
        if float(cart_total_amount) < 20000:
            delivery_charges = 100

        # Add delivery charges to the cart total amount
        cart_total_amount += delivery_charges

        # Calculate discount
        discount = sub_total_old_price - cart_total_amount

        # Create the Order instance
        order = Order.objects.create(
            user=request.user,
            order_status=Order.ORDER_RECEIVED,
            total_items=total_quantity,
            sub_total=sub_total_old_price,
            discount=discount,
            delivery_fee=delivery_charges,
            total_paid=cart_total_amount,
            order_time=timezone.now(),
            address=user_address,
        )

        selected_address_id = request.session.get('selected_address_id')
        if selected_address_id:
            order.selected_address_id = selected_address_id
            order.save()

        for pid, item in request.session['cart_data_obj'].items():
            product = Products.objects.get(id=pid)
            order_item = OrderItem.objects.create(order=order, product=product, quantity=item['qty'])
            product.decrease_quantity(item['qty'])

            # Create Sale instance after OrderItem is created
            Sale.objects.create(product=product, order=order, quantity=item['qty'], date=timezone.now())
        

        order_id = order.order_id
        order_time = order.order_time
        
        delivery_time = order_time + timedelta(days=5)

        cart_data = request.session['cart_data_obj']
        request.session['invoice_data_obj'] = cart_data
        del request.session['cart_data_obj']

    payment_method = request.GET.get('payment_method')
    
    selected_address = Address.objects.get(id=selected_address_id) 

    return render(request, "Core/payment-completed.html", {
        "cart_data": cart_data,
        'totalcartitems': len(cart_data),
        'cart_total_amount': cart_total_amount,
        'total_quantity': total_quantity,
        'discount': '{:,.2f}'.format(discount).rstrip('0').rstrip('.'),
        'sub_total_old_price': '{:,.2f}'.format(sub_total_old_price).rstrip('0').rstrip('.'),
        'order_id': order_id,
        'order_time': order_time,
        'delivery_time': delivery_time,
        'delivery_fee': delivery_charges,
        'selected_address':selected_address,
        'payment_method' : payment_method
    })









"""
import stripe
from django.conf import settings
from django.http import JsonResponse

def create_checkout_session(request):
    # Set your Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Create a new Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Your Product Name',
                },
                'unit_amount': 2000,  # Amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://yourwebsite.com/success/',
        cancel_url='http://yourwebsite.com/cancel/',
    )

    # Return the session ID to the client-side JavaScript
    return JsonResponse({'sessionId': session.id})
"""






@login_required
def orders_view(request):
    # Fetch all orders for the current user
    orders = Order.objects.filter(user=request.user)
    order_count = orders.count()  # Calculate the order count

    # Fetch the OrderItems for each order and calculate the delivery time
    for order in orders:
        order.items = OrderItem.objects.filter(order=order)
        order.delivery_time = order.order_time + timedelta(days=5)  # Calculate delivery time

        # Check if the order is delivered
        order.is_delivered = order.order_status == Order.ORDER_DELIVERED

        # Fetch the selected address for this order
        try:
            address = Address.objects.get(id=order.selected_address_id)
            order.address = address  # Attach the address to the order
        except Address.DoesNotExist:
            # Handle the case where the address doesn't exist (optional)
            order.address = None

    # Prepare the context
    context = {
        'orders': orders,
        'order_count': order_count,
    }

    # Render the template with the context
    return render(request, 'Core/orders.html', context)





    

 

def payment_failed_view(request):
    return render(request, 'Core/payment-failed.html')




@login_required
def customer_dashboard(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        form_data = request.POST

        # Check if the form is the address form
        if 'address-form' in form_data:
            # Create a new address with the form data
            address = Address(
                user=request.user,
                title=form_data.get('title'),
                street_address=form_data.get('address'),
                city_district_town=form_data.get('City/District/Town'),
                state=form_data.get('State'),
                pincode=form_data.get('Pincode'),
                first_name = form_data.get('first_name'),
                last_name = form_data.get('last_name')
            )
            # Save the new address
            address.save()
            print(address)

            messages.success(request, 'Your address has been added!')
            return redirect('core:dashboard')

        else:
            # Get the current user's profile
            profile = Profile.objects.get(user=request.user)

            # Update the profile fields with the form data
            profile.first_name = form_data.get('first_name')
            profile.last_name = form_data.get('last_name')
            profile.email = form_data.get('email')
            profile.phone = form_data.get('phone')
            profile.secondary_phone = form_data.get('secondary_phone')

            # Handle the profile image separately as it's a file input
            if 'image' in request.FILES:
                profile.image = request.FILES['image']

            # Save the updated profile
            profile.save()

            messages.success(request, 'Your profile has been updated!')
            return redirect('core:dashboard')

    else:
        # Get the current user's profile
        profile = Profile.objects.get(user=request.user)
        addresses = request.user.userauths_addresses.all()

        # Render the profile edit page
        return render(request, 'Core/dashboard.html', {'profile': profile, 'address': addresses})


@login_required
def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        Address.objects.filter(id=address_id, user=request.user).delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})



@login_required
def delete_contact(request):
    if request.method == 'POST' and request.is_ajax():
        phone_type = request.POST.get('phone_type')
        phone_number = request.POST.get('phone_number')
        profile = Profile.objects.get(user=request.user)

        try:
            if phone_type == 'primary' and profile.phone == phone_number:
                profile.phone = None
            elif phone_type == 'secondary' and profile.secondary_phone == phone_number:
                profile.secondary_phone = None

            profile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False})

@login_required
def wishlist_view(request):
    # Filter wishlist items by the current user
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    context = {
        "w": wishlist_items
    }
    return render(request, "Core/wishlist.html", context)

@login_required
def add_to_wishlist(request):
    id = request.GET.get('id')
    if id:
        product = Products.objects.filter(id=id).first()
        if product:
            # Check if the product already exists in the wishlist for the current user
            wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
            if wishlist_count == 0:  # If product doesn't exist, add it to the wishlist
                new_wishlist = Wishlist.objects.create(
                    product=product,
                    user=request.user
                )
                # Return updated count of products in the wishlist for the current user
                updated_count = Wishlist.objects.filter(user=request.user).count()
                return JsonResponse({"success": True, "updated_count": updated_count})
            else:
                # If the product already exists, return a response indicating it wasn't added
                return JsonResponse({"success": False, "message": "Product already exists in wishlist"})
        else:
            return JsonResponse({"success": False, "message": "Invalid product ID"})
    else:
        return JsonResponse({"success": False, "message": "Product ID not provided"})


def remove_wishlist(request):
    id = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    product = Wishlist.objects.get(id=id)
    product.delete()

    # Get the updated count of products in the wishlist for the current user
    updated_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        "bool":True,
        "wishlist":wishlist,
        "updated_count": updated_count  # Add the updated count to the context
    }
    qs_json = serializers.serialize('json', wishlist)

    data = render_to_string("Core/async/wishlist-list.html")
    return JsonResponse({"data":data, "wishlist":qs_json, "updated_count": updated_count})  # Return the updated count in the response


import logging
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings  
# Add logging configuration
logger = logging.getLogger(__name__)

def Contact_us_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate email address
        if not email:
            logger.error("Email address is missing.")
            return redirect('core:contact')

        contact = Contact_Us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            contact.save()
            return redirect('core:index')
        except Exception as e:
            # Log the error
            logger.error(f"Error sending email: {e}")
            # Print the exception to console
            print(f"Error sending email: {e}")
            return redirect('core:contact')

    return render(request, 'Core/contact.html')










# Helper function to convert HTML to PDF



def render_to_pdf(template_src, context_dict, width=410, height=297):
    html_string = render_to_string(template_src, context_dict)
    pdf = HTML(string=html_string).write_pdf(pages=[{
        'size': (width, height),
        'margin': (0, 0, 0, 0),  # Setting margin to 0 to use entire page
    }])
    return pdf

@login_required
def Invoice(request):
    cart_total_amount = 0
    total_quantity = 0
    sub_total_old_price = 0
    discount = 0
    selected_address_id = request.session.get('selected_address_id')
    selected_address = Address.objects.get(id=selected_address_id)
    if request.user.is_authenticated:
        # Get the current user model instance
        current_user = request.user
    date_of_invoice = timezone.now().strftime("%d/%m/%Y")

    # Set locale for formatting with thousand separator
    locale.setlocale(locale.LC_ALL, '')

    # Retrieve the stored cart data from the session
    cart_data = request.session.get('invoice_data_obj', {})

    # Calculate totals and discount
    for p_id, item in cart_data.items():
        # Convert price to string and remove commas before conversion
        price_for_calculation = str(item['price']).replace(',', '')

        try:
            # Calculate total price for the current item
            total_price = int(item['qty']) * float(price_for_calculation)
            item['total_price'] = '{:,.0f}'.format(total_price)  # Format total_price without decimal places

            # Update cart totals
            cart_total_amount += total_price
            total_quantity += int(item['qty'])

            # Calculate sub total old price
            sub_total_old_price += float(item.get('old_price', 0)) * int(item['qty'])

        except ValueError:
            messages.warning(request, f"Invalid price for product with ID: {p_id}")

    # Calculate discount
    discount = sub_total_old_price - cart_total_amount

    # Format cart_total_amount, discount, and sub_total_old_price with thousand separator
    cart_total_amount_formatted = locale.format_string('%d', cart_total_amount, grouping=True)
    discount_formatted = locale.format_string('%d', discount, grouping=True)
    sub_total_old_price_formatted = locale.format_string('%d', sub_total_old_price, grouping=True)

    # Convert the HTML template with data to PDF using WeasyPrint
    pdf = render_to_pdf('Core/invoicePdf.html', {
    'cart_data': cart_data,
    'cart_total_amount': cart_total_amount_formatted,
    'total_quantity': total_quantity,
    'sub_total_old_price': sub_total_old_price_formatted,
    'discount': discount_formatted,
    'address' : selected_address,
    'user' : current_user,
    'date' : date_of_invoice, 

     }, width=400, height=400)  # Specify the desired width and height


    # Check if pdf is generated successfully
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Invoice.pdf'
        return response

    return HttpResponse("Error Rendering PDF", status=400)

def order_invoice(request, order_id):
    # Use get() instead of filter() to retrieve a single order
    order = Order.objects.get(order_id=order_id)
    # Use filter() to retrieve all order items related to the order
    order_items = OrderItem.objects.filter(order=order)
    date_of_invoice = timezone.now().strftime("%d/%m/%Y")

    if request.user.is_authenticated:
        # Get the current user model instance
        current_user = request.user

    try:
        address = Address.objects.get(id=order.selected_address_id)
        order.address = address  # Attach the address to the order
    except Address.DoesNotExist:
        # Handle the case where the address doesn't exist (optional)
        order.address = None

    pdf = render_to_pdf('Core/Invoice.html', {
        'order': order,
        'user': current_user,
        'products': order_items,
        'date': date_of_invoice,
    }, width=400, height=400)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Invoice.pdf'
        return response

    return HttpResponse("Error Rendering PDF", status=400)





"""
def get_cart_total(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            price_for_calculation = str(item['price']).replace(',', '')
            total_price = int(item['qty']) * float(price_for_calculation)
            cart_total_amount += total_price
    return JsonResponse({'cart_total_amount': cart_total_amount})
"""




@login_required
def update_selected_address(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address_id')
        # Optionally, you can validate the selected_address_id here
        
        # Store the selected address ID in the session or any other storage mechanism
        request.session['selected_address_id'] = selected_address_id
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})



from django.shortcuts import render
from .models import PrivacyPolicy

def privacy(request):
    # Retrieve all PrivacyPolicy objects
    privacy_policies = PrivacyPolicy.objects.all()

    # Pass the queryset to the template context
    context = {
        'privacy_policies': privacy_policies
    }

    # Render the template with the context
    return render(request, "Core/privacy.html", context)


def Terms_Conditions(request):
    TC = TermAndConditions.objects.all()

    context = {
        'TC':TC
    }
   
    return render(request,"Core/terms-conditions.html", context)




"""
@login_required
def checkout_view(request):
    cart_total_amount = 0
    sub_total_old_price = 0
    total_quantity = 0
    delivery_charges = 0
    in_stock_items = {}

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            if item['stock'] == '0':
                messages.warning(request, f"Few products in your cart are out of stock and have been removed from your cart.")
            else:
                in_stock_items[p_id] = item
                price_for_calculation = item['price'].replace(',', '')
                total_price = int(item['qty']) * float(price_for_calculation)
                cart_total_amount += total_price
                
                old_price = float(str(item.get('old_price', '0')).replace(',', ''))
                sub_total_old_price += old_price * int(item['qty'])
                
                total_quantity += int(item['qty'])

        request.session['cart_data_obj'] = in_stock_items

        if not in_stock_items:
            messages.warning(request, "All items in your cart are out of stock.")
            return redirect('core:cart')

        total_cart_amount_old_price = sub_total_old_price
    
        cart_total_amount = float(cart_total_amount)
        if cart_total_amount < 20000:
            delivery_charges = 100
        
        cart_total_amount += float(delivery_charges)
        
        cart_total_amount = '{:,.2f}'.format(cart_total_amount).rstrip('0').rstrip('.')
        sub_total_old_price = '{:,.2f}'.format(sub_total_old_price).rstrip('0').rstrip('.')
        total_cart_amount_old_price = '{:,.2f}'.format(total_cart_amount_old_price).rstrip('0').rstrip('.')

    discount = '{:,.2f}'.format(float(sub_total_old_price.replace(',', '')) - float(cart_total_amount.replace(',', ''))).rstrip('0').rstrip('.')
    profile = Profile.objects.get(user=request.user)
    address = Address.objects.filter(user=request.user).first()
    
    host = request.get_host()

    if request.method == 'POST':
        form_data = request.POST
        logger.info("Form data received: %s", form_data)

        if 'address-form' in form_data:
            address = Address(
                user=request.user,
                title=form_data.get('title'),
                street_address=form_data.get('address'),
                city_district_town=form_data.get('City/District/Town'),
                state=form_data.get('State'),
                pincode=form_data.get('Pincode'),
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name')
            )
            address.save()
            messages.success(request, 'Your address has been added!')
            return redirect('core:checkout')

        if 'pay_now' in form_data:
            try:
                API = Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
                response = API.payment_request_create(
                    amount=str(cart_total_amount),
                    purpose='Order Payment',
                    send_email=False,
                    email="khatik.rk11@gmail.com",
                    redirect_url='http://127.0.0:8000/payment-completed/',
                )
                print(response)
                payment_request_url = response['payment_request']['longurl']
                logger.info("Instamojo payment request created successfully.")
                return redirect(payment_request_url)
          
            except Exception as e:
              logger.error("Error creating Instamojo payment request: %s", str(e))
              messages.error(request, f"Error: {str(e)}. Please try again later.")
              return HttpResponse("Error creating Instamojo payment request. Please try again later.")


    if 'selected_address_id' in request.session and request.session['selected_address_id']:
        del request.session['selected_address_id']

    if 'selected_address_id' not in request.session and address:
        request.session['selected_address_id'] = address.id
  
    logger.info("Rendering checkout page.")
    return render(request, "Core/checkout.html", {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'total_quantity': total_quantity,
        'sub_total_old_price': sub_total_old_price,
        'total_cart_amount_old_price': total_cart_amount_old_price,
        'discount': discount,
        'delivery_charges': delivery_charges,
        'profile': profile,
        'address': address,
    })
"""