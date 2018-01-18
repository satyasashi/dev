# import Login required decorator
from django.contrib.auth.decorators import login_required

# import LoginRequiredMixin behaviour to Class Based View
# Similar (login_required)
from django.contrib.auth.mixins import LoginRequiredMixin

# Q is used to filter using (|) operation
# This is called - Q Lookups
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Importing Class based view
from django.views import View

# Importing Template View. Importing Generic Views
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import RestaurantLocationCreateForm
from .models import RestaurantLocation

# Create your views here.

#  Function based View to understand how it really works. Later Class Based View
@login_required(login_url='/login/')
def restaurant_createview(request):
    # Instance of Form
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None

    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False)
            # Customize
            # like pre_save
            instance.owner = request.user
            instance.save()
            # like post_save
            return HttpResponseRedirect("/restaurants/")
        else:
            return HttpResponseRedirect("/login/")

    if form.errors:
        errors = form.errors

    template_name = 'restaurants/form.html'
    context = {"form": form, "errors": errors,}
    return render(request, template_name, context)

# Function based View to understand how it really works. Later Class Based View
def restaurant_listview(request):
    template_name = 'restaurants/restaurants_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        "object_list": queryset,
    }
    return render(request, template_name, context)

# Function based View to understand how it really works. Later Class Based View
def restaurant_detailview(request, slug):
    template_name = 'restaurants/restaurantlocation_detail.html'
    obj = RestaurantLocation.objects.get(slug=slug)
    context = {
    "object": obj,
    }
    return render(request, template_name, context)


# Generic Class Based View - ListView
class RestaurantListView(ListView):

    # def get_context_data(self, *args, **kwargs):
    #     print(self.kwargs)
    #     context = super(RestaurantListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    # This method shows you what Context or data is retrieving and helps you see the
    # objects returned. For ListView Default Context will be 'object_list'.

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocation.objects.filter(
                Q(category__iexact=slug) |
                Q(category__icontains=slug)
                )
        else:
            queryset = RestaurantLocation.objects.all()
        return queryset

# Generic Class Based View- DetailView
class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all()#filter(category__icontains='asian')

    # we don't know what Context is coming through by default. So, we mention it.
    # when you see the results in Terminal, it retrieves the {'pk'} passed in URL
    # and the Object dictionary containing the Data Objects. So, you can use 'object'
    # to get -- 'name', 'category',...
    # For DetailView always Default Context will be 'object'

    def get_context_data(self, *args, **kwargs):
        print(self.kwargs)
        context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    # So far we can only call DetailView with Object 'pk' or 'slug'.
    # If you change <pk> to <some_id> in URLs it shows 'pk' or 'slug' AttributeError.
    # You can change this to <some_id> which is also Object ID/PK it needs by using
    # get_object(self, *args, **kwargs). Also Import 'get_object_or_404' shortcut to TryExcept.

    # def get_object(self, *args, **kwargs):
    #     rest_id = self.kwargs.get('rest_id') # <whatever_id> you gave in URLs RegexGroup
    #     obj = get_object_or_404(RestaurantLocation, pk=rest_id) # OR  id = rest_id
    #     return obj


# Generic Class Based View- CreateView
# 'LoginRequiredMixin' is similar to '@login_required()' decorator in
# Function Based Views. 'LoginRequiredMixin' should be LeftMost position in
# Inheritance list -->
#       RestaurantView( LoginRequiredMixin, <InheritanceList> )

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    success_url = '/restaurants/'

    # We have a way to create View associated to Authenticated User
    # As of now there is no association to it and hence we get
    # IntegrityError at /restaurants/create
    # Let's First create it in 'Function Based View' to understand
    # Later we'll implement in 'Class Based View'

    # Lets override another method 'form_valid'
    def form_valid(self, form):
        instance = form.save(commit= False)
        instance.owner = self.request.user
        # instance.save() By default 'CreateView' uses 'save()' in 'form_valid'
        return super(RestaurantCreateView, self).form_valid(form)