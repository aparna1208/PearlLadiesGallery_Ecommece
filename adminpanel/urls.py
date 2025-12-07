from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("view_user/<int:user_id>/", views.view_user, name="view_user"),

    path('users/', views.users_list, name='admin_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:cat_id>/', views.delete_category, name='delete_category'),


    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),

    # Variation
    path("products/<int:product_id>/variations/", views.variation_list, name="variation_list"),
    path("products/<int:product_id>/variations/add/", views.add_variation, name="add_variation"),
    path("variations/delete/<int:variation_id>/", views.delete_variation, name="delete_variation"),

    # Gallery
    path("products/<int:product_id>/gallery/", views.gallery_list, name="gallery_list"),
    path("products/<int:product_id>/gallery/add/", views.add_gallery, name="add_gallery"),
    path("gallery/delete/<int:img_id>/", views.delete_gallery, name="delete_gallery"),

    # cart
    path("carts/", views.cart_list, name="cart_list"),
    path("carts/<int:cart_id>/items/", views.cart_items, name="cart_items"),
    path("cart-item/delete/<int:item_id>/", views.delete_cart_item_admin, name="delete_cart_item_admin"),

    # orders
    path("admin-orders/", views.orders_dashboard, name="orders_dashboard"),
    path("admin-orders/<int:order_id>/", views.view_order, name="view_order"),

]
