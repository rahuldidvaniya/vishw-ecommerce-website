console.log("working fineJLKFJLFJ");
/*function updateCartTotal() {
    $.get('/get_cart_total/', function(data) {
        // Format the cart total amount with a thousand separator and rupee sign
        var formattedAmount = '₹' + parseFloat(data.cart_total_amount).toLocaleString('en-IN');
        
        // Update the cart total amount element with the formatted value
        $('#cart-total-amount').text(formattedAmount);
        
        console.log("Cart total is updated");
    }); 
}

setInterval(updateCartTotal, 1000);
*/

// validation.js

// JavaScript function to enforce maximum character limit and disallow spaces for username field










$(document).ready(function() {
    // Smooth scrolling to the review section
    $('a[href^="#"]').on('click', function (event) {
        var target = $($(this).attr('href'));

        if (target.length) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top
            }, 1000);
        }
    });
});


$(document).ready(function() {
    $('#category-select').change(function() {
        var selectedCategory = $(this).val();
        
        // Always set the category parameter in the URL
        var url = window.location.pathname + '?category=' + selectedCategory;
        
        // Reload the page with the updated URL
        window.location.href = url;
    });
});





//Determine the selected address by user
$(document).ready(function() {
    // Event listener for when the user selects an address
    $('input[name="selected_address"]').change(function() {
        // Capture the value (address ID) of the selected radio button
        var selectedAddressId = $('input[name="selected_address"]:checked').val();
        console.log("The selected address id:", selectedAddressId);
        
        // Send an AJAX request to store the selected address ID
        $.ajax({
            url: '/update_selected_address/', // Update the URL as per your Django URL configuration
            type: 'post',
            data: {
                'selected_address_id': selectedAddressId
            },
            headers: {"X-CSRFToken": csrftoken},
            success: function(data) {
                // Handle success response if needed
            },
            error: function() {
                // Handle error if needed
            }
        });
    });

    $('.profile-card').click(function() {
        console.log("The Profile card is clicked");
        var radioButton = $(this).find('input[type=radio]');
        if (!radioButton.prop('checked')) {
            radioButton.prop('checked', true);
            radioButton.change();  // Manually trigger the change event
        }
    });
});





$(document).ready(function() {
        $('.modal-form').submit(function(event) {
            var form = $(this);
            var fields = form.find('input[type="text"], textarea, select');
            var hasEmptyField = false;

            fields.each(function() {
                if ($(this).val() === '') {
                    hasEmptyField = true;
                    return false; // Stop the loop early if an empty field is found
                }
            });

            if (hasEmptyField) {
                alert('Please fill in all fields.');
                event.preventDefault(); // Prevent form submission
            }
        });
});


$(document).ready(function () {
    $(".minPrice, .maxPrice").on('input', function() {
        // Remove non-numeric characters
        $(this).val($(this).val().replace(/[^\d]/g, ''));

        // Ensure maximum length is 6 digits
        if ($(this).val().length > 6) {
            $(this).val($(this).val().slice(0, 6));
        }
    });

    $(".minPrice, .maxPrice").on('keydown', function(event) {
        // Allow only numbers 0-9 and the backspace key
        if (!(event.key >= '0' && event.key <= '9' || event.key === 'Backspace')) {
            event.preventDefault();
        }
    });

    $(".minPrice, .maxPrice").on('paste', function(event) {
        // Prevent pasting non-numeric characters and restrict to 6 digits
        let clipboardData = event.originalEvent.clipboardData || window.clipboardData;
        let pastedData = clipboardData.getData('text').replace(/[^\d]/g, '');
        if (pastedData.length > 6) {
            pastedData = pastedData.slice(0, 6);
        }
        $(this).val(pastedData);
        event.preventDefault();
    });

    $(".minPrice, .maxPrice").on('blur', function() {
        // Ensure minimum price is not negative
        let minPrice = parseInt($(".minPrice").val()) || 0;
        if (minPrice < 0) {
            $(".minPrice").val(0);
        }

        // Ensure maximum price is not negative
        let maxPrice = parseInt($(".maxPrice").val()) || 0;
        if (maxPrice < 0) {
            $(".maxPrice").val(0);
        }
    });

    // Profile card click event
    $('.profile-card.address').on('click', function(){
        $('.profile-card.address').removeClass('active');
        $(this).addClass('active');
    });
});


