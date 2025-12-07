from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import Account, UserProfile

from category.models import Category
from store.models import Product, Variation, ProductGallery
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct



def admin_login(request):
    # If already logged in as superadmin → go to dashboard
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect('admin_login')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_superadmin:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin email or password")
            return redirect('admin_login')

    return render(request, 'adminpanel/admin_login.html')

def admin_dashboard(request):
    admin_user = request.user 
    total_users = Account.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()

    # Get recent users from Account model
    recent_users = Account.objects.order_by('-date_joined')[:5]

    return render(request, "adminpanel/dashboard.html", {
        'admin_user': admin_user,
        "total_users": total_users,
        "total_orders": total_orders,
        "total_products": total_products,
        "recent_users": recent_users,
    })


def view_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    profile = UserProfile.objects.filter(user=user).first()  # safe fetch

    return render(request, "adminpanel/view_user.html", {
        "user": user,
        "profile": profile,
    })



def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def users_list(request):
    # Only allow superadmins
    if not request.user.is_authenticated or not request.user.is_superadmin:
        messages.error(request, "Access denied.")
        return redirect('admin_login')

    users = Account.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/users_list.html', {'users': users})


def admin_users(request):
    query = request.GET.get('q')

    if query:
        users = Account.objects.filter(
            email__icontains=query
        ) | Account.objects.filter(
            username__icontains=query
        ) | Account.objects.filter(
            first_name__icontains=query
        )
    else:
        users = Account.objects.all()

    return render(request, 'adminpanel/admin_users.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    user.delete()
    return redirect('admin_users')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'adminpanel/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == "POST":
        name = request.POST['category_name']
        slug = request.POST['slug']
        description = request.POST['description']
        image = request.FILES.get('cat_image')

        Category.objects.create(
            category_name=name,
            slug=slug,
            description=description,
            cat_image=image
        )
        messages.success(request, "Category added successfully.")
        return redirect('category_list')

    return render(request, 'adminpanel/add_category.html')

def edit_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)

    if request.method == "POST":
        category.category_name = request.POST['category_name']
        category.slug = request.POST['slug']
        category.description = request.POST['description']

        if 'cat_image' in request.FILES:
            category.cat_image = request.FILES['cat_image']

        category.save()
        messages.success(request, "Category updated successfully.")
        return redirect('category_list')

    return render(request, 'adminpanel/edit_category.html', {'category': category})


def delete_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    category.delete()
    messages.success(request, "Category deleted.")
    return redirect('category_list')





# ---------------- PRODUCT LIST ----------------
def product_list(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()

    return render(request, "adminpanel/product_list.html", {
        "products": products,
    })


# ---------------- ADD PRODUCT ----------------
def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        product_name = request.POST["product_name"]
        slug = request.POST["slug"]
        description = request.POST["description"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        category_id = request.POST["category"]
        image = request.FILES.get("image")

        Product.objects.create(
            product_name=product_name,
            slug=slug,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            image=image,
        )

        messages.success(request, "Product added successfully!")
        return redirect("product_list")

    return render(request, "adminpanel/add_product.html", {"categories": categories})


# ---------------- EDIT PRODUCT ----------------
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.product_name = request.POST["product_name"]
        product.slug = request.POST["slug"]
        product.description = request.POST["description"]
        product.price = request.POST["price"]
        product.stock = request.POST["stock"]
        product.category_id = request.POST["category"]

        if request.FILES.get("image"):
            product.image = request.FILES["image"]

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("product_list")

    return render(request, "adminpanel/edit_product.html", {
        "product": product,
        "categories": categories,
    })


# ---------------- DELETE PRODUCT ----------------
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("product_list")


# ---------------- VARIATION LIST ----------------
def variation_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variations = Variation.objects.filter(product_id=product_id)

    return render(request, "adminpanel/variation_list.html", {
        "product": product,
        "variations": variations,
    })


# ---------------- ADD VARIATION ----------------
def add_variation(request, product_id):
    if request.method == "POST":
        variation_category = request.POST["variation_category"]
        variation_value = request.POST["variation_value"]

        Variation.objects.create(
            product_id=product_id,
            variation_category=variation_category,
            variation_value=variation_value,
        )

        messages.success(request, "Variation added!")
        return redirect("variation_list", product_id=product_id)

    return render(request, "adminpanel/add_variations.html", {"product_id": product_id})


# ---------------- DELETE VARIATION ----------------
def delete_variation(request, variation_id):
    variation = get_object_or_404(Variation, id=variation_id)
    pid = variation.product.id
    variation.delete()
    messages.success(request, "Variation deleted!")
    return redirect("variation_list", product_id=pid)

# ---------------- GALLERY LIST ----------------
def gallery_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    gallery = ProductGallery.objects.filter(product=product)

    return render(request, "adminpanel/product_gallery.html", {
        "product": product,
        "gallery": gallery,
    })


# ---------------- ADD GALLERY IMAGE ----------------
def add_gallery(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        image = request.FILES.get("image")
        if image:
            ProductGallery.objects.create(product=product, image=image)
            messages.success(request, "Image uploaded successfully!")
            return redirect('gallery_list', product_id=product_id)

    return redirect('gallery_list', product_id=product_id)


# ---------------- DELETE GALLERY IMAGE ----------------
def delete_gallery(request, img_id):
    img = get_object_or_404(ProductGallery, id=img_id)
    product_id = img.product.id
    img.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect('gallery_list', product_id=product_id)



# -------------Cart----------------

def cart_list(request):
    carts = Cart.objects.all().order_by('-date_added')
    return render(request, "adminpanel/cart_list.html", {"carts": carts})

def cart_items(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, "adminpanel/cart_items.html", {
        "cart": cart,
        "cart_items": cart_items,
    })

def delete_cart_item_admin(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_list')


# -------------Orders----------------

def orders_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/orders_list.html', {'orders': orders})


def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    products = OrderProduct.objects.filter(order=order)

    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
        'products': products
    })