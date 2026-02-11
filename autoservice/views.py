from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Car, Service, Order, OrderLine, CustomUser
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import OrderReviewForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from .forms import UserChangeForm
from .forms import CustomUserChangeForm
from .forms import OrderReviewForm, UserChangeForm, CustomUserCreationForm, OrderCreateUpdateForm

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

class OrderListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 3

    def test_func(self):
        return self.request.user.is_staff

# def orders_list(request):
#     orders = Order.objects.all()
#     print("ORDERS COUNT:", orders.count())
#     return render(request, "orders.html", {"orders": orders})

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    form_class = OrderReviewForm

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

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

# Kūrimas
class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Order
    form_class = OrderCreateUpdateForm
    template_name = "order_form.html"
    success_url = reverse_lazy('orders')

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

# Redagavimas
class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    form_class = OrderCreateUpdateForm
    template_name = "order_form.html"
    success_url = reverse_lazy('orders')

    def test_func(self):
        return self.request.user.is_staff

# Trynimas
class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = "order_delete.html"
    success_url = reverse_lazy('orders')

    def test_func(self):
        return self.request.user.is_staff

class MyOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(reader=self.request.user)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

# 1. Pridėti paslaugą prie užsakymo
class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    fields = ['service', 'quantity']
    template_name = "order_line_form.html"

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.is_staff

# 2. Redaguoti esamą paslaugą
class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    fields = ['service', 'quantity']
    template_name = "order_line_form.html"

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.order.pk})

    def test_func(self):
        return self.request.user.is_staff

# 3. Pašalinti paslaugą iš užsakymo
class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine
    template_name = "order_line_delete.html"

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.order.pk})

    def test_func(self):
        return self.request.user.is_staff