from django.contrib import admin
from .models import Products, Category, ProductImages, ProductReview, Wishlist, Brand, Contact_Us, Order, OrderItem, Sale, PrivacyPolicy, TermAndConditions
from userauths.models import Address
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import FileResponse
import io
import datetime


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'featured', 'product_status', 'pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand_image']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_product_title', 'get_product_image', 'review', 'rating']

    def get_product_title(self, obj):
        return obj.product.title if obj.product else 'No product'
    get_product_title.short_description = 'Product Title'  # Sets column name in admin panel

    def get_product_image(self, obj):
        return format_html('<img src="{}" alt="{}" style="max-height: 100px; max-width: 100px;" />',
                           obj.product.image.url, obj.product.title) if obj.product else 'No image'
    get_product_image.short_description = 'Product Image'  # Sets column name in admin panel

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False





class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    def has_change_permission(self, request, obj=None):
        return False

class Contact_usAdmin(admin.ModelAdmin):
    list_display=['name', 'email', 'date', 'message']

    def has_change_permission(self, request, obj=None):
        return False






from django.contrib import admin
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product_image','product', 'quantity']
    extra = 0
    can_delete = False
    can_add_related = False

    def product_image(self, obj):
        return format_html('<img src="{}" alt="{}" style="max-height: 100px; max-width: 100px;" />',
                           obj.product.image.url, obj.product.title)
    product_image.short_description = 'Product Image'




class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'order_status', 'total_items', 'total_paid', 'address', 'order_time']
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj: # when editing an object
            return ['order_id', 'user', 'total_items', 'total_paid', 'address', 'order_time', 'sub_total', 'discount', 'delivery_fee', 'selected_address_id']
        else:
            return []

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from django.http import FileResponse
import datetime
import io

class SaleAdmin(admin.ModelAdmin):
    list_display = ['order', 'quantity', 'date']
    actions = ['generate_daily_report','generate_monthly_report', 'generate_yearly_report']

    def generate_report(self, request, queryset, interval='day'):
        # Get the current date
        current_date = datetime.datetime.now()

        # Filter sales queryset by the given interval
        if interval == 'day':
            queryset = queryset.filter(date__date=current_date)
        elif interval == 'week':
            # Calculate the start and end dates for the last week
            last_week_start = current_date - datetime.timedelta(days=current_date.weekday() + 7)
            last_week_end = current_date - datetime.timedelta(days=current_date.weekday() + 1)
            queryset = queryset.filter(date__date__range=[last_week_start, last_week_end])
        elif interval == 'month':
            queryset = queryset.filter(date__year=current_date.year, date__month=current_date.month)
        elif interval == 'year':
            queryset = queryset.filter(date__year=current_date.year)

        # Calculate total number of orders and total price for the interval
        total_orders = queryset.count()
        total_price = sum(int(sale.product.price.replace(',', '')) * sale.quantity for sale in queryset)
        total_price_with_commas = "{:,}".format(total_price)  # Format total_price with commas

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

        # Prepare data for the table
        if interval == 'day':
            data = [['Date', 'Total Orders', 'Total Price']]  # Changed 'Interval' to 'Date'
            data.append([current_date.strftime("%Y-%m-%d"), total_orders, total_price_with_commas])  # Added date here
        elif interval == 'year':
            data = [['Year', 'Total Orders', 'Total Price']]  # Changed 'Interval' to 'Year'
            data.append([str(current_date.year), total_orders, total_price_with_commas])  # Added current year here
        else:
            data = [['Interval', 'Total Orders', 'Total Price']]
            data.append([interval.capitalize(), total_orders, total_price_with_commas])

        # Create a Table object with adjusted column widths
        table = Table(data, colWidths=[100, 100, 100])

        # Add a TableStyle to handle text wrapping and other style elements
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
        ])
        table.setStyle(style)

        # Add the Table object to the PDF
        elements = [table]

        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'sales_report_{interval}_{current_date.strftime("%Y-%m-%d")}.pdf')

    def generate_daily_report(self, request, queryset):
        return self.generate_report(request, queryset, interval='day')
    generate_daily_report.short_description = 'Generate Daily Sales Report'

    """
    def generate_weekly_report(self, request, queryset):
        return self.generate_report(request, queryset, interval='week')
    generate_weekly_report.short_description = 'Generate Weekly Sales Report'
    """

    def generate_monthly_report(self, request, queryset):
        return self.generate_report(request, queryset, interval='month')
    generate_monthly_report.short_description = 'Generate Monthly Sales Report'

    def generate_yearly_report(self, request, queryset):
        return self.generate_report(request, queryset, interval='year')
    generate_yearly_report.short_description = 'Generate Yearly Sales Report'
    
    """
    def generate_product_sales_report(self, request, queryset):
        # Get the current date
        current_date = datetime.datetime.now()

        # Prepare data for the table
        data = [['Product', 'Total Orders', 'Total Price']]
        for product in Products.objects.all():
            product_sales = queryset.filter(product=product)
            total_orders = product_sales.count()
            total_price = sum(int(sale.product.price.replace(',', '')) * sale.quantity for sale in product_sales)
            total_price_with_commas = "{:,}".format(total_price)  # Format total_price with commas
            data.append([product.title, total_orders, total_price_with_commas])

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

        # Create a Table object with adjusted column widths
        table = Table(data, colWidths=[200, 100, 100])

        # Add a TableStyle to handle text wrapping and other style elements
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
        ])
        table.setStyle(style)

        # Add the Table object to the PDF
        elements = [table]

        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'product_sales_report_{current_date.strftime("%Y-%m-%d")}')
    from .models import Category"""


    # Your existing code...

    
 
class PrivacyAdmin(admin.ModelAdmin):
    list_display = ['title']

class terms_conditionsAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Sale, SaleAdmin)





admin.site.register(Products, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Contact_Us, Contact_usAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(OrderItem)
admin.site.register(PrivacyPolicy, PrivacyAdmin)
admin.site.register(TermAndConditions, terms_conditionsAdmin)







    