//review functionality
$("#submit-template-review").click(function (e) {
    console.log("THIS IS THE BEGINNING OF THE REVIEW FUNCTION");
    e.preventDefault();

    // Get the product ID from the form's data attribute
    let productId = $("#template-review-form").data("product-id");

    // Get the value of the checked radio button
    let rating = $('input[name="rating"]:checked').length > 0 ? $('input[name="rating"]:checked').val() : null;

    let reviewData = {
        review: $("#template-review").val(),
        rating: rating,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    };
    console.log("Rating: " + rating);
    // Now, make the AJAX call

    $.ajax({
        data: reviewData,
        method: "POST",
        url: "/ajax-add-review/" + productId + "/",
        dataType: "json",
        success: function (res) {
            console.log("Review Saved to Db");
            console.log("User-profile image url:", res.context.user_profile_image_url);

            if (res.bool === true) {
                $("#review-res").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                // Convert the rating to a number
                let rating = parseInt(res.context.rating);

                let _html = '<ul class="review-list">';
                _html += '<li class="review-item">';
                _html += '<div class="review-media">';
                _html += '<a class="review-avatar" href="#">';
                if (res.context.user_profile_image_url) {
                    _html += '<img src="' + res.context.user_profile_image_url + '">';
                } else {
                    _html += '<img src="https://www.gravatar.com/avatar/2c7d99fe281ecd3bcd65ab915bac6dd5?s=250">';
                }
                _html += '</a>';
                _html += '<h5 class="review-meta">';
                _html += '<a href="#">' + res.context.user + '</a>';
                _html += '<span>' + res.context.time + '</span>';
                _html += '</h5>';
                _html += '</div>';
                _html += '<ul class="review-rating">';
                for (let i = 1; i <= 5; i++) {
                    if (i <= rating) {
                        _html += '<li class="icofont-ui-rating"></li>';
                    } else {
                        _html += '<li class="icofont-ui-rate-blank"></li>';
                    }
                }
                _html += '</ul>';

                _html += '<p class="review-desc">' + res.context.review + '</p>';
                _html += '</li>';
                _html += '</ul>';
                $(".review-list").prepend(_html);
            }
        }
    });
});














