from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DetailView, View, CreateView
from django.shortcuts import redirect
# Create your views here.
from restaurant.models import RestaurantLocation
from menus.models import Item
from .models import Profile
from .forms import RegisterForm
User = get_user_model()

def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated=True
                profile.activation_key=None
                profile.save()
                return redirect("/login")
    # invalid code
    return redirect("/login")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #print(request.data)
        print(request.POST)
        user_to_toggle = request.POST.get('username')
        print(user_to_toggle)
        profile_, is_following = Profile.objects.toggle_follow(request.user, user_to_toggle)
        # profile_=Profile.objects.get(user__username__iexact=user_to_toggle)
        # user = request.user
        # if user in profile_.followers.all():
        #     profile_.followers.remove(user)
        # else:
        #     profile_.followers.add(user)

        return redirect("/u/icecreamparlor/")

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
            qs = qs.search(query)
        if item_exists and qs.exists():
            context['locations'] = qs
        return context
