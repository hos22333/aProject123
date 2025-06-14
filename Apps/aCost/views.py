from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Category, ItemSize, SizePrice, CostFormData, CategoryItem, AutoFillConfig
from .forms import CategoryForm, CategoryItemForm, ItemSizeForm, SizePriceForm, MachineCostForm

import json
from django.shortcuts import redirect


from Apps.aAppSubmittal.models import AddMachine

@login_required
def cost_calculation_form(request):
    
    
    categories = Category.objects.prefetch_related("items__sizes").order_by("id").all()
    
    sheet_keys = AddMachine.objects.exclude(nameForm__isnull=True).exclude(nameForm__exact="None").exclude(nameForm__exact="No").order_by('order')

    return render(request, "aCost/cost_form.html", {
        'categories': categories,
        "sheet_keys": sheet_keys,
    })





def get_autofill_data(request):
    project_type = request.GET.get('project_type')
    print(f"Project Type: {project_type}")

    item_ids = {}
    size_ids = {}
    quantity_map = {}

    configs = AutoFillConfig.objects.filter(project_type=project_type)

    for config in configs:
        cat_id = f"{config.category_id:02}"  # e.g., '01'
        row_num = f"{config.row_number:02}"  # e.g., '01'

        # Keys must match frontend expectations
        item_ids[f'Cat{cat_id}Row{row_num}Field01'] = config.item.id if config.item else 0
        size_ids[f'Cat{cat_id}Row{row_num}Field02'] = config.size.id if config.size else 0
        quantity_map[f'{config.category_id}_{config.row_number}'] = config.quantity

    return JsonResponse({
        'item_ids': item_ids,
        'size_ids': size_ids,
        'quantity_map': quantity_map,
    })
    
    
# def get_autofill_data(request):
    


#     project_type = request.GET.get('project_type', None)  # <-- Add this line

#     print(f"Project Type: {project_type}")  # <-- Add this line for debugging
    
#     if project_type == 'OptionA':
#         item_ids = {
#             'Cat01Row01Field01': 1,
#             'Cat01Row02Field01': 2,
#             'Cat01Row03Field01': 1,
#             'Cat01Row04Field01': 2,
            
#             'Cat02Row01Field01': 3,
#             'Cat02Row02Field01': 4,
#             'Cat02Row03Field01': 3,
#             'Cat02Row04Field01': 4,
            
#             'Cat03Row01Field01': 5,
#             'Cat03Row02Field01': 6,
#             'Cat03Row03Field01': 5,
#             'Cat03Row04Field01': 6,
#         }

#         size_ids = {
#             'Cat01Row01Field02': 1,
#             'Cat01Row02Field02': 2,
#             'Cat02Row01Field02': 5,
#             'Cat02Row02Field02': 7,
#             'Cat03Row01Field02': 9,
#             'Cat03Row02Field02': 10,
#         }

#         quantity_map = {
#             '1_1': 100,
#             '1_2': 200,
#             '1_3': 100,
#             '1_4': 200,
            
#             '2_1': 150,
#             '2_2': 50,
#             '2_3': 150,
#             '2_4': 50,
            
#             '3_1': 20,
#             '3_2': 30,
#             '3_3': 20,
#             '3_4': 30,
#         }
        
        
#     if project_type == 'OptionB':
#         item_ids = {
#             'Cat01Row01Field01': 1,
#             'Cat01Row02Field01': 2,
#             'Cat01Row03Field01': 0,
#             'Cat01Row04Field01': 0,
            
#             'Cat02Row01Field01': 3,
#             'Cat02Row02Field01': 4,
#             'Cat02Row03Field01': 0,
#             'Cat02Row04Field01': 0,
            
#             'Cat03Row01Field01': 5,
#             'Cat03Row02Field01': 6,
#             'Cat03Row03Field01': 0,
#             'Cat03Row04Field01': 0,
#         }

