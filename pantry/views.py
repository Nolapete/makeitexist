from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F
from .models import Location, StorageUnit, PantryItem, Stock, ItemCategory
from .forms import LocationForm, StorageUnitForm, PantryItemForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def pantry_item_detail(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    return render(request, "pantry/pantry_item_detail.html", {"item": item})


@login_required
def pantry_item_update(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)

    if request.method == "POST":
        form = PantryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ "{item.name}" updated.')
            return redirect("pantry:pantry_item_detail", pk=item.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PantryItemForm(instance=item)

    return render(
        request,
        "pantry/pantry_item_form.html",
        {"form": form, "title": "Edit Item", "item": item},
    )


@login_required
def pantry_item_create(request):
    # Pre-fill barcode if passed in URL
    initial_data = {}
    barcode = request.GET.get("barcode")
    if barcode:
        initial_data["barcode"] = barcode

    if request.method == "POST":
        form = PantryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, f'✅ "{item.name}" added to your pantry.')
            return redirect("pantry:pantry_item_detail", pk=item.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PantryItemForm(initial=initial_data)

    return render(
        request, "pantry/pantry_item_form.html", {"form": form, "title": "Add New Item"}
    )


@login_required
def pantry_item_create(request):
    barcode = request.GET.get("barcode", "")
    return render(request, "pantry/item_form.html", {"barcode": barcode})


@login_required
def barcode_scan(request):
    return render(request, "pantry/barcode_scan.html")


@login_required
def api_barcode_scan(request):
    barcode = request.GET.get("barcode", "").strip()
    if not barcode:
        return JsonResponse({"error": "No barcode provided"}, status=400)

    try:
        item = PantryItem.objects.get(barcode=barcode)
        return JsonResponse(
            {
                "found": True,
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "barcode": item.barcode,
                    "min_stock_level": item.min_stock_level,
                },
            }
        )
    except PantryItem.DoesNotExist:
        return JsonResponse(
            {"found": False, "error": "Item not found in your pantry"}, status=404
        )


@login_required
def location_list(request):
    locations = Location.objects.prefetch_related("storage_units")
    return render(request, "pantry/location_list.html", {"locations": locations})


@login_required
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    storage_units = location.storage_units.all().prefetch_related("stocks__item")
    return render(
        request,
        "pantry/location_detail.html",
        {"location": location, "storage_units": storage_units},
    )


@login_required
def location_create(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_by = request.user
            location.save()
            messages.success(request, f'✅ Location "{location.name}" created.')
            return redirect("pantry:location_detail", pk=location.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LocationForm()

    return render(
        request,
        "pantry/location_form.html",
        {"form": form, "title": "Create New Location"},
    )


@login_required
def location_update(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Location "{location.name}" updated.')
            return redirect("pantry:location_detail", pk=location.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LocationForm(instance=location)

    return render(
        request,
        "pantry/location_form.html",
        {"form": form, "title": "Edit Location", "location": location},
    )


@login_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        name = location.name
        location.delete()
        messages.success(request, f'🗑️ Location "{name}" deleted.')
        return redirect("pantry:location_list")

    return render(
        request, "pantry/location_confirm_delete.html", {"location": location}
    )


@login_required
def storage_unit_detail(request, pk):
    unit = get_object_or_404(StorageUnit.objects.select_related("location"), pk=pk)
    stocks = unit.stocks.select_related("item").all()
    return render(
        request, "pantry/storage_unit_detail.html", {"unit": unit, "stocks": stocks}
    )


@login_required
def storage_unit_update(request, pk):
    unit = get_object_or_404(StorageUnit, pk=pk)
    if request.method == "POST":
        form = StorageUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'✅ Updated {unit.get_unit_type_display()} "{unit.name}".'
            )
            return redirect("pantry:storage_unit_detail", pk=unit.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StorageUnitForm(instance=unit)

    return render(
        request,
        "pantry/storage_unit_form.html",
        {"form": form, "title": f"Edit {unit.get_unit_type_display()}", "unit": unit},
    )


@login_required
def storage_unit_delete(request, pk):
    unit = get_object_or_404(StorageUnit, pk=pk)
    location_pk = unit.location.pk
    if request.method == "POST":
        name = unit.name
        unit_type = unit.get_unit_type_display()
        unit.delete()
        messages.success(request, f'🗑️ Deleted {unit_type} "{name}".')
        return redirect("pantry:location_detail", pk=location_pk)

    return render(request, "pantry/storage_unit_confirm_delete.html", {"unit": unit})


# --- Pantry Item Views ---
@login_required
def pantry_item_detail(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    return render(request, "pantry/pantry_item_detail.html", {"item": item})


@login_required
def pantry_item_update(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    # Placeholder for form handling
    messages.info(request, "Edit item functionality coming soon.")
    return redirect("pantry:pantry_item_detail", pk=pk)


# --- Stock Management ---
@login_required
def stock_add(request):
    # Read optional pre-fill parameters
    item_pk = request.GET.get("item")
    unit_pk = request.GET.get("unit")

    # Try to pre-fill item and unit
    try:
        item = get_object_or_404(PantryItem, pk=item_pk) if item_pk else None
    except (ValueError, TypeError):
        item = None

    try:
        unit = get_object_or_404(StorageUnit, pk=unit_pk) if unit_pk else None
    except (ValueError, TypeError):
        unit = None

    # If POST, process the form
    if request.method == "POST":
        item_pk = request.POST.get("item_pk") or item_pk
        unit_pk = request.POST.get("unit_pk") or unit_pk
        quantity = request.POST.get("quantity")
        expiry = request.POST.get("expiry_date")

        # Validate item
        if not item_pk:
            messages.error(request, "Item is required.")
            return render_stock_add_form(request, None, None, quantity, expiry)

        try:
            item = get_object_or_404(PantryItem, pk=item_pk)
        except (ValueError, TypeError):
            messages.error(request, "Invalid item.")
            return render_stock_add_form(request, None, unit, quantity, expiry)

        # Validate unit
        if not unit_pk:
            messages.error(request, "Storage unit is required.")
            return render_stock_add_form(request, item, None, quantity, expiry)

        try:
            unit = get_object_or_404(StorageUnit, pk=unit_pk)
        except (ValueError, TypeError):
            messages.error(request, "Invalid storage unit.")
            return render_stock_add_form(request, item, None, quantity, expiry)

        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid quantity.")
            return render_stock_add_form(request, item, unit, quantity, expiry)

        # Create stock
        stock = Stock.objects.create(
            item=item, storage_unit=unit, quantity=quantity, expiry_date=expiry or None
        )

        messages.success(
            request, f"✅ Added {quantity} of '{item.name}' to '{unit.name}'."
        )
        return redirect("pantry:storage_unit_detail", pk=unit.pk)

    # If GET, show form
    return render_stock_add_form(request, item, unit)


# Helper function to avoid code duplication
def render_stock_add_form(request, item=None, unit=None, quantity="", expiry=""):
    items = PantryItem.objects.order_by("name")
    units = StorageUnit.objects.select_related("location")

    return render(
        request,
        "pantry/stock_add.html",
        {
            "items": items,
            "units": units,
            "item": item,
            "unit": unit,
            "quantity": quantity,
            "expiry": expiry,
        },
    )


@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        expiry = request.POST.get("expiry_date")

        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
            return redirect("pantry:stock_edit", pk=pk)

        stock.quantity = quantity
        stock.expiry_date = expiry or None
        stock.save()
        messages.success(request, f"Updated stock for {stock.item.name}.")
        return redirect("pantry:storage_unit_detail", pk=stock.storage_unit.pk)

    return render(request, "pantry/stock_form.html", {"stock": stock})


@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)

    if request.method == "POST":
        item_name = stock.item.name
        unit_name = stock.storage_unit.name
        stock.delete()
        messages.success(request, f"✅ Removed '{item_name}' from '{unit_name}'.")
        return redirect("pantry:storage_unit_detail", pk=stock.storage_unit.pk)

    return render(request, "pantry/stock_confirm_delete.html", {"stock": stock})


# --- Barcode Scanning (Web UI) ---
@login_required
def barcode_scan(request):
    """Simple page to simulate or handle barcode scanning"""
    scanned_barcode = request.GET.get("barcode", "").strip()
    context = {"scanned_barcode": None, "item": None, "error": None}

    if scanned_barcode:
        try:
            item = PantryItem.objects.get(barcode=scanned_barcode)
            context.update({"scanned_barcode": scanned_barcode, "item": item})
        except PantryItem.DoesNotExist:
            context["error"] = f"No item found with barcode: {scanned_barcode}"

    return render(request, "pantry/barcode_scan.html", context)


# --- API Endpoint: Barcode Scan (for mobile app) ---
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
@login_required
def api_barcode_scan(request):
    """API endpoint to handle barcode scan from mobile app"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            barcode = data.get("barcode", "").strip()

            if not barcode:
                return JsonResponse({"error": "No barcode provided"}, status=400)

            try:
                item = PantryItem.objects.get(barcode=barcode)
                return JsonResponse(
                    {
                        "found": True,
                        "item": {
                            "id": item.id,
                            "name": item.name,
                            "barcode": item.barcode,
                            "min_stock_level": item.min_stock_level,
                            "category": item.category.name if item.category else None,
                            "default_storage": (
                                {
                                    "id": item.default_storage.id,
                                    "name": item.default_storage.name,
                                    "type": item.default_storage.get_unit_type_display(),
                                    "location": item.default_storage.location.name,
                                }
                                if item.default_storage
                                else None
                            ),
                        },
                    }
                )
            except PantryItem.DoesNotExist:
                return JsonResponse(
                    {"found": False, "error": "Item not found in your pantry"},
                    status=404,
                )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "POST request required"}, status=405)


@login_required
def alerts_dashboard(request):
    """
    Show all active alerts:
    - Items expiring within 7 days
    - Items out of stock (quantity == 0)
    - Items below min_stock_level (low stock)
    """
    today = timezone.now().date()
    expiry_threshold = today + timedelta(days=7)

    # 1. Expiring Soon (not expired yet, within 7 days)
    expiring_soon = (
        Stock.objects.filter(
            expiry_date__gte=today, expiry_date__lte=expiry_threshold, quantity__gt=0
        )
        .select_related("item", "storage_unit")
        .order_by("expiry_date")
    )

    # 2. Out of Stock (quantity == 0)
    out_of_stock = (
        PantryItem.objects.filter(stocks__quantity=0)
        .distinct()
        .prefetch_related("stocks__storage_unit")
    )

    # 3. Low Stock (quantity > 0 but below min_stock_level)
    low_stock = (
        PantryItem.objects.exclude(
            stocks__quantity__gte=F("min_stock_level")  # quantity >= min_stock_level
        )
        .exclude(stocks__quantity=0)  # already covered above
        .distinct()
        .prefetch_related("stocks__storage_unit")
    )

    context = {
        "expiring_soon": expiring_soon,
        "out_of_stock": out_of_stock,
        "low_stock": low_stock,
        "today": today,
    }
    return render(request, "pantry/alerts_dashboard.html", context)
