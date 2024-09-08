# Vishw - ECommerce Website

This project is a fully-featured e-commerce website built with Django. It includes product listing, filtering, searching, a shopping cart, and checkout functionalities. The admin panel is customized using the **Jazzmin** theme for enhanced UI and UX.

## Features

- **Product Listings:** View a range of products with options to filter by price, category, and rating.
- **Product Search:** Easily search for products using a search bar.
- **Product Details:** Detailed view of each product, including images, price, and reviews.
- **Shopping Cart:** Add products to the cart, update quantities, and remove items.
- **Checkout Process:** Seamless checkout with shipping and payment options.
- **User Authentication:** Register, log in, and manage user accounts.
- **Jazzmin Admin Panel:** Customized admin interface using [Jazzmin](https://django-jazzmin.readthedocs.io/) for better usability and aesthetics.

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (default) or PostgreSQL (optional)
- **Admin Panel:** Jazzmin

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/django-ecommerce.git
    cd django-ecommerce
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the website:**

    Visit `http://127.0.0.1:8000/` in your browser to view the website.

8. **Admin Panel:**

    Visit `http://127.0.0.1:8000/admin/` to access the admin panel, which is styled with **Jazzmin**.

## Customization

- **Jazzmin Theme:** The admin panel's appearance and functionality have been enhanced using Jazzmin, making it more user-friendly.
- **Product Management:** Admin users can easily manage products, categories, and brands from the admin panel.