// Cart functionality
$(document).ready(function () {
    // Event listener for add-to-cart button
    $(".add-to-cart-btn").on("click", function () {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let container = this_val.closest('.product-card');
    
        let quantity = parseInt(container.find(".product-quantity-" + index).val());
        let product_title = container.find(".product-title-" + index).val();
        let product_id = container.find(".product-id-" + index).val();
        let old_price = parseFloat(container.find(".old-product-price-" + index).text().replace("₹", '').replace(',', ''));
        let product_price = parseFloat(container.find(".current-product-price-" + index).text().replace('₹', '').replace(',', ''));
        let product_pid = container.find(".product-pid-" + index).val();
        let product_image = container.find(".product-image-" + index).val();
        let stock = parseInt(container.find(".product-stock-" + index).val());
    
        console.log("OLD PRICE", old_price);
        console.log("PRICE", product_price);
    
        console.log("Product quantity is: ", quantity);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'old_price': old_price,
                'stock': stock
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding product to cart...");
            },
            success: function (response) {
                if (response.error) {
                    // Product already in cart, show alert
                    alert(response.error);
                } else {
                    // Product added successfully
                    this_val.html("Item added to cart");
                    console.log("Added product to Cart");
                    $(".cart-items-count").text(response.totalcartitems);
                    // Update the cart total amount with the new total amount from the server
                    let newTotal = response.new_total_amount;
                    // Format the total with commas as thousand separators
                    let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                    $('#cart-total-amount').text('₹' + formattedTotal);
                }
            },
            error: function (jqXHR) {
                // If the server responded with a 400 error, show the alert
                if (jqXHR.status === 400) {
                    let response = JSON.parse(jqXHR.responseText);
                    alert(response.error);
                }
            }
        });
    });
    
    

    
    $(".add-to-cart-btn-v3").on("click", function () {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let container = this_val.closest('.details-add-group');
    
        let quantity = parseInt(container.find(".product-quantity-" + index).val());
        let product_title = container.find(".product-title-" + index).val();
        let product_id = container.find(".product-id-" + index).val();
        let old_price = parseFloat(container.find(".old-product-price-" + index).text().replace("₹", '').replace(',', ''));
        let product_price = parseFloat(container.find(".current-product-price-" + index).text().replace('₹', '').replace(',', ''));
        let product_pid = container.find(".product-pid-" + index).val();
        let product_image = container.find(".product-image-" + index).val();
        let stock = parseInt(container.find(".product-stock-" + index).val());
    
        console.log("OLD PRICE", old_price);
        console.log("PRICE", product_price);
    
        console.log("Product quantity is: ", quantity);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'old_price': old_price,
                'stock': stock
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding product to cart...");
            },
            success: function (response) {
                if (response.error) {
                    // Product already in cart, show alert
                    alert(response.error);
                } else {
                    // Product added successfully
                    this_val.html("Item added to cart");
                    console.log("Added product to Cart");
                    $(".cart-items-count").text(response.total);
                    // Update the cart total amount with the new total amount from the server
                    let newTotal = response.new_total_amount;
                    // Format the total with commas as thousand separators
                    let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                    $('#cart-total-amount').text('₹' + formattedTotal);
                }
            },
            error: function (jqXHR) {
                // If the server responded with a 400 error, show the alert
                if (jqXHR.status === 400) {
                    let response = JSON.parse(jqXHR.responseText);
                    alert(response.error);
                }
            }
        });
    });
    
    $(".add-to-cart-btn-v2").one("click", function () {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let container = this_val.closest('tr');
    
        let quantity = parseInt(container.find(".action-input").val());
        let product_title = container.find(".table-name h6").text();
        let product_id = container.find(".product-id-" + index).val();
        let old_price_str = container.find(".old-product-price-" + index).val(); // Retrieve old price from the hidden input
        let old_price = parseFloat(old_price_str.replace(',', '')); // Convert old price string to float and remove commas
        if (isNaN(old_price)) {
            // Handle the case where the old price is not a valid number
            console.log("Invalid old price:", old_price_str);
            old_price = 0.0; // Set a default value if old price is not a valid number
        }
        // Retrieve old price from the hidden input
        let product_price = parseFloat(container.find(".current-product-price-" + index).text().replace('₹', '').replace(',', ''));
        let product_pid = container.find(".product-pid-" + index).val();
        let product_image = container.find(".table-image img").attr("src");
        let stock = parseInt(container.find(".product-stock-" + index).val());
    
        console.log("OLD PRICE", old_price);
        console.log("PRICE", product_price);
    
        console.log("Product quantity is: ", quantity);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'old_price': old_price, // Pass the old price to the backend
                'stock': stock
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding product to cart...");
            },
            success: function (response) {
                if (response.error) {
                    // Product already in cart, show alert
                    alert(response.error);
                } else {
                    // Product added successfully
                    this_val.html("Item added to cart");
                    console.log("Added product to Cart");
                    $(".cart-items-count").text(response.totalcartitems);
                    // Update the cart total amount with the new total amount from the server
                    let newTotal = response.new_total_amount;
                    // Format the total with commas as thousand separators
                    let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                    $('#cart-total-amount').text('₹' + formattedTotal);
                }
            },
            error: function (jqXHR) {
                // If the server responded with a 400 error, show the alert
                if (jqXHR.status === 400) {
                    let response = JSON.parse(jqXHR.responseText);
                    alert(response.error);
                }
            }
        });
    });
    
    $(".add-to-cart-btn-v4").on("click", function () {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let container = this_val.closest('.feature-card');
    
        let quantity = parseInt(container.find(".product-quantity-" + index).val());
        let product_title = container.find(".product-title-" + index).val();
        let product_id = container.find(".product-id-" + index).val();
        let old_price = parseFloat(container.find(".old-product-price-" + index).text().replace("₹", '').replace(',', ''));
        let product_price = parseFloat(container.find(".current-product-price-" + index).text().replace('₹', '').replace(',', ''));
        let product_pid = container.find(".product-pid-" + index).val();
        let product_image = container.find(".product-image-" + index).val();
        let stock = parseInt(container.find(".product-stock-" + index).val());
    
        console.log("OLD PRICE", old_price);
        console.log("PRICE", product_price);
    
        console.log("Product quantity is: ", quantity);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'old_price': old_price,
                'stock': stock
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding product to cart...");
            },
            success: function (response) {
                if (response.error) {
                    // Product already in cart, show alert
                    alert(response.error);
                } else {
                    // Product added successfully
                    this_val.html("Item added to cart");
                    console.log("Added product to Cart");
                    $(".cart-items-count").text(response.totalcartitems);
                    // Update the cart total amount with the new total amount from the server
                    let newTotal = response.new_total_amount;
                    // Format the total with commas as thousand separators
                    let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                    $('#cart-total-amount').text('₹' + formattedTotal);
                }
            },
            error: function (jqXHR) {
                // If the server responded with a 400 error, show the alert
                if (jqXHR.status === 400) {
                    let response = JSON.parse(jqXHR.responseText);
                    alert(response.error);
                }
            }
        });
    });


    $(".add-to-cart-btn-v5").on("click", function () {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let container = this_val.closest('.product-view');
    
        let quantity = parseInt(container.find(".product-quantity-" + index).val());
        let product_title = container.find(".product-title-" + index).val();
        let product_id = container.find(".product-id-" + index).val();
        let old_price = parseFloat(container.find(".old-product-price-" + index).text().replace("₹", '').replace(',', ''));
        let product_price = parseFloat(container.find(".current-product-price-" + index).text().replace('₹', '').replace(',', ''));
        let product_pid = container.find(".product-pid-" + index).val();
        let product_image = container.find(".product-image-" + index).val();
        let stock = parseInt(container.find(".product-stock-" + index).val());
    
        console.log("OLD PRICE", old_price);
        console.log("PRICE", product_price);
    
        console.log("Product quantity is: ", quantity);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'old_price': old_price,
                'stock': stock
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding product to cart...");
            },
            success: function (response) {
                if (response.error) {
                    // Product already in cart, show alert
                    alert(response.error);
                } else {
                    // Product added successfully
                    this_val.html("Item added to cart");
                    console.log("Added product to Cart");
                    $(".cart-items-count").text(response.totalcartitems);
                    // Update the cart total amount with the new total amount from the server
                    let newTotal = response.new_total_amount;
                    // Format the total with commas as thousand separators
                    let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                    $('#cart-total-amount').text('₹' + formattedTotal);
                }
            },
            error: function (jqXHR) {
                // If the server responded with a 400 error, show the alert
                if (jqXHR.status === 400) {
                    let response = JSON.parse(jqXHR.responseText);
                    alert(response.error);
                }
            }
        });
    });

    $(".add-to-cart-btn-v6").on("click", function () {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let container = this_val.closest('.inner-section');
    
        let quantity = parseInt(container.find(".product-quantity-" + index).val());
        let product_title = container.find(".product-title-" + index).val();
        let product_id = container.find(".product-id-" + index).val();
        let old_price = parseFloat(container.find(".old-product-price-" + index).text().replace("₹", '').replace(',', ''));
        let product_price = parseFloat(container.find(".current-product-price-" + index).text().replace('₹', '').replace(',', ''));
        let product_pid = container.find(".product-pid-" + index).val();
        let product_image = container.find(".product-image-" + index).val();
        let stock = parseInt(container.find(".product-stock-" + index).val());
    
        console.log("OLD PRICE", old_price);
        console.log("PRICE", product_price);
    
        console.log("Product quantity is: ", quantity);
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'old_price': old_price,
                'stock': stock
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding product to cart...");
            },
            success: function (response) {
                if (response.error) {
                    // Product already in cart, show alert
                    alert(response.error);
                } else {
                    // Product added successfully
                    this_val.html("Item added to cart");
                    console.log("Added product to Cart");
                    $(".cart-items-count").text(response.totalcartitems);
                    // Update the cart total amount with the new total amount from the server
                    let newTotal = response.new_total_amount;
                    // Format the total with commas as thousand separators
                    let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                    $('#cart-total-amount').text('₹' + formattedTotal);
                }
            },
            error: function (jqXHR) {
                // If the server responded with a 400 error, show the alert
                if (jqXHR.status === 400) {
                    let response = JSON.parse(jqXHR.responseText);
                    alert(response.error);
                }
            }
        });
    });


    // Event listener for quantity change
    $(".quantity-update").on("change keydown keyup", function () {
        console.log("quantity changed.......");
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = parseInt(this_val.val())
        let product_id = $(".product-id-" + index).val()

        $.ajax({
            url: '/update-cart',
            data: {
                'id': product_id,
                'qty': quantity
            },
            dataType: 'json',
            success: function (response) {
                console.log("Updated product quantity");
                // Update the cart total amount with the new total amount from the server
                let newTotal = response.new_total_amount;
                // Format the total with commas as thousand separators
                let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                $('#cart-total-amount').text('₹' + formattedTotal);
                $('#cart-total-amount1').text('₹' + formattedTotal);
                // Update the total amount for the product
                let productTotal = response.updated_product_price;
                let formattedProductTotal = productTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                $('.product-total-' + index + ' h6').text('₹' + formattedProductTotal);
            }
        })
    })

    // Event listener for delete-product button
    $(".delete-product").on("click", function () {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);

        console.log("product id:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide();
            },
            success: function (response) {
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                // Remove the deleted product from the DOM
                this_val.closest('.remove-cart-item').remove();
                // Update the cart total amount with the new total amount from the server
                let newTotal = response.new_total_amount;
                // Format the total with commas as thousand separators
                let formattedTotal = newTotal.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); // Remove decimal places
                $('#cart-total-amount').text('₹' + formattedTotal);
                // Also update the total amount on the checkout button
                $('.checkout-price').text('₹' + formattedTotal);
            }
        });
    });
});





