from django import forms

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