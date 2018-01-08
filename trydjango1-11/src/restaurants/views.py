# Q is used to filter using (|) operation
# This is called - Q Lookups
from django.db.models import Q

from django.shortcuts import render, get_object_or_404

# Importing Class based view
from django.views import View

from django.views.generic import TemplateView, ListView, DetailView
# Importing Template View. Importing Generic Views

from django.http import HttpResponse

from .models import RestaurantLocation


# Create your views here.
def restaurant_listview(request):
	template_name = 'restaurants/restaurants_list.html'
	queryset = RestaurantLocation.objects.all()
	context = {
		"object_list": queryset,
	}
	return render(request, template_name, context)


# Generic - ListView
class RestaurantListView(ListView):

    # def get_context_data(self, *args, **kwargs):
    #     print(self.kwargs)
    #     context = super(RestaurantListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    # This method shows you what Context or data is retreiving and helps you see the 
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

# Generic - DetailView
class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all()

    # we don't know what Context is coming through by default. So, we mention it.
    # when you see the results in Terminal, it retreives the {'pk'} passed in URL
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
    def get_object(self, *args, **kwargs):
        rest_id = self.kwargs.get('rest_id') # <whatever_id> you gave in URLs RegexGroup
        obj = get_object_or_404(RestaurantLocation, pk=rest_id) # OR  id = rest_id
        return obj