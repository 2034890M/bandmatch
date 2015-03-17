from django import template
from bandmatch.models import Advert, Band

register = template.Library()

@register.filter(name='get_ads_looking_for')
@register.inclusion_tag("bandmatch/search_bands.html")
def get_ads_looking_for(band):
	looking_for_list = []
	ads = Advert.objects.filter(band__exact = band)
	for ad in ads:
		print ad.looking_for
		looking_for_list.append(ad.looking_for)
	print looking_for_list
	return (looking_for_list)

register.tag('band_search_ads', get_ads_looking_for)