// Wishlist functinality
$(document).ready(function () {
    // Add to wishlist
    $(document).on("click", ".add-to-wishlist", function () {
        let product_id = $(this).attr("data-product-item");
        let this_val = $(this);
    
        console.log("Product ID is:", product_id);
    
        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function (response) {
                console.log("adding product to wishlist....");
            },
            success: function (response) {
                console.log("Added product to wishlist...");
                if (response.success) {
                    // Update the wishlist count in the DOM
                    $('#wishlist-count').text(response.updated_count);
                    $('#wishlist-count1').text(response.updated_count);
                    alert("Item added to Wishlist");
                } else {
                    alert("Product is already in the wishlist");
                }
            }
        });
    });
    

    // Remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function () {
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id is: ", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Deleting product from wishlist");

            },
            success: function (response) {
                console.log("Deleted product from wishlist");
                // Remove the product row from the DOM
                this_val.closest('tr').remove();
                // Update the wishlist count in the DOM
                $('#wishlist-count').text(response.updated_count);
                $('#wishlist-count1').text(response.updated_count);
            }
        })
    })
});


// JavaScript code in your template
function readMore() {
    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("readMoreBtn");

    if (dots.style.display === "none") {
        dots.style.display = "inline";
        btnText.innerHTML = "Read more";
        moreText.style.display = "none";
    } else {
        dots.style.display = "none";
        btnText.innerHTML = "Read less";
        moreText.style.display = "inline";
    }
}

