from django import forms

# import Model to created Form fields instead of re-creating field names
from .models import RestaurantLocation

# import validators.py to validate some fields
from .validators import validate_category

class RestaurantCreateForm(forms.Form):

	'''
	We use this form class to create form fields. These Form Fields are declared similar
	to Model Fields. So let's get required fields from Model.

	Change models.CharField(..) to forms.CharField() which has no args. Because, data 
	limitation is already specified in our Table in Database/Models.py
	'''
	name        =   forms.CharField()
	location    =   forms.CharField(required=False)
	category    =   forms.CharField(required=False)


	# cleaning with clean_<method_name>
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if name == "Hello":
			raise forms.ValidationError("Not a valid name")
		return name

class RestaurantLocationCreateForm(forms.ModelForm):
	# email = forms.EmailField()
	# category = forms.CharField(required=False, validators=[validate_category])
	# 	Commented above 'category' as we mentioned 'validators' in Models.py
	class Meta:
		model = RestaurantLocation
		fields = [
			'name',
			'location',
			'category'
		]

	# cleaning with clean_<method_name>
	# This is custom cleaning method runs after default 'clean' method
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if name == "Hello":
			raise forms.ValidationError("Not a valid name")
		return name

	# Cleaning with clean_<method_name>
	# This is custom cleaning method runs after default 'clean' method
	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
    #
	# 	if ".edu" in email:
	# 		raise forms.ValidationError("We do not accept .edu in emails")
	# 	return email