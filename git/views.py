from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from blog.form import signupform
from .models import CarouselItem, Catagory, Cart, Products, Favourite
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Order, OrderItem
from django.conf import settings
from decimal import Decimal
import json
import logging
from .models import Poster
from .models import CartItem

logger = logging.getLogger(__name__)




data = {
    "chatinit": {
        "title": ["Greetings from", "How can I help you today?"],
        "options": ['Discover Products', 'Other Queries']
    },
    "discover products": {
        "title": ["ORGANIC"],
        "options": ["Organic", "Benefits", "Categories"]
    },
    "organic": {
        "title": ["What is Organic:"],
        "options": ["Organic refers to farming practices that avoid synthetic fertilizers, pesticides, genetically modified organisms, and artificial additives."]
    },
    "benefits": {
        "title": ["ORGANIC BENEFITS:","Organic farmers and food producers grow and produce food without using synthetic chemicals such as pesticides and artificial fertilisers."],
        "options": ["Veterinary-Benefits", "Health Care-Benefits", "Personal Care-Benefits", "Agriculture-Benefits", "Grocery-Benefits"]
    },
    "categories": {
        "title": ["Five Categories"],
        "options": ["Veterinary", "Health Care", "Personal Care", "Agriculture", "Grocery"]
    },
    "veterinary-benefits": {
        "title": ["VETERINARY-BENEFITS","Vaccines against distemper, rabies, feline leukemia virus, and parvovirus","Treatments for cancer","New techniques for traumas and surgery","Antibiotics to treat infections","Prevention and treatment for dog heartworm","Breeding programs for endangered species"],
        "options": ["Go Back"]
    },
    "health care-benefits": {
        "title": ["HEALTH CARE-BENEFITS","Convers daycare procedures", "Convers domiciliary treatments","Convers alternative treatment","Offers add-on cover for critical illnesses"],
        "options": ["Go Back"]
    },
    "personal care-benefits": {
        "title": ["PERSONAL CARE-BENEFITS","Round-the-Clock Professional Staff","Maximum Independence","Clean and Comfortable Living Space","An Engaging Social Life","Gourmet, Restaurant-Style Dining","Discover More Tips on Finding a Safe and Comfortable Senior Living Community  "],
        "options": ["Go Back"]
    },
    "agriculture-benefits": {
        "title": ["AGRICULTURE-BENEFITS","Sustainability", "Water depletion", "Carbon sequestration", "Agricultural productivity", "Healthier soils", "Biodiversity conservation"],
        "options": ["Go Back"]
    },
    "grocery-benefits": {
        "title": ["GROCERY-BENEFITS","Ingesting fewer chemicals", "No antibiotics or synthetic hormones", "Nutrition", "Better taste"],
        "options": ["Go Back"]
    },
    "veterinary": {
        "title": ["VETERINARY","Organic animal products are produced in an environment that follows specific guidelines to ensure the health and welfare of animals, and to conserve natural resources"],
        "options": ["veterinary-brand"]
    },
    "veterinary-brand": {
        "title": ["veterinary-brand"],
        "options": ["Paw Mark"]
    },
    "health care": {
        "title": ["HEALTH CARE","Organic health care products are made with ingredients from organic farming or natural resources, and are intended to be safe for the skin and body."],
        "options": ["health care-brand"]
    },
    "health care-brand": {
        "title": ["health care-brand"],
        "options": ["Uniaktiv", "Nutrimark"]
    },
    "personal care": {
        "title": ["PERSONAL CARE","Organic personal care products are made from natural ingredients and are free of synthetic chemicals and additives."],
        "options": ["health care-brand"]
    },
    "personal care-brand": {
        "title": ["personal care-brand"],
        "options": ["Myristika", "Ocean Fresh"]
    },
    "agriculture": {
        "title": ["AGRICULTURE","Organic agriculture is a farming method that produces food and animal products without using synthetic chemicals, genetically modified organisms (GMOs), or irradiation."],
        "options": ["health care-brand"]
    },
    "agriculture-brand": {
        "title": ["agriculture-brand"],
        "options": ["Uni Mark"]
    },
    "grocery": {
        "title": ["GROCERY","Organic food is produced using farming methods that avoid the use of synthetic chemicals, such as pesticides and fertilizers, and genetically modified organisms (GMOs)."],
        "options": ["health care-brand"]
    },
    "grocery-brand": {
        "title": ["grocery-brand"],
        "options": ["UNYK"]
    },
    "other queries": {
        "title": ["What can I help you with?"],
        "options": ["Contact Us", "Go Back"]
    },
    "contact us": {
        "title": ["Phone: 9999999999",
            "E-mail: xxx@gmail.com",
            "Website: http://unilink.com"],
        "options": [
            "Main Menu"
        ]
    },
}

