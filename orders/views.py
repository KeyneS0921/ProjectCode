from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Table, MenuCategory, Order, OrderItem, Restaurant
import qrcode
import io

# Login Page
def home(request):
    return render(request, "Index.html", {"hide_navbar": True, "hide_footer": True})

# Merchant Login
def merchant_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if user has a restaurant
                try:
                    restaurant = user.restaurant
                    login(request, user)
                    return redirect('merchant-dashboard')
                except Restaurant.DoesNotExist:
                    error_message = "This account is not associated with any restaurant."
            else:
                error_message = "Invalid username or password."
        else:
            error_message = "Please enter both username and password."

    return render(request, 'merchant_login.html', {'error_message': error_message})

# Merchant Logout
def merchant_logout(request):
    logout(request)
    return redirect('home')

# Merchant dashboard
@login_required(login_url='merchant-login')
def merchant_dashboard(request):
    if request.method == 'POST':
        try:
            table_count = int(request.POST.get('table_count', 0))
            if table_count > 0:
                restaurant = request.user.restaurant
                current_tables = restaurant.table_set.count()

                if table_count > current_tables:
                    for i in range(current_tables + 1, table_count + 1):
                        Table.objects.create(restaurant=restaurant, table_number=i)
                elif table_count < current_tables:
                    restaurant.table_set.filter(table_number__gt=table_count).delete()

                restaurant.num_tables = table_count
                restaurant.save()
                return redirect('merchant-dashboard')

        except (ValueError, ObjectDoesNotExist):
            pass

    orders = Order.objects.filter(status='PENDING').order_by('-created_at')
    restaurant = request.user.restaurant
    categories = MenuCategory.objects.filter(restaurant=restaurant)

    return render(request, 'merchant_dashboard.html', {
        'orders': orders,
        'categories': categories,
        'restaurant': restaurant,
        'user': request.user
    })

# Menu_Customer
def table_menu(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    restaurant = table.restaurant
    categories = MenuCategory.objects.filter(restaurant=restaurant)

    cart_key = f'cart_{table_id}'
    session_cart = request.session.get(cart_key, {})
    cart_quantities = {}
    for item_id_str, qty in session_cart.items():
        cart_quantities[int(item_id_str)] = qty

    return render(request, 'menu_customer.html', {
        'table': table,
        'restaurant': restaurant,
        'categories': categories,
        'cart': cart_quantities
    })

# Add Items
def place_order(request, table_id, item_id):
    get_object_or_404(Table, pk=table_id)
    get_object_or_404(MenuItem, pk=item_id)

    cart_key = f'cart_{table_id}'
    cart = request.session.get(cart_key, {})

    item_id_str = str(item_id)
    cart[item_id_str] = cart.get(item_id_str, 0) + 1

    request.session[cart_key] = cart
    return redirect('table-menu', table_id=table_id)

# Decrease item
def decrease_item(request, table_id, item_id):
    get_object_or_404(Table, pk=table_id)
    get_object_or_404(MenuItem, pk=item_id)

    cart_key = f'cart_{table_id}'
    cart = request.session.get(cart_key, {})
    item_id_str = str(item_id)

    if item_id_str in cart:
        if cart[item_id_str] > 1:
            cart[item_id_str] -= 1
        else:
            del cart[item_id_str]
        request.session[cart_key] = cart

    return redirect('table-menu', table_id=table_id)

# Cart page
def view_cart(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    request.session['last_table_id'] = table_id
    cart_key = f'cart_{table_id}'
    cart = request.session.get(cart_key, {})

    if not cart:
        return render(request, 'cart.html', {
            'table': table,
            'items': [],
            'total_price': 0
        })

    existing_order = Order.objects.filter(table=table, status='PENDING').first()
    if not existing_order:
        order = Order.objects.create(table=table)
        for item_id_str, quantity in cart.items():
            item = get_object_or_404(MenuItem, pk=int(item_id_str))
            OrderItem.objects.create(order=order, item=item, quantity=quantity)
        del request.session[cart_key]
    else:
        order = existing_order

    items = order.items.all()
    total_price = sum(item.item.price * item.quantity for item in items)

    return render(request, 'cart.html', {
        'table': table,
        'items': items,
        'total_price': total_price
    })

# Order_detail(Merchant)
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items = order.items.all()
    total_price = sum(item.item.price * item.quantity for item in items)
    return render(request, 'order_detail.html', {
        'order': order,
        'items': items,
        'total_price': total_price
    })

# Order completed
def complete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'COMPLETED'
    order.save()
    return redirect('merchant-dashboard')

# Order Success
def order_success(request):
    table_id = request.session.get('last_table_id')
    return render(request, 'order_success.html', {'table_id': table_id})

# QR Code
def generate_qr_code(request, table_id):
    url = request.build_absolute_uri(reverse('table-menu', args=[table_id]))
    qr = qrcode.make(url)

    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)

    return FileResponse(buffer, content_type='image/png')

def feedback(request):
    return render(request, 'feedback.html')

# Add menu category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()
        if category_name:
            restaurant = request.user.restaurant
            MenuCategory.objects.create(restaurant=restaurant, name=category_name)
    return redirect('merchant-dashboard')

# Add menu item
def add_menu_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name', '').strip()
        item_price = request.POST.get('item_price', '')
        item_description = request.POST.get('item_description', '').strip()
        category_id = request.POST.get('category_id', '')

        if item_name and item_price and category_id:
            try:
                price = float(item_price)
                category = MenuCategory.objects.get(id=int(category_id), restaurant=request.user.restaurant)
                MenuItem.objects.create(
                    category=category,
                    name=item_name,
                    description=item_description,
                    price=price,
                    available=True
                )
            except (ValueError, MenuCategory.DoesNotExist):
                pass
    return redirect('merchant-dashboard')