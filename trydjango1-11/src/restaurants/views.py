from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# function based view
def home(request):
	return render(request, "base.html", {"html_var": True})
	#return HttpResponse("HELLO")