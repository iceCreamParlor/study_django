from django.db import models # Use AUTH_USER_MODEL
from django.conf import settings

from django.core.mail import send_mail
from django.db.models.signals import post_save
from .utils import code_generator
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL
# Create your models here.

class ProfileManager(models.Manager):
    def toggle_follow(self, profile_user, user_to_toggle):
        profile_=Profile.objects.get(user__username__iexact=user_to_toggle)
        user = request.user
        is_following=False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            if_following=True
        return is_following

class Profile(models.Model):
    user        = models.OneToOneField(User) # user.profile 
    followers   = models.ManyToManyField(User, related_name='followers', blank=True)
    following   = models.ManyToManyField(User, related_name='following', blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    activated   = models.BooleanField(default=False)
    activation_key= models.CharField(max_length=120, blank=True, null=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        print("Activation")
        if self.activated:
            pass
        else:
            self.activation_key = code_generator()
            self.save()
            path_ = reverse('activate', kwargs={"code":self.activation_key}) # Activate Key
            subject = 'Activate Account',
            message = f'Activate your account here: {path_}',
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [self.user.email],
            html_message = f'<p>Activate your account here: {path_}</p>',
            fail_silently=False,
            
            
            sent_mail = send_mail(
                subject, 
                message, 
                from_email, 
                recipient_list, 
                html_message=html_message, 
                fail_silently=False
            )
            return sent_mail
        

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        #default_user_profile = Profile.objects.get_or_create(user__id=1)[0]
        #default_user_profile.followers.add(instance)
        #default_user_profile.followers.remove(instance)
        #default_user_profile.save()
        #profile.followers.add(default_user_profile)
        #profile.followers.add(2)

post_save.connect(post_save_user_receiver, sender=User)