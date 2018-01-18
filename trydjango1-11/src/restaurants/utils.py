import random # To create random of something
import string # To use strings

from django.utils.text import slugify # To create slugs automatically

'''
random_string_generator() is also explained in Local Python Directory as test.py


1] What (__, chars=string.___ + string.___) does? :
string.ascii_lowercase --> abcdefghijklmnopqrstuvwxyz
string.digits --> 1234567890

chars = string.ascii_lowercase + string.digits --> abcdefghijklmnopqrstuvwxyz0123456789

2] random.choice(chars) - Selects random CHARACTER from 'chars' containing a-z0-9
	for _ in range(size) - 
			Takes range sizeNUMBER and iterates through it.

3] ''.join(random.choice(chars) for _ in range(size))
	for every Number in 'size' it creates random Charcter from a-z0-9
	and joins with '' empty string.


4] random_string_generator() is the function that takes 'size' as input and generates
   randomString upto that Size. Default size = 10

5] random_string_generator(50) takes '50' as it's 'size' as input and generates
   randomString upto to 50 Characters includes a-z0-9.

'''
DONT_USE = ['create',]

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
	"""
	This is for Django project and it assumes your instance(Model's) has
	a model with a slug field and a title Character(CHAR) Field.
	"""
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title) # Model's instance obj -> obj.title

	if slug in DONT_USE:
		new_slug = "{slug}-{randstr}".format(
			slug=slug,
			randstr=random_string_generator(size=4)
		)
		return unique_slug_generator(instance, new_slug=new_slug)

	# Klass holds instance(Model's) class name -> 
	# which at moment is 'RestaurantLocation'
	Klass = instance.__class__ 
	print(Klass)
	# Checks if the above slug exists in database
	qs_exists = Klass.objects.filter(slug=slug).exists()

	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug = slug,
			randstr = random_string_generator(size=4)
			)
		return unique_slug_generator(instance, new_slug=new_slug)

	return slug