#         size_ids = {
#             'Cat01Row01Field02': 1,
#             'Cat01Row02Field02': 2,
#             'Cat02Row01Field02': 5,
#             'Cat02Row02Field02': 7,
#             'Cat03Row01Field02': 9,
#             'Cat03Row02Field02': 10,
#         }

#         quantity_map = {
#             '1_1': 100,
#             '1_2': 200,
#             '1_3': 100,
#             '1_4': 200,
            
#             '2_1': 150,
#             '2_2': 50,
#             '2_3': 150,
#             '2_4': 50,
            
#             '3_1': 20,
#             '3_2': 30,
#             '3_3': 20,
#             '3_4': 30,
#         }
    
#     # add key-values
    
#     # based on the key-values get the parameters ids from the database
    
    

#     return JsonResponse({
#         'item_ids': item_ids,
#         'size_ids': size_ids,
#         'quantity_map': quantity_map,
#     })


@login_required
def get_sizes(request, item_id):
    sizes = ItemSize.objects.filter(item_id=item_id).values("id", "name")
    return JsonResponse({"sizes": list(sizes)})

@login_required
def get_price(request, size_id):
    price = SizePrice.objects.filter(size_id=size_id).order_by("-date").first()
    return JsonResponse({"price": price.price if price else 0})

