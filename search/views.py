import operator
from functools import reduce

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render



from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse

from .forms import MixtureForm
from .forms import SearchForm
from .models import House

# Create your views here.


items_each_page = 20


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name_get = form.cleaned_data['search_name']
            name_get = str(name_get)
            name_get = name_get.split(' ')
            qlist = []
            if name_get:
                for each in name_get:
                    q_obj = Q(name__contains=each)
                    qlist.append(q_obj)
            city_get = form.cleaned_data['search_city']
            location_get = form.cleaned_data['search_location']
            area_get = form.cleaned_data['search_area']
            area_get = float(area_get)
            price_get = form.cleaned_data['search_price']
            price_get = float(price_get)
            House_list = House.objects.filter((reduce(operator.and_, qlist)) & Q(city__contains= city_get) & Q(location__contains=location_get) & Q(area__gte=area_get) & Q(price__lte=price_get))
            House_list_weak = House.objects.filter((reduce(operator.or_, qlist)) & Q(city__contains= city_get) & Q(location__contains=location_get) & Q(area__gte=area_get) & Q(price__lte=price_get))

            return render(request, 'results.html', {'House_list': House_list, 'House_list_weak': House_list_weak})
        else:
            return HttpResponse('Invalid search!')
    else:
        form = SearchForm()
        return render (request, 'index.html', {'form': form})

def mixture(request, s):

    form = MixtureForm(s)

    anything_get = s
    anything_get = str(anything_get)
    anything_get = anything_get.split(' ')

    qlist = []
    if anything_get:
        for each in anything_get:
            q_obj = (Q(name__contains=each) | Q(city__contains=each) | Q(location__contains=each))

            qlist.append(q_obj)
    House_list = House.objects.filter(reduce(operator.and_, qlist))
    House_list_weak = House.objects.filter(reduce(operator.or_, qlist))

    rlist = []
    for h in House_list:
        rlist.append(h)
    for h in House_list_weak:
        rlist.append(h)

    paginator = Paginator(rlist, items_each_page)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'fenye.html', {'contacts': contacts})

def redirect (request):
    if request.method == 'POST':
        s = request.POST['search_anything']
        return HttpResponseRedirect(reverse('mixture', args=(s,)))
    else:
        form = MixtureForm()
        return render(request, 'mixture.html', {'form': form})