from django.contrib.sites.models import Site
from django.conf import settings


def site(request):
    """Adds a site context variable"""
    return {'site': Site.objects.get_current(), 'WEBMAIL_URL':settings.WEBMAIL_URL, 'EXTERNAL_WIKI_URL':settings.EXTERNAL_WIKI_URL }

def search(request):
	"""Adds a search form if a valid one isn't in there already"""
	from front.forms import SearchForm
	if request.method == 'POST' and SearchForm(request.POST).is_valid():
		return { }
	return {'search_form': SearchForm() }
