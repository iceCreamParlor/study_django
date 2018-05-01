# -*- coding: utf-8 -*- 

import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation
# Create your views here.
#

@login_required(login_url = "/login")
def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
   # if(request.method=="GET"):
   #     print("GET")
   #if(request.method=="POST"):
   #    print(request.POST)
   #    form = RestaurantCreateForm(request.POST)

    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit = False)
           # user = request.user
           # title = request.POST.get("title")
           # location = request.POST.get("location")
           # category = request.POST.get("category")
           # obj = RestaurantLocation.objects.create(
           #         name = form.cleaned_data.get('name'), 
           #         location = form.cleaned_data.get('location'), 
           #         category = form.cleaned_data.get('category'),
           # )
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect("/restaurants")

    if form.errors:
        errors = form.errors
        print(form.errors)

    template_name = 'restaurant/forms.html'
    context =  { "form" : form, "errors": errors }

    return render(request, template_name, context)

def restaurant_listview(request):
    # 함수로view
    template_name = 'restaurant/restaurants_list.html'
    queryset = RestaurantLocation.objects.all()
    context =  {
        "object_list" : queryset
     }
    return render(request, template_name, context)

class RestaurantListView(LoginRequiredMixin, ListView):
    template_name = 'restaurant/restaurants_list.html'

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
        '''
        print(self.kwargs)
        slug = self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocation.objects.filter(Q(category__icontains = slug) | Q(category__iexact=slug))
        else: 
            queryset = RestaurantLocation.objects.all()
    
        return queryset
        '''

class SearchRestaurantListView(ListView):
    
    template_name = 'restaurant/restaurantlocation_detail.html'
    
    def get_queryset(self):
        print(self.kwargs)
        slug = self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocation.objects.filter(Q(name__icontains = slug) | Q(name__iexact=slug))
        else: 
            queryset = RestaurantLocation.objects.none()
        print(queryset)
        return queryset

class RestaurantDetailView(LoginRequiredMixin, DetailView):
    
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
    
    def get_context_data(self, *args, **kwargs):
        print(self.kwargs)
        context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context
    
    def get_object(self, *args, **kwargs):
        rest_id = self.kwargs.get('rest_id')
        obj = get_object_or_404(RestaurantLocation, id = rest_id) #pk = rest_id
        return obj
    def get_object_or_404(self, *args, **kargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(RestaurantLocation, slug = slug)
        if not obj:
             print("slug not found")
        return obj

# Use This one Because Simpler is Better
class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurant/forms.html'
    success_url = '/restaurants/'

    def form_valid(self, form):
        instance = form.save(commit= False)
        instance.owner = self.request.user
        #instance.save()
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurant/detail-update.html'
    login_url = '/login/'
    success_url = '/restaurants/'

    def form_valid(self, form):
        instance = form.save(commit= False)
        instance.owner = self.request.user
        #instance.save()
        return super(RestaurantCreateView, self).form_valid(form)
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context
