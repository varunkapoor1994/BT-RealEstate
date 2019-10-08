from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from .models import Listing
from realtors.models import Realtor
from .choices import bedrooms, cities, prices


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings,
        'cities': cities,
        'bedrooms': bedrooms,
        'prices': prices
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    mvp_realtor = Realtor.objects.all().filter(is_mvp=True)
    context = {
        'listing': listing,
        'mvp_realtors': mvp_realtor
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    query_set = Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        if request.GET['keywords']:
            query_set = query_set.filter(
                description__icontains=request.GET['keywords'])
    if 'city' in request.GET:
        if request.GET['city']:
            query_set = query_set.filter(
                city__iexact=request.GET['city'])
    if 'state' in request.GET:
        if request.GET['state']:
            query_set = query_set.filter(
                state__iexact=request.GET['state'])
    if 'bedrooms' in request.GET:
        if request.GET['bedrooms']:
            query_set = query_set.filter(
                bedrooms__iexact=request.GET['bedrooms'])
    if 'price' in request.GET:
        if request.GET['price']:
            query_set = query_set.filter(
                price__lte=request.GET['price'])
    context = {
        'cities': cities,
        'bedrooms': bedrooms,
        'prices': prices,
        'listings': query_set,
        'values' : request.GET
    }
    return render(request, 'listings/search.html', context)
