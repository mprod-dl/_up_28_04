from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# View
def view_products(request):
    products = Product.objects.filter(is_deleted=False).order_by('id')
    return render(request, 'view_products.html', {
        'products': products,
        'active_tab': 'view_products',
        'active_nav': 'view_products'
    })

def view_product_by_id(request, id):
    product = Product.objects.filter(id=id, is_deleted=False).first()
    return render(request, 'view_product_by_id.html', {
        'product': product,
        'active_tab': 'view_products'
    })

def view_products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_deleted=False).order_by('id')
    return render(request, 'view_products.html', {
        'products': products,
        'active_tab': 'view_products',
        'filter_title': f'Фильтр по категории: { category.name }'
    })

def view_products_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    products = tag.product_set.filter(is_deleted=False).order_by('id')
    return render(request, 'view_products.html', {
        'products': products,
        'active_tab': 'view_products',
        'filter_title': f'Фильтр по тегу: { tag.name }'
    })

def view_categories_and_tags(request):
    categories = Category.objects.all()
    tags = Tag.objects.all().order_by('id')
    return render(request, 'view_categories_and_tags.html', {
        'categories': categories,
        'tags': tags,
        'active_tab': 'view_categories_and_tags',
        'active_nav': 'view_categories_and_tags'
    })
    
# Cart
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_products')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total': total,
        'active_tab': 'view_cart',
        'active_nav': 'view_cart'
    })


# Profile
@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {
        'user': request.user,
        'active_tab': 'view_profile',
        'active_nav': 'view_profile'
    })

# Add
@login_required
def add_product(request):
    if not request.user.groups.filter(name__in=['Seller', 'Admin']).exists() and not request.user.is_superuser:
        return redirect('forbidden')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form = ProductForm()
    return render(request, 'form.html', {
        'form': form,
        'form_label': "Добавить товар",
        'active_tab': "view_products",
        'active_nav': 'add_product'
    })

@login_required
def add_category(request):
    if not request.user.groups.filter(name__in=['Seller', 'Admin']).exists() and not request.user.is_superuser:
        return redirect('forbidden')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_categories_and_tags')
    else:
        form = CategoryForm()
    return render(request, 'form.html', {
        'form': form,
        'form_label': "Добавить категорию",
        'active_tab': "view_categories_and_tags",
        'active_nav': 'add_category'
    })

@login_required
def add_tag(request):
    if not request.user.groups.filter(name__in=['Seller', 'Admin']).exists() and not request.user.is_superuser:
        return redirect('forbidden')
    
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_categories_and_tags')
    else:
        form = TagForm()
    return render(request, 'form.html', {
        'form': form,
        'form_label': "Добавить тег",
        'active_tab': "view_categories_and_tags",
        'active_nav': 'add_tag'
    })


# Edit
@login_required
def edit_product(request, id):
    if not request.user.groups.filter(name__in=['Seller', 'Admin']).exists() and not request.user.is_superuser:
        return redirect('forbidden')
    
    product = Product.objects.filter(id=id, is_deleted=False).first()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'form.html', {
        'form': form,
        'form_label': "Добавить товар",
        'active_tab': "add_product",
    })
    
# forbidden
def forbidden(request):
    return render(request, '403.html')