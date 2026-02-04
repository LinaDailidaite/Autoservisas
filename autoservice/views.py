from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from .models import Car, Service, Order, OrderLine
from django.views import generic
from django.db.models import Q

def index(request):
    num_car = Car.objects.all().count()
    num_service = Service.objects.all().count()
    num_order = Order.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_car': num_car,
        'num_service': num_service,
        'num_order': num_order,
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context = context)

def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars
    }
    print(cars)
    return render(request, template_name='cars.html', context=context)

def car(request, car_id):
    car = Car.objects.get(pk=car_id)
    return render(request, template_name='car.html', context={'car': car})

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 3

def orders_list(request):
    orders = Order.objects.all()
    print("ORDERS COUNT:", orders.count())
    return render(request, "orders.html", {"orders": orders})

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"

def search(request):
    query = request.GET.get('query','')

    if query:
        car_search_results = Car.objects.filter(
            Q(model__icontains=query) |
            Q(client_name__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(make__icontains=query) |
            Q(vin_code__icontains=query)
        ).distinct()
    else:
        car_search_results = Car.objects.none()

    context = {
        "query": query,
        "cars": car_search_results
    }
    return render(request, "search.html", context=context)