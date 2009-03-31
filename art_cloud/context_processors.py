from django.contrib.sites.models import Site

def site(request):
    """Adds a site context variable"""
    return {'site': Site.objects.get_current() }

def search(request):
	"""Adds a search form if a valid one isn't in there already"""
	from front.forms import SearchForm
	if request.method == 'POST' and SearchForm(request.POST).is_valid():
		return { }
	return {'search_form': SearchForm() }