//filter product functionality 
$(document).ready(function() {
    // Function to get search query from URL
    function getSearchQuery() {
        var urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('q');
    }

    // Event listener for category, brand, and price range inputs
    $('.filter-checkbox, .filter-brand-checkbox, .shop-widget-btn, .shop-widget-list input[type="checkbox"]').on('change click', function() {
        // Initialize arrays to store selected category, brand, and rating IDs
        var selectedCategories = [];
        var selectedBrands = [];
        var selectedRatings = [];
        var minPrice = $('#min_price').val();
        var maxPrice = $('#max_price').val();

        // Iterate over checked checkboxes and extract category, brand, and rating IDs
        $('.filter-checkbox:checked').each(function() {
            selectedCategories.push($(this).val());
        });
        $('.filter-brand-checkbox:checked').each(function() {
            selectedBrands.push($(this).val());
        });
        $('.rating-checkbox-list input[type="checkbox"]:checked').each(function() {
            selectedRatings.push($(this).val());
        });

        // Create an object to store all selected filters
        var filters = {
            'category': selectedCategories,
            'brand': selectedBrands,
            'rating': selectedRatings
        };

        // Add min and max price to filters if they are not empty
        if (minPrice && minPrice !== '') {
            filters['min_price'] = minPrice;
        }
        if (maxPrice && maxPrice !== '') {
            filters['max_price'] = maxPrice;
        }

        // Get the current URL parameters
        var urlParams = new URLSearchParams(window.location.search);

        // Update the URL parameters with the selected filters
        for (var key in filters) {
            urlParams.delete(key);  // Remove any existing values for this filter
            filters[key].forEach(function(value) {
                urlParams.append(key, value);  // Add the new filter values
            });
        }

        // Reload the page with the updated query parameters
        window.location.href = window.location.pathname + '?' + urlParams.toString();
    });

    $('.shop-widget-btn-v2').on('click', function() {
        // Uncheck all checkboxes
        $('input[type="checkbox"]').prop('checked', false);

        // Clear local storage
        localStorage.clear();

        // Reload the page without any query parameters
        window.location.href = window.location.pathname;
    });
});






function checkQuantity(input) {
    var maxQuantity = parseInt(input.getAttribute('max'));
    var enteredQuantity = parseInt(input.value);

    if (enteredQuantity > maxQuantity) {
        alert("You can only select a maximum of " + maxQuantity + " quantity for this product");
        input.value = maxQuantity; // Set the value back to the maximum allowed quantity
    }
}





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

