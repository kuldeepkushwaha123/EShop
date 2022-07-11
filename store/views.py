from django.shortcuts import render, redirect
from .models import Product, Category
from .models import Customer
from django.contrib import messages
from store.models.orders import Order
from django.views import View


# Create your views here.


# This is a index page
def index(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    product = None
    categories = Category.get_all_category()
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.get_all_products_by_categoryid(categoryID)
    else:
        product = Product.get_all_products()

    data = {}
    data['products'] = product
    data['categories'] = categories
    print('you are : ', request.session.get('email'))

    ''' take the product id in front end '''
    if request.method == "POST":
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print('cart :', request.session['cart'])

        return redirect('/')

    return render(request, 'index.html', data)


# signup code view
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validation every fields
        if not first_name:
            messages.error(request, 'First Name Required !!')
        elif len(first_name) < 2:
            messages.error(request, 'First Name Must be 4 Char long or More.!!')
        elif not last_name:
            messages.error(request, 'Last Name Required !!')
        elif len(last_name) < 4:
            messages.error(request, 'Last Name Must be 4 Char long or More..!!')
        elif not phone:
            messages.error(request, 'Phone Number Required!!')
        elif len(phone) < 10:
            messages.error(request, 'Phone Number Must be 10 Char Long')
        elif len(phone) > 10:
            messages.error(request, 'Phone Number Must Be 10 Digit !! ')
        elif len(password) < 6:
            messages.error(request, 'Password Must Be 6 Char long !!')
        elif len(email) < 5:
            messages.error(request, 'Email Must Be 5 Char long !!')


        # data save
        else:
            data = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            data.save()
            messages.error(request, 'signup successfully..')

    return render(request, 'signup.html')


# login code view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Customer.get_customer_by_email(email)
        if user:
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            return redirect('/')
        else:
            messages.error(request, 'Email or Password invalid !!')
    return render(request, 'login.html')


# Cart Manage

def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_Products_by_id(ids)
    print(products)
    return render(request, 'cart.html', {'products': products})


# Check Out
class CheckOut(View):
    def post(self , request):
        address = request.POST.get['address']
        phone = request.POST.get['phone']
        customer = request.session.get['customer']
        cart = request.session.get['cart']

        products = Product.get_Products_by_id(list(cart.keys()))
        for product in products:
            order = Order(customer=Customer(id=customer),product=product,price=products.price,address=address,
                          phone=phone,quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')


# logout code

def logout(request):
    request.session.clear()
    return redirect('login')