def profile(request):
    # Fetch categories with status=0
    category = Catagory.objects.filter(status=0)

    if request.method == 'POST':
        # Get the submitted form data
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Update the user's information
        request.user.username = username
        request.user.email = email
        request.user.save()

        messages.success(request, 'Your profile has been updated!')

        # Redirect back to the profile page to display the updated data
        return redirect('blog:profile')

    return render(request, 'blog/profile.html', {'category': category})
def offer_view(request):
    posters = Poster.objects.all()
    category = Catagory.objects.filter(status=0)  # Fetch categories with status=0
    
    # Add both 'posters' and 'category' to the context
    return render(request, 'blog/offers.html', {'posters': posters, 'category': category})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart_count = sum(item['quantity'] for item in cart)

    return JsonResponse({'cart_count': cart_count})

def home(request):
    carousel_items = CarouselItem.objects.all()
    category = Catagory.objects.filter(status=0)
    return render(request, 'blog/index.html', {'category': category, 'carousel_items': carousel_items})

def cart_page(request):
    category = Catagory.objects.filter(status=0)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "blog/cart.html", {'cart': cart , 'category': category})
    else:
        return redirect(reverse('blog:signup'))

def delet_cart(request, cid):
    cartitem = get_object_or_404(Cart, id=cid)
    cartitem.delete()
    return redirect(reverse('blog:cart'))

