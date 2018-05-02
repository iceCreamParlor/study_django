from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from .models import Item ,HealthClub, HealthDiary
from .forms import ItemForm
# Create your tests here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, "home.html", {})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.following.all()]
        qs = Item.objects.filter(user__id__in = is_following_user_ids, public=True).order_by("-updated")

        return render(request, "menus/home-feed.html", {"object_list" : qs})

class ItemListView(ListView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
        
class ItemDetailView(DetailView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'menus/form.html'
    form_class = ItemForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create Item'
        return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'menus/detail-update.html'
    form_class = ItemForm
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Item'
        return context
    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

@login_required(login_url = "/login")
def health_exercise(request):
    healthclub_id = request.GET.get('healthclub_id')
    user = request.user
    healthclub = HealthClub.objects.get(id = healthclub_id)
    timestamp = datetime.now()

    obj = HealthDiary.objects.create(
        user = user,
        healthclub = healthclub,
        timestamp = timestamp,
    )
    obj.save()
    context = {'healthclub' : healthclub, 'user' : user, 'timestamp' : timestamp}
    return render(request, 'menus/health_diary.html', context)

@login_required(login_url = "/login")
def health_check(request):
    context = {}
    return render(request, 'menus/health_check.html', context)
