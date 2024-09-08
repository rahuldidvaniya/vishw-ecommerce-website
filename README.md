Vishw Electronics - E-commerce Website
This is a fully functional e-commerce website built using Django, a high-level Python web framework. The project includes essential features like product listing, filtering, user authentication, cart functionality, and order management. It also incorporates various templates for dynamic content rendering and uses third-party libraries to enhance the functionality.

Features
Product Management: Admins can add, update, or delete products with details such as price, description, and categories.
Product Filtering: Users can filter products by categories, brands, price range, and ratings.
Cart Functionality: Users can add products to a shopping cart, update product quantities, and view the total price.
User Authentication: Includes registration, login, logout, and profile management features.
Order Management: Users can place orders and view their order history.
Search Functionality: Users can search for products by name or category.
Responsive Design: Fully responsive UI that adapts to different devices (mobile, tablet, desktop).
 **Jazzmin Admin Panel:** Customized admin interface using [Jazzmin](https://django-jazzmin.readthedocs.io/) for better usability and aesthetics.
 
Tech Stack
Backend: Django (Python)
Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
Database: SQLite (can be configured to use PostgreSQL or MySQL)
Authentication: Django's built-in authentication system
Media Management: Django's FileField for product images
Static Files Management: Django's static files handling system


Installation
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.7 or higher
Django 4.x
Git
Virtualenv
Step-by-Step Guide
Clone the repository:

git clone https://github.com/your-username/django-ecommerce.git
cd django-ecommerce
Create a virtual environment:

python -m venv env
Activate the virtual environment:

On Windows:
env\Scripts\activate

On macOS/Linux:
source env/bin/activate

Install dependencies:
pip install -r requirements.txt
Set up the database:

Run migrations to set up the database schema:
python manage.py migrate
Create a superuser (admin):

python manage.py createsuperuser
Follow the prompts to create an admin user for accessing the admin dashboard.


Run the development server:
python manage.py runserver
Access the website:

Open your browser and visit http://127.0.0.1:8000 to see the website.

Access the Admin Dashboard:

Visit http://127.0.0.1:8000/admin to log in as an admin and manage products, categories, and orders.