def add_to_cart(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data.get('product_qty')
            product_id = data.get('pid')

            product_status = get_object_or_404(Products, id=product_id)

            # Check if the product is already in the cart
            cart_item = Cart.objects.filter(user=request.user.id, product_id=product_id).first()

            if cart_item:
                # If the product is already in the cart, update the quantity
                new_qty = cart_item.product_qty + product_qty

                if product_status.quantity >= new_qty:
                    cart_item.product_qty = new_qty
                    cart_item.save()
                    return JsonResponse({'status': 'Product Quantity Updated in Cart'}, status=200)
                else:
                    return JsonResponse({'status': 'sorry, this product is currently out of stock. It will be available again soon.'}, status=200)
            else:
                # If the product is not in the cart, create a new cart item
                if product_status.quantity >= product_qty:
                    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Currently Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add to Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

def fav_page(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data.get('pid')

            product_status = get_object_or_404(Products, id=product_id)

            if Favourite.objects.filter(user=request.user.id, product_id=product_id).exists():
                return JsonResponse({'status': 'Your Item Already in Wishlist'}, status=200)
            else:
                Favourite.objects.create(user=request.user, product_id=product_id)
                return JsonResponse({'status': 'Your Item Added to Favourite'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add to Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

def favview(request):
    category = Catagory.objects.filter(status=0)
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "blog/fav.html", {'fav': fav ,'category': category })
    else:
        return redirect(reverse('blog:signup'))

def delet_fav(request, fid):
    favitem = get_object_or_404(Favourite, id=fid)
    favitem.delete()
    return redirect(reverse('blog:favview'))

def about(request):
    category = Catagory.objects.filter(status=0)
    return render(request, "blog/about.html", {'category': category})

def contact(request):
    category = Catagory.objects.filter(status=0)
    return render(request, "blog/contact.html",  {'category': category})


def chatbot_page(request):
    category = Catagory.objects.filter(status=0)
    return render(request, "blog/chatbot.html", {'category': category})

def logout_page(request):

    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout Successfully')
    return redirect(reverse('blog:login'),)

def login_page(request):
    category = Catagory.objects.filter(status=0)  

    if request.user.is_authenticated:
        return redirect(reverse('blog:home'))
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(request, username=name, password=passwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successfully')
                return redirect(reverse('blog:home'))
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect(reverse('blog:login'))
        return render(request, 'blog/login.html',{'category': category})


def category(request):
    category = Catagory.objects.filter(status=0)
    return render(request, 'blog/category.html', {'category': category})

def view_category(request,name):
    if Catagory.objects.filter(name=name,status=0):
        category=Catagory.objects.get(name=name,status=0)
        products=Products.objects.filter(catagory__name=name)
        category = Catagory.objects.filter(status=0)
        return render(request,'blog/view_category.html',{'products':products,'category_name':name, 'category': category})
    else:
        messages.warning(request,"No Such Category Found")
        return redirect(reverse('blog:category'))
    

def product_detail(request, cname, pname):
    category = get_object_or_404(Catagory, name=cname, status=0)
    product = get_object_or_404(Products, name=pname, status=0)
    category = Catagory.objects.filter(status=0)
    return render(request, "blog/product_detail.html", {'category': category,'product': product})

def search_results(request):
    query = request.GET.get('query', '')
    if query:
        products = Products.objects.filter(name__icontains=query, status=0)
        category = Catagory.objects.filter(status=0)

        if products.exists():
            pname = products.first().name 
            product = get_object_or_404(Products, name=pname, status=0)

            return render(request, 'blog/search.html', {'category': category, 'products': products, 'query': query, 'product': product})
        else:
            messages.error(request, "No products match your search.")
            return render(request, 'blog/search.html', {'category': category, 'products': None, 'query': query})
    else:
        messages.error(request, "No search term provided.")
        return render(request, 'blog/search.html', {'category': category, 'products': None})
        

def checkout_view(request):
    # Assuming you have a way to get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)  # Adjust as necessary
    total = sum(item.product.price * item.product_qty for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'order.html', context)

def chatbot_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('input', '').strip().lower()
        response = {}

        if user_input in data:
            response['title'] = data[user_input]['title']
            response['options'] = data[user_input]['options']
           
        elif user_input == 'other queries':
            response['title'] = data['other queries']['title']
            response['options'] = data['other queries']['options']
          
        elif user_input in ['veterinary-benefits', 'veterinary-benefits']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
          
        elif user_input in ['veterinary-brand', 'veterinary-brand']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
        
        elif user_input in ['health care-brand', 'health care-brand']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
          
        elif user_input in ['personal care-brand', 'personal care-brand']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
      
        elif user_input in ['agriculture-brand', 'agriculture-brand']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
         
        elif user_input in ['grocery-brand', 'grocery-brand']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
           
        elif user_input in ['go back', 'main menu']:
            response['title'] = data['chatinit']['title']
            response['options'] = data['chatinit']['options']
 
        else:
            response['title'] = ["Sorry, I don't understand that."]
            response['options'] = []
          

        return JsonResponse(response)

    return JsonResponse({"error": "Invalid request method."}, status=400)
    


def delete_cart_item(request, item_id):
    # Logic to remove the item from the cart
    # Example:
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    # Get the updated cart count
    cart_count = Cart.objects.filter(user=request.user).count()  # Update this according to your model

    return JsonResponse({'cart_count': cart_count})




def signup(request):
    form =signupform()  # Ensure 'SignupForm' is capitalized correctly
    categories = Catagory.objects.filter(status=0)  # Fix typo in 'Category'
    success = False
    error_message = None

    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save()  # Save user instance
            username = form.cleaned_data.get('username')
            number = request.POST.get('number')
            email = form.cleaned_data.get('email')

            full_message = f"Name: {username}\nEmail: {email}\nPhone Number: {number}"

            try:
                # Send registration notification email
                send_mail(
                    'New User Registration',
                    full_message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False
                )

                # Send confirmation email to the user
                confirmation_message = f"Thank you {username}, your registration was successful! Happy shopping at rushibioorganic.com. For any queries, contact our free chatbot or call us at 9361868205."
                send_mail(
                    'Registration Successful',
                    confirmation_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )

                success = True
                messages.success(request, "Signup successful! Check your email for confirmation.")
                return redirect('blog:login')
            except Exception as e:
                error_message = "An error occurred while sending the confirmation email. Please try again."
                logger.error(f"Error sending email: {e}")  # Log the error for debugging
        else:
            error_message = "There were errors in your form submission. Please correct them and try again."

    return render(request, 'blog/signup.html', {
        'form': form,
        'categories': categories,
        'success': success,
        'error_message': error_message
    })

def address_view(request):
    category = Catagory.objects.filter(status=0)
    return render(request, "blog/address.html", {'category': category})

def checkout_page(request):
    if request.user.is_authenticated:
        # Fetch cart items for the authenticated user
        cart_items = Cart.objects.filter(user=request.user)

        # Check if the cart is empty
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect(reverse('blog:cart'))

        # Fetch categories (ensure that the 'Category' model is correctly referenced)
        category = Catagory.objects.filter(status=0)

        # Calculate total cost of the cart items
        total_cost = sum(item.product.price * item.product_qty for item in cart_items)

        if request.method == 'POST':
            # Capture the total sent from the cart page if the request method is POST
            total_cost = request.POST.get('total')
            total_cost = Decimal(total_cost) if total_cost else Decimal(0.0)
            
            # Process checkout form (e.g., payment gateway logic)
            # Example: Add payment logic here. If the order is successfully placed:
            
            messages.success(request, "Your order has been placed successfully!")
            
            # Clear the cart after the order is placed
            cart_items.delete()
            
            # Redirect to the home page (or wherever you want)
            return redirect(reverse('blog:home'))

        # Render the checkout page for GET request (passing cart items, total cost, and categories)
        return render(request, 'blog/checkout.html', {
            'cart_items': cart_items,
            'total': total_cost,
            'category': category  # Pass categories to the template
        })
    
    else:
        # Redirect to login if the user is not authenticated
        return redirect(reverse('blog:login'))
    
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        new_quantity = data.get('new_quantity')

        if request.user.is_authenticated:
            cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
            cart_item.product_qty = new_quantity
            cart_item.save()

            # Calculate the total cost for this item
            total_cost = cart_item.product.price * cart_item.product_qty

            return JsonResponse({'status': 'Quantity updated successfully', 'total_cost': total_cost})
        else:
            return JsonResponse({'status': 'User not authenticated'}, status=403)

    return JsonResponse({'status': 'Invalid request method'}, status=400)



from django.shortcuts import render, redirect
from .models import Order  # Ensure you import your Order model

def order_view(request):
    if request.method == "POST":
        # Process the order
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        postcode = request.POST['postcode']
        phone = request.POST['phone']
        email = request.POST['email']
        notes = request.POST['notes']
        total_amount = request.POST['total_amount']

        # Save the order or perform further processing
        # Order.objects.create(...)  # Example of creating an Order

        # Pass data to the confirmation template
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'city': city,
            'state': state,
            'postcode': postcode,
            'phone': phone,
            'email': email,
            'notes':notes,
            'cart_items': request.session.get('cart_items', []),  # Assuming cart items are stored in session
            'total': total_amount,
        }
        return render(request, 'blog/order.html', context)
    
    return redirect('blog:checkout')  # Redirect if not a POST request


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()  
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'blog/order.html', context)

def delete_order_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id)
        order = item.order  # Assuming you have a reverse relation from OrderItem to Order
        
        # Optionally check if the order can be modified
        if order.can_be_modified:  # Replace this with your actual logic
            item.delete()
            
            # Recalculate the order total after deletion
            order.total_amount = sum(item.price * item.quantity for item in order.orderitem_set.all())
            order.save()
            
            # Success message
            messages.success(request, 'Item removed from your order successfully.')
        else:
            # Error message if the order cannot be modified
            messages.error(request, 'This order cannot be modified at this time.')

        # Redirect back to the order confirmation page with the order ID
        return redirect('blog:order_confirmation', order_id=order.id)

@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart_item = Cart.objects.get(id=product_id)

        # Update the quantity
        cart_item.product_qty = quantity
        cart_item.save()

        # Optionally return updated totals
        total_cost = cart_item.product.price * cart_item.product_qty
        return JsonResponse({'total_cost': total_cost})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def about_view(request):
    posters = Poster.objects.all()[:4]  # Get the first 4 posters
    return render(request, 'blog:about.html', {'posters': posters})

def about(request):
    # Fetch the categories and posters from the database
    categories = Catagory.objects.all()
    posters = Poster.objects.all()

    context = {
        'category': categories,
        'posters': posters,
    }

    return render(request, 'blog/about.html', context)

def cash_page_view(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        address = request.POST.get('address')


        context = {
            'product_name': product_name,
            'price': price,
            'address': address,
        }
        return render(request, 'blog/order_confirmation.html', context)  

def cash_view(request):
    return render(request, 'blog/cash.html')

def order_confirmation_view(request, order_id):
    # Retrieve the order based on the order_id
    order = Order.objects.get(id=order_id)
    
    # Get cart items associated with the order (assuming you have a related model)
    cart_items = OrderItem.objects.filter(order=order)
    
    # Calculate the total amount from order items
    total_amount = sum(item.price * item.quantity for item in cart_items)

    context = {
        'order': order,
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'blog/order_confirmation.html', context)

def refund_view(request):
    return render(request, 'blog/refund.html')

def terms_view(request):
    return render(request, 'blog/terms.html')
 
def privacy_view(request):
    return render(request, 'blog/privacy.html')

def shipping_view(request):
    return render(request, 'blog/shipping.html')


import random
import string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# Store OTPs temporarily
otp_store = {}

def generate_otp():
    return "".join(random.choices(string.digits, k=6))  # 6-digit OTP


def get_otp_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = generate_otp()
        
        # Store OTP temporarily (use session or database for production)
        otp_store[email] = otp
        
        # Save email in session for future OTP verification
        request.session['email'] = email
        
        # Send OTP via email
        send_mail(
            "Your OTP",
            f"Your OTP is: {otp}",
            "your_email@gmail.com",  # Replace with your email
            [email],
            fail_silently=False,
        )
        messages.success(request, "OTP sent to your email.")
        return redirect("blog:verify_otp")  # Redirect to OTP verification page
    
    return render(request, "blog/get_otp.html")

from django.shortcuts import render, redirect
from django.contrib import messages

def verify_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        
        # Check if the entered OTP is 6 digits
        if len(entered_otp) != 6:
            messages.error(request, "OTP must be exactly 6 digits.")
            return redirect("blog:verify_otp")  # Reload the page to allow re-entry of OTP
        
        # Get the email stored in session
        email = request.session.get('email')
        
        if email:
            # Retrieve the stored OTP
            stored_otp = otp_store.get(email)
            
            if stored_otp and entered_otp == stored_otp:
                # OTP is correct
                messages.success(request, "OTP verified successfully. You can now reset your password.")
                return redirect("blog:reset_password")  # Redirect to password reset page
            else:
                # OTP is incorrect
                messages.error(request, "Incorrect OTP. Please try again.")
                return redirect("blog:verify_otp")  # Reload the page to allow re-entry of OTP
        else:
            # No email found in session (this shouldn't happen unless the user skips the get_otp page)
            messages.error(request, "Session expired. Please request a new OTP.")
            return redirect("blog:get_otp")  # Redirect back to the OTP request page
    
    return render(request, "blog/verify_otp.html")




from django.shortcuts import render, redirect
from django.contrib import messages

def reset_password_view(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        # Accept any matching passwords
        if new_password and confirm_password and new_password == confirm_password:
            messages.success(request, "Password reset successful.")
            return redirect("blog:login")
        else:
            messages.error(request, "Passwords do not match or are empty.")
            return redirect("blog:login")
    
    return render(request, "blog/reset_password.html")



# payment


from django.shortcuts import render, redirect
from django.http import HttpResponse
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.env import Env
import uuid

# Configuration settings

MERCHANT_ID = "M22BPS5QQ5EXL"
SALT_KEY = "09b3a60d-907c-40b8-af13-514bae4bb7d4"
SALT_INDEX = 1
ENV = Env.PROD  # Use production environment
UI_REDIRECT_URL = "http://127.0.0.1:8000/cart/"
S2S_CALLBACK_URL = "http://127.0.0.1:8000/payment/callback/"
MERCHANT_USER_ID = "USER123"  # Unique user ID

# Initialize PhonePe Client
phonepe_client = PhonePePaymentClient(
    merchant_id=MERCHANT_ID,
    salt_key=SALT_KEY,
    salt_index=SALT_INDEX,
    env=ENV
)

def payment_view(request):
    if request.method == "GET" and "amount" in request.GET:
        try:
            amount = int(request.GET["amount"]) * 100  # Convert to paise
            unique_transaction_id = str(uuid.uuid4())[:32]  # Generate unique transaction ID
            pay_page_request = PgPayRequest.pay_page_pay_request_builder(
                merchant_transaction_id=unique_transaction_id,
                amount=amount,
                merchant_user_id=MERCHANT_USER_ID,
                callback_url=S2S_CALLBACK_URL,
                redirect_url=UI_REDIRECT_URL
            )

            # Send payment request
            pay_page_response = phonepe_client.pay(pay_page_request)

            # Extract payment page URL
            pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
            return redirect(pay_page_url)

        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, "blog/cart.html")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

def payment_callback(request):
    if request.method == "GET":
        payment_status = request.GET.get("status")

        if payment_status == "success":
            # Redirect to the cart view, where the cart will be empty
            return redirect(reverse('cart_view') + "?message=Your cart is now empty.")
        else:
            # Handle failure or any other status
            return HttpResponse("Payment failed. Please try again.", status=400)

    return HttpResponse("Invalid callback", status=400)




# def cart_view(request):
#     total_amount = request.GET.get('total_amount', 0)  # Default to 0 if no total_amount is passed
#     return render(request, "blog/cart.html", {"total_amount": total_amount})


