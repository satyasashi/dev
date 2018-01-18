from django.conf import settings
from django.db import models
# Signals. Does a task Before saving something and after saving (Pre_save & Post_save)
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator

# import validators.py to validate some fields
from .validators import validate_category


User = settings.AUTH_USER_MODEL

# Create your models here.
class RestaurantLocation(models.Model):
    owner       =   models.ForeignKey(User)
    name        =   models.CharField(max_length=120)
    location    =   models.CharField(max_length=120, null=True, blank=True)
    category    =   models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
    timestamp   =   models.DateTimeField(auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True)
    slug		=	models.SlugField(null=True, blank=True)
    #my_date_field = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        

    @property
    def title(self):
        '''
        We have 'name' field, but to work with slug generation we need 'title' field
        So, we are creating 'title' decorator which acts as getting an object ->
            RestaurantLocation.title

        So, we make it return 'name' so that it just acts as title, but returns 
        value of 'name'. Because we already created 'name' and made migrations.

        If we now think to change field name to 'title' it'll be pain in the butt.
        '''
        return self.name # obj.title

# receiver function
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# receiver function
# def rl_post_save_receiver(sender, instance, *args, **kwargs):
#     print('Saved.')
#     print(instance.timestamp)


pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
#post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)