from django.urls import path
from . import views

urlpatterns = [
    path("cost_form/", views.cost_calculation_form, name="cost_form"),
    path("get_sizes/<int:item_id>/", views.get_sizes, name="get_sizes"),
    path("get_price/<int:size_id>/", views.get_price, name="get_price"),
    path("submit_cost_form/", views.submit_cost_form, name="submit_cost_form"),
    
    #path("categories/", views.categories, name="categories"),
    #path("categories/<int:category_id>/items/", views.category_items, name="category_items"),
    path("items/<int:item_id>/sizes/", views.item_sizes, name="item_sizes"),
    path("sizes/<int:size_id>/prices/", views.size_prices, name="size_prices"),
    
    
    
    path("get-autofill-data/", views.get_autofill_data, name="get_autofill_data"),

    
    
    
    ####
    ####
    ####
    ####
    ####
    
    # Category URLs
    path("categories/", views.category_list, name="categories"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:category_id>/update/", views.category_update, name="category_update"),
    path("categories/<int:category_id>/delete/", views.category_delete, name="category_delete"),
    
    path("category-items/", views.category_item_list, name="category_items"),
    path("category-items/add/", views.category_item_create, name="category_item_create"),
    path("category-items/edit/<int:item_id>/", views.category_item_edit, name="category_item_edit"),
    path("category-items/delete/<int:item_id>/", views.category_item_delete, name="category_item_delete"),
    
    
    
    path("category-items-size/", views.category_item_size_list, name="category_items_size"),
    path("category-items-size/add/", views.category_item_size_create, name="category_item_size_create"),
    path("category-items-size/edit/<int:item_id>/", views.category_item_size_edit, name="category_item_size_edit"),
    path("category-items-size/delete/<int:item_id>/", views.category_item_size_delete, name="category_item_size_delete"),



    path("category-items-size-price/", views.category_item_size_price_list, name="category_items_size_price"),
    path("category-items-size-price/add/", views.category_item_size_price_create, name="category_item_size_price_create"),
    path("category-items-size-price/edit/<int:item_id>/", views.category_item_size_price_edit, name="category_item_size_price_edit"),
    path("category-items-size-price/delete/<int:item_id>/", views.category_item_size_price_delete, name="category_item_size_price_delete"),

    # Item Size URLs
    # path("items/<int:item_id>/sizes/", views.item_size_list, name="item_sizes"),
    # path("item_sizes/create/", views.item_size_create, name="item_size_create"),
    # path("item_sizes/<int:size_id>/update/", views.item_size_update, name="item_size_update"),
    # path("item_sizes/<int:size_id>/delete/", views.item_size_delete, name="item_size_delete"),

    # Size Price URLs
    path("sizes/<int:size_id>/prices/", views.size_price_list, name="size_prices"),
    path("size_prices/create/", views.size_price_create, name="size_price_create"),
    path("size_prices/<int:price_id>/update/", views.size_price_update, name="size_price_update"),
    path("size_prices/<int:price_id>/delete/", views.size_price_delete, name="size_price_delete"),

    # Machine Cost URLs
    path("machine_costs/", views.machine_cost_list, name="machine_costs"),
    path("machine_costs/create/", views.machine_cost_create, name="machine_cost_create"),
    path("machine_costs/<int:cost_id>/update/", views.machine_cost_update, name="machine_cost_update"),
    path("machine_costs/<int:cost_id>/delete/", views.machine_cost_delete, name="machine_cost_delete"),
]
