from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404
from django.views.generic import DetailView
# Create your views here.
from restaurant.models import RestaurantLocation
from menus.models import Item

User = get_user_model()

class ProfileDetailView(DetailView):
    #queryset = User.objects.filter(is_active=True)
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get("username")
        print(username)
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact = username, is_active = True)
    
    def get_context_data(self, *args, **kargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kargs)
        print(context)
        user = self.get_object()
        item_exists = Item.objects.filter(user = user).exists()
        query = self.request.GET.get('q')
        qs  = RestaurantLocation.objects.filter(owner=user)
        if query:
            qs = qs.filter(name__icontains = query)
        if item_exists and qs.exists():
            context['locations'] = qs
        return context