//delete address from profile 
$('.trash1').click(function() {
    var addressId = $(this).data('id');
    var addressCard = $(this).closest('.profile-card');
    $.ajax({
        url: '/delete_address/',
        type: 'post',
        data: {'id': addressId},
        headers: {"X-CSRFToken": csrftoken},
        success: function(data) {
            if (data.success) {
                addressCard.remove(); // Remove the address card from the DOM
                alert('Address deleted successfully!');
            } else {
                alert('An error occurred!');
            }
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    function enforceNumericInput(e) {
        var charCode = (e.which) ? e.which : e.keyCode;
        if ((charCode < 48 || charCode > 57) && (charCode < 37 || charCode > 40) && charCode !== 8 && charCode !== 46) {
            e.preventDefault();
        }
        if (this.value.length >= 10 && charCode !== 8 && (charCode < 37 || charCode > 40) && charCode !== 46) {
            e.preventDefault();
        }
    }

    document.querySelector('input[name="phone"]').addEventListener('keydown', enforceNumericInput);
    document.querySelector('input[name="secondary_phone"]').addEventListener('keydown', enforceNumericInput);

    document.querySelector('input[name="Pincode"]').addEventListener('keydown', function (e) {
        var charCode = (e.which) ? e.which : e.keyCode;
        if ((charCode < 48 || charCode > 57) && (charCode < 37 || charCode > 40) && charCode !== 8 && charCode !== 46) {
            e.preventDefault();
        }
        if (this.value.length >= 6 && charCode !== 8 && (charCode < 37 || charCode > 40) && charCode !== 46) {
            e.preventDefault();
        }
    });
});


var quantityInput = document.getElementById('product-quantity-cart');

quantityInput.addEventListener('keydown', function(e) {
    console.log('Keydown event triggered');
    var isZeroKey = e.key === '0';
    var isZeroAfterNumber = this.value === '0' && !isNaN(parseInt(e.key));
    
    if ((isZeroKey && this.value === '') || e.key === '-' || isZeroAfterNumber) {
        e.preventDefault();
    }
});

quantityInput.addEventListener('input', function() {
    var isZeroValue = this.value === '0';
    
    if (isZeroValue) {
        this.value = ''; // Clear the value if '0' is entered
    }
});








  document.getElementById('submit-btn').addEventListener('click', function(event) {
    var form = document.getElementById('address-form');
    var inputs = form.querySelectorAll('input, select, textarea');
    var isValid = true;
    
    inputs.forEach(function(input) {
        if (!input.value && input.hasAttribute('required')) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        event.preventDefault();
        alert('Please fill in all required fields.');
    }
});


$(document).ready(function () {
    $(".minPrice, .maxPrice").on('input', function() {
        // Remove non-numeric characters
        $(this).val($(this).val().replace(/[^\d]/g, ''));

        // Get the values of min and max price
        let minPrice = parseInt($(".minPrice").val()) || 0;
        let maxPrice = parseInt($(".maxPrice").val()) || 0;

        // Ensure max price is always greater than min price
        if (maxPrice < minPrice) {
            $(".maxPrice").val(minPrice);
            maxPrice = minPrice;
        }
    });

    $(".minPrice, .maxPrice").on('keydown', function(event) {
        // Allow special keys like backspace, delete, arrow keys, etc.
        if (event.key.length === 1 && !/[0-9]/.test(event.key)) {
            // Prevent typing non-numeric characters
            event.preventDefault();
        }
    });

    $(".minPrice, .maxPrice").on('paste', function(event) {
        // Prevent pasting non-numeric characters
        let clipboardData = event.originalEvent.clipboardData || window.clipboardData;
        let pastedData = clipboardData.getData('text');
        if (!/^\d*$/.test(pastedData)) {
            event.preventDefault();
        }
    });

    $(".minPrice, .maxPrice").on('blur', function() {
        // Ensure minimum price is not negative
        let minPrice = parseInt($(".minPrice").val()) || 0;
        if (minPrice < 0) {
            $(".minPrice").val(0);
        }

        // Ensure maximum price is not negative and greater than minimum price
        let maxPrice = parseInt($(".maxPrice").val()) || 0;
        if (maxPrice < 0) {
            $(".maxPrice").val(0);
        }

        if (maxPrice < minPrice) {
            $(".maxPrice").val(minPrice);
        }
    });
});




  
  
  
  
  






