@login_required
def submit_cost_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        update_existing = data.get("update_existing", False)

        if update_existing:
            cost_record = CostFormData.objects.filter(user=request.user).order_by("-created_at").first()
            if cost_record:
                cost_record.data = data
                cost_record.save()
                return JsonResponse({"message": "Record updated successfully"}, status=200)

        CostFormData.objects.create(user=request.user, data=data)
        return JsonResponse({"message": "New record created successfully"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)



@login_required
def categories(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST.get("description", "")
        Category.objects.create(name=name, description=description)
        return redirect("categories")
    
    categories = Category.objects.all()
    return render(request, "aCost/categories.html", {"categories": categories})

@login_required
def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST.get("description", "")
        CategoryItem.objects.create(category=category, name=name, description=description)
        return redirect("category_items", category_id=category_id)
    
    return render(request, "aCost/category_items.html", {"category": category})

@login_required
def item_sizes(request, item_id):
    item = get_object_or_404(CategoryItem, id=item_id)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST.get("description", "")
        ItemSize.objects.create(item=item, name=name, description=description)
        return redirect("item_sizes", item_id=item_id)

    return render(request, "aCost/item_sizes.html", {"item": item})

@login_required
def size_prices(request, size_id):
    size = get_object_or_404(ItemSize, id=size_id)

    if request.method == "POST":
        price = request.POST["price"]
        SizePrice.objects.create(size=size, price=price, user=request.user)
        return redirect("size_prices", size_id=size_id)

    return render(request, "aCost/size_prices.html", {"size": size})








#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################
#################

# CATEGORY VIEWS
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'aCost/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'aCost/category_form.html', {'form': form})

@login_required
def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'aCost/category_form.html', {'form': form})

@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('categories')










# CATEGORY ITEM VIEWS
def category_item_list(request):
    category_items = CategoryItem.objects.all()
    return render(request, "aCost/category_item_list.html", {"category_items": category_items})

def category_item_create(request):
    if request.method == "POST":
        form = CategoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_items")
    else:
        form = CategoryItemForm()
    
    return render(request, "aCost/category_item_form.html", {"form": form, "action": "Add New"})

def category_item_edit(request, item_id):
    item = get_object_or_404(CategoryItem, id=item_id)
    
    if request.method == "POST":
        form = CategoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("category_items")
    else:
        form = CategoryItemForm(instance=item)

    return render(request, "aCost/category_item_form.html", {"form": form, "action": "Edit"})

def category_item_delete(request, item_id):
    item = get_object_or_404(CategoryItem, id=item_id)
    
    if request.method == "POST":
        item.delete()
        return redirect("category_items")
    
    return render(request, "aCost/category_item_confirm_delete.html", {"item": item})



#####
###
###




# CATEGORY ITEM VIEWS
def category_item_size_list(request):
    category_items_size = ItemSize.objects.all()
    return render(request, "aCost/category_item_size_list.html", {"category_items_size": category_items_size})

def category_item_size_create(request):
    if request.method == "POST":
        form = ItemSizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_items_size")
    else:
        form = ItemSizeForm()
    
    return render(request, "aCost/category_item_size_form.html", {"form": form, "action": "Add New"})

def category_item_size_edit(request, item_id):
    item = get_object_or_404(ItemSize, id=item_id)
    
    if request.method == "POST":
        form = ItemSizeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("category_items_size")
    else:
        form = ItemSizeForm(instance=item)

    return render(request, "aCost/category_item_size_form.html", {"form": form, "action": "Edit"})

def category_item_size_delete(request, item_id):
    item = get_object_or_404(ItemSize, id=item_id)
    
    if request.method == "POST":
        item.delete()
        return redirect("category_items_size")
    
    return render(request, "aCost/category_item_size_confirm_delete.html", {"item": item})


###
###
###

# CATEGORY ITEM VIEWS
def category_item_size_price_list(request):
    category_items_size_price = SizePrice.objects.all()
    return render(request, "aCost/category_item_size_price_list.html", {"category_items_size_price": category_items_size_price})

def category_item_size_price_create(request):
    if request.method == "POST":
        form = SizePriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_items_size_price")
    else:
        form = SizePriceForm()
    
    return render(request, "aCost/category_item_size_price_form.html", {"form": form, "action": "Add New"})

def category_item_size_price_edit(request, item_id):
    item = get_object_or_404(SizePrice, id=item_id)
    
    if request.method == "POST":
        form = SizePriceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("category_items_size_price")
    else:
        form = SizePriceForm(instance=item)

    return render(request, "aCost/category_item_size_price_form.html", {"form": form, "action": "Edit"})

def category_item_size_price_delete(request, item_id):
    item = get_object_or_404(SizePrice, id=item_id)
    
    if request.method == "POST":
        item.delete()
        return redirect("category_items_size_price")
    
    return render(request, "aCost/category_item_size_price_confirm_delete.html", {"item": item})












# SIZE PRICE VIEWS
@login_required
def size_price_list(request, size_id):
    size = get_object_or_404(ItemSize, id=size_id)
    prices = size.prices.all()
    return render(request, 'aCost/size_price_list.html', {'size': size, 'prices': prices})

@login_required
def size_price_create(request):
    if request.method == 'POST':
        form = SizePriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = SizePriceForm()
    return render(request, 'aCost/size_price_form.html', {'form': form})

@login_required
def size_price_update(request, price_id):
    price = get_object_or_404(SizePrice, id=price_id)
    if request.method == 'POST':
        form = SizePriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = SizePriceForm(instance=price)
    return render(request, 'aCost/size_price_form.html', {'form': form})

@login_required
def size_price_delete(request, price_id):
    price = get_object_or_404(SizePrice, id=price_id)
    price.delete()
    return redirect('categories')














# MACHINE COST VIEWS
@login_required
def machine_cost_list(request):
    costs = MachineCost.objects.all()
    return render(request, 'aCost/machine_cost_list.html', {'costs': costs})

@login_required
def machine_cost_create(request):
    if request.method == 'POST':
        form = MachineCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = MachineCostForm()
    return render(request, 'aCost/machine_cost_form.html', {'form': form})

@login_required
def machine_cost_update(request, cost_id):
    cost = get_object_or_404(MachineCost, id=cost_id)
    if request.method == 'POST':
        form = MachineCostForm(request.POST, instance=cost)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = MachineCostForm(instance=cost)
    return render(request, 'aCost/machine_cost_form.html', {'form': form})

@login_required
def machine_cost_delete(request, cost_id):
    cost = get_object_or_404(MachineCost, id=cost_id)
    cost.delete()
    return redirect('categories')
