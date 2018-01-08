# Q is used to filter using (|) operation
# This is called - Q Lookups
from django.db.models import Q

from django.shortcuts import render

# Importing Class based view
from django.views import View

from django.views.generic import TemplateView, ListView
# Importing Template View

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