from django.urls import path, include
#from core.views import index
from core import views

app_name = 'core'

urlpatterns = [
    #index page
    path('', views.index, name = "index"),

    #shop page
    path('products/', views.product_list, name = 'product'),

    #product-detail page
    path('product/<pid>/', views.product_detail_view, name = 'product-detail'),

    #category
    path('category/', views.category_list_view, name = 'category'),

    #category product list 
    path('category/<cid>/', views.category_product_list_view, name = 'category-product-list'),

    #tag product list
    path('products/tag/<slug:tag_slug>/', views.tag_list, name="tags"),
    
    #review
    path('ajax-add-review/<int:pid>/', views.ajax_add_review, name='ajax_add_review'),

    #search
    path('search/', views.search_view, name='search'),

    #filter-product
    #path('filter-product/', views.filter_product, name="filter-product"),

    #cart
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.cart_view, name='cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    path('update-cart', views.update_cart, name='update-cart'),

    #checkout
    path('checkout/', views.checkout_view, name='checkout'),

    #paypal payment
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-completed/', views.payment_completed_view, name='payment-completed'),
    path('payment-failed/', views.payment_failed_view, name='payment-failed'),
    
    #user profile
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('delete_contact/', views.delete_contact, name='delete-contact'),
    path('delete_address/', views.delete_address, name='delete-address'),

    #Brand
    path('brand/<bid>/', views.brand_product_list_view, name = 'brand-product-list'),

    #wishlist
    path('wishlist/', views.wishlist_view, name = 'wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/', views.remove_wishlist, name='remove-from-wishlist'),

    #contact us
    path('contact/', views.Contact_us_view, name='contact'),

    #order
    path('orders/', views.orders_view, name='Orders'),

    #invoice pdf download
    path('invoice/', views.Invoice, name='Invoice'),
    
    #get total cart amount every second
    #path('get_cart_total/', views.get_cart_total, name='get_cart_total')

    #determine the address selectd by the user on the invoice page
    path('update_selected_address/', views.update_selected_address, name='selected_address'),

    #stripe payment
    #path('create_checkout_session/', views.create_checkout_session, name='create-checkout-session'), 

    #privacy policy page
    path('privacy-policy/', views.privacy, name='privacy-policy'),


    #order invoice from order page
    path('order_invoice/<int:order_id>/' , views.order_invoice, name='Order_invoice'),

    #Terms-conditions page
    path('terms-conditions/', views.Terms_Conditions, name='terms-conditions'),

 
    



   
    